#!/usr/bin/env python
import rospy
import math
import xcom
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist,Vector3
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
import tf.transformations as transform

class MapSquare():

    parent = None
    position = (-1,-1)
    x = -1
    y = -1
    g = -1
    h = -1
    f = -1
    wall = 1


pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
goalposition = Vector3(0,0,0)
botposition = Vector3(0,0,0)
goalset = False
botset = False
wallfollow = False
wallfollowleft = False
forwardcone = [0,0,0,0,0,0,0,0,0,0,0]

forwardspeed = 0.0
rotspeed = 0.0
astarpath = []
avoidspot = (0,0)
currentpathnode = 0
lastcheckpoint = (0,0)
waitforlaserdata = True
hasangle = False
euler = 0
hashistogram = False
# positive is left

def astar(endy,endx,starty,startx):

    map2d = [[0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0],
         # [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7],
           [0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0], #5
           [0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0],
           [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0],
           [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1],
           [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1],
           [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1],#10
           [0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,0],
           [0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,0],
           [0,0,0,0,0,0,0,0,1,1,1,0,0,1,1,1,1,0],
           [0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,1,0],
         # [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7],
           [0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,1]]

    # + 10x + 9y to off set the negative start
    # y,x

    countx = 0
    county = -1
    # start = (12, 1)
    # end = (1,13)
    maparray = []
    start = (10 - starty,startx + 9)
    end = (10 - math.floor(endy),9 + math.floor(endx))
    for row in map2d:
        countx = 0
        county = county + 1
        rowarray = []
        maparray.append(rowarray)
        for col in row:
            newsquare = MapSquare()
            newsquare.g = math.sqrt((county - end[0])**2 +(countx - end[1])**2  )
            newsquare.x = countx
            newsquare.y = county
            newsquare.position = (county,countx)
            newsquare.f = -1
            newsquare.wall = map2d[county][countx]
            rowarray.append(newsquare)
            countx = countx + 1
    startsquare = MapSquare()
    startsquare.position = start
    startsquare.x = start[1]
    startsquare.y = start[0]
    startsquare.f = 0
    startsquare.g = 0
    startsquare.h = 0#math.sqrt((start[0] - end[0])**2 +(start[1] - end[1])**2  )
    endsquare = MapSquare()
    endsquare.position = end
    endsquare.g = 0
    endsquare.h = 0
    endsquare.f = -100
    endsquare.x = end[1]
    endsquare.y = end[0]

    opensquares = []

    currentsquare = startsquare

    opensquares.append(startsquare)

    while currentsquare.position != end :

        lastsquare = currentsquare


        if currentsquare.x > 0:
            if maparray[currentsquare.y][currentsquare.x - 1].wall == 0:
                # #print(maparray[currentsquare.y][currentsquare.x - 1])
                if maparray[currentsquare.y][currentsquare.x - 1].f == -1 or maparray[currentsquare.y][currentsquare.x - 1].f > (1 + currentsquare.f + maparray[currentsquare.y][currentsquare.x - 1].g):
                    maparray[currentsquare.y][currentsquare.x - 1].f = currentsquare.f + maparray[currentsquare.y][currentsquare.x - 1].g
                    maparray[currentsquare.y][currentsquare.x - 1].parent = currentsquare
                    opensquares.append(maparray[currentsquare.y][currentsquare.x - 1])
        if currentsquare.x < len(maparray[0]) - 1:
            if maparray[currentsquare.y][currentsquare.x + 1].wall == 0:
                # #print(maparray[currentsquare.y][currentsquare.x + 1].wall )
                if maparray[currentsquare.y][currentsquare.x + 1].f == -1 or maparray[currentsquare.y][currentsquare.x + 1].f > (1 + currentsquare.f + maparray[currentsquare.y][currentsquare.x + 1].g):
                    maparray[currentsquare.y][currentsquare.x + 1].f = currentsquare.f + maparray[currentsquare.y][currentsquare.x + 1].g
                    maparray[currentsquare.y][currentsquare.x + 1].parent = currentsquare
                    opensquares.append(maparray[currentsquare.y][currentsquare.x + 1])


        if currentsquare.y > 0:
            if maparray[currentsquare.y - 1][currentsquare.x ].wall == 0:
                #print(maparray[currentsquare.y - 1][currentsquare.x ].wall)
                if maparray[currentsquare.y - 1 ][currentsquare.x ].f == -1 or maparray[currentsquare.y - 1][currentsquare.x ].f > (1 + currentsquare.f + maparray[currentsquare.y - 1][currentsquare.x ].g):
                    maparray[currentsquare.y - 1][currentsquare.x ].f = currentsquare.f + maparray[currentsquare.y - 1][currentsquare.x ].g
                    maparray[currentsquare.y - 1][currentsquare.x ].parent = currentsquare
                    opensquares.append(maparray[currentsquare.y - 1][currentsquare.x ])

            if currentsquare.x > 0:
                if maparray[currentsquare.y - 1][currentsquare.x - 1].wall == 0:
                    if maparray[currentsquare.y ][currentsquare.x - 1].wall != 1 and maparray[currentsquare.y - 1][currentsquare.x ].wall != 1:
                        #print(maparray[currentsquare.y - 1][currentsquare.x - 1])
                        if maparray[currentsquare.y - 1][currentsquare.x - 1].f == -1 or maparray[currentsquare.y - 1][currentsquare.x - 1].f > (2 + currentsquare.f + maparray[currentsquare.y - 1][currentsquare.x - 1].g):
                            maparray[currentsquare.y - 1][currentsquare.x - 1].f = currentsquare.f + maparray[currentsquare.y - 1][currentsquare.x - 1].g
                            maparray[currentsquare.y - 1][currentsquare.x - 1].parent = currentsquare
                            opensquares.append(maparray[currentsquare.y - 1][currentsquare.x - 1])
            if currentsquare.x < len(maparray[0]) - 1:
                if maparray[currentsquare.y - 1][currentsquare.x + 1].wall == 0:
                    if maparray[currentsquare.y ][currentsquare.x + 1].wall != 1 and maparray[currentsquare.y - 1][currentsquare.x ].wall != 1:
                        #print(maparray[currentsquare.y - 1][currentsquare.x + 1].wall )
                        if maparray[currentsquare.y - 1][currentsquare.x + 1].f == -1 or maparray[currentsquare.y - 1][currentsquare.x + 1].f > (2 + currentsquare.f + maparray[currentsquare.y - 1][currentsquare.x + 1].g):
                            maparray[currentsquare.y - 1][currentsquare.x + 1].f = currentsquare.f + maparray[currentsquare.y - 1][currentsquare.x + 1].g
                            maparray[currentsquare.y - 1][currentsquare.x + 1].parent = currentsquare
                            opensquares.append(maparray[currentsquare.y - 1][currentsquare.x + 1])
        if currentsquare.y < len(maparray) - 1:
            if maparray[currentsquare.y + 1][currentsquare.x ].wall == 0:
                #print(maparray[currentsquare.y + 1][currentsquare.x ].wall)
                if maparray[currentsquare.y + 1 ][currentsquare.x ].f == -1 or maparray[currentsquare.y + 1][currentsquare.x ].f > (1 + currentsquare.f + maparray[currentsquare.y + 1][currentsquare.x ].g):
                    maparray[currentsquare.y + 1][currentsquare.x ].f = currentsquare.f + maparray[currentsquare.y + 1][currentsquare.x ].g
                    maparray[currentsquare.y + 1][currentsquare.x ].parent = currentsquare
                    opensquares.append(maparray[currentsquare.y + 1][currentsquare.x ])

                if currentsquare.x > 0:
                    if maparray[currentsquare.y + 1][currentsquare.x - 1].wall == 0:
                        if maparray[currentsquare.y ][currentsquare.x - 1].wall != 1 and maparray[currentsquare.y + 1][currentsquare.x ].wall != 1:
                            #print(maparray[currentsquare.y + 1][currentsquare.x - 1])
                            if maparray[currentsquare.y + 1][currentsquare.x - 1].f == -1 or maparray[currentsquare.y + 1][currentsquare.x - 1].f > (2 + currentsquare.f + maparray[currentsquare.y + 1][currentsquare.x - 1].g):
                                maparray[currentsquare.y + 1][currentsquare.x - 1].f = currentsquare.f + maparray[currentsquare.y + 1][currentsquare.x - 1].g
                                maparray[currentsquare.y + 1][currentsquare.x - 1].parent = currentsquare
                                opensquares.append(maparray[currentsquare.y + 1][currentsquare.x - 1])
                if currentsquare.x < len(maparray[0]) - 1:
                    if maparray[currentsquare.y + 1][currentsquare.x + 1].wall == 0:
                        if maparray[currentsquare.y ][currentsquare.x + 1].wall != 1 and maparray[currentsquare.y + 1][currentsquare.x ].wall != 1:
                            #print(maparray[currentsquare.y + 1][currentsquare.x + 1].wall )
                            if maparray[currentsquare.y + 1][currentsquare.x + 1].f == -1 or maparray[currentsquare.y + 1][currentsquare.x + 1].f > (2 + currentsquare.f + maparray[currentsquare.y + 1][currentsquare.x + 1].g):
                                maparray[currentsquare.y + 1][currentsquare.x + 1].f = currentsquare.f + maparray[currentsquare.y + 1][currentsquare.x + 1].g
                                maparray[currentsquare.y + 1][currentsquare.x + 1].parent = currentsquare
                                opensquares.append(maparray[currentsquare.y + 1][currentsquare.x + 1])

        if len(opensquares) > 0:
            currentsquare = opensquares[0]
            opensquares.remove(currentsquare)
        for el in opensquares:
            if el.f < currentsquare.f:
                currentsquare = el



    togoal = []
    current = currentsquare
    while current.position != start:
        togoal.append((current.y,current.x))
        # map2d[current.y][current.x] = 2
        current = current.parent
    # for el in map2d:
    #     print(el)
    pathlength = len(togoal) - 1
    returnpath = []
    while pathlength >= 0:
        returnpath.append(togoal[pathlength])
        pathlength = pathlength - 1

    return returnpath

def CheckLaserSection(laserdata):
    global wallfollow
    global forwardcone
    global forwardspeed
    global rotspeed
    global botposition
    global euler
    global hashistogram
    global currentpathnode
    global angleneeded
    global avoidspot
    global botposition

    movespeed = 1.0
    rotspeed = 0.2
    if hashistogram == False:
        count2 = 0
        newnode = (0,0)
        while count2 < 9:
            count = 0
            while count < 39:
                # if laserdata.ranges[count + (40 * count2)] < 2.5:
                forwardcone[count2] += laserdata.ranges[count + (40 * count2)]
                count = count + 1
            forwardcone[count2] = forwardcone[count2] / 40
            print("cone ",count2, " : ",forwardcone[count2])
            count2 = count2 + 1


        if forwardcone[4] <= 1.5 :
            hasangle = False
            if angleneeded > 1.5:
                if forwardcone[6] >= 2.0:
                    avoidspot = ((10 - botposition[1]) - 0.5, (9 + botposition[0]) + 0.5)
                elif forwardcone[3] >= 2.0:
                    avoidspot = ((10 - botposition[1]) - 0.5, (9 + botposition[0]) - 0.5)
                else:
                    avoidspot = ((10 - botposition[1]), (9 + botposition[0]) + 0.5)
            elif angleneeded > 0:
                if forwardcone[6] >= 2.0:
                    avoidspot = ((10 - botposition[1]) + 0.5, (9 + botposition[0]) )
                elif forwardcone[3] >= 2.0:
                    avoidspot = ((10 - botposition[1]) + 0.5, (9 + botposition[0]) - 0.5)
                else:
                    avoidspot = ((10 - botposition[1]) + 0.5, (9 + botposition[0]) - 0.5)
            elif angleneeded > -1.5:
                if forwardcone[6] >= 2.0:
                    avoidspot = ((10 - botposition[1]) + 0.5, (9 + botposition[0]) )
                elif forwardcone[3] >= 2.0:
                    avoidspot = ((10 - botposition[1]) + 0.5, (9 + botposition[0]) )
                else:
                    avoidspot = ((10 - botposition[1]) + 0.5, (9 + botposition[0]) - 0.5)
            else:
                if forwardcone[6] >= 2.0:
                    avoidspot = ((10 - botposition[1]) - 0.5, (9 + botposition[0]) )
                elif forwardcone[3] >= 2.0:
                    avoidspot = ((10 - botposition[1]) + 0.5, (9 + botposition[0]) + 0.5 )
                else:
                    avoidspot = ((10 - botposition[1]) + 0.5, (9 + botposition[0]) + 0.5)

        hashistogram = True



def quattest(data):
    global forwardspeed
    global rotspeed
    global astarpath
    global avoidspot
    print(astarpath[0][0])
    quaternion = [data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w]
    euler = transform.euler_from_quaternion(quaternion)
    print(euler)
    # print(quat_msg)
    if forwardcone[4] > 2.9 and forwardcone[9] > 2.9 and forwardcone[10] > 2.9:
        forwardspeed = 1.0
        rotspeed = 0
    if forwardcone[4] > 2.0 and forwardcone[9] > 2.2 and forwardcone[10] > 2.2:
        forwardspeed = 0.3
        rotspeed = 0
    else:
        rotspeed = -1.0
    if euler > 1:
        pub.publish(Vector3(0.1,0,0),Vector3(0,0,0.1))
    else:
        pub.publish(Vector3(0,0,0),Vector3(0,0,0.4))




def getangle(data):
    global avoidspot
    global forwardspeed
    global rotspeed
    global astarpath
    global currentpathnode
    global avoidspot
    global hasangle
    global euler
    global hashistogram
    global angleneeded
    global botposition
    # botposition = (data.pose.pose.orientation.x,data.pose.pose.orientation.y,0)
    if hasangle == False:

        quaternion = [data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w]
        euler = transform.euler_from_quaternion(quaternion)


        angleneeded = 0.0

        if astarpath[(currentpathnode + 1)][1] + 0.5 == round(9 + data.pose.pose.position.x,1):
            if ( astarpath[(currentpathnode + 1)][0] + 0.5)  <  round(10 - data.pose.pose.position.y,1):
                angleneeded = 1.5
            else:
                angleneeded = -1.5# else:
    #     progress(data)
        elif astarpath[(currentpathnode + 1)][1] + 0.5  > (9 + data.pose.pose.position.x):
            if ( astarpath[(currentpathnode + 1)][0] + 0.5)  ==  round(10 - data.pose.pose.position.y,1):
                angleneeded = 0.0
            elif ( astarpath[(currentpathnode + 1)][0] + 0.5)  <  round(10 - data.pose.pose.position.y,1):
                angleneeded = 0.75
            else:
                angleneeded = -0.75
        else:#if astarpath[currentpathnode][0] < (9 + data.pose.pose.position.x):
            if ( astarpath[(currentpathnode + 1)][0] + 0.5)  == round( 10 - data.pose.pose.position.y,1):
                angleneeded = 2.9
            elif ( astarpath[(currentpathnode + 1)][0] + 0.5)  < round( 10 - data.pose.pose.position.y,1):
                angleneeded = 2.25
            else:
                angleneeded = -2.25

        if math.fabs(euler[2] - angleneeded) > 0.15:
            rotspeed = math.fabs(math.fabs(euler[2] - angleneeded))
            if euler[2] < 3.0 and euler[2] > 0:
                if euler[2] < angleneeded:
                    pub.publish(Vector3(0,0,0),Vector3(0,0,rotspeed))
                else:
                    pub.publish(Vector3(0,0,0),Vector3(0,0,-rotspeed))
            else:
                if euler[2] < angleneeded:
                    pub.publish(Vector3(0,0,0),Vector3(0,0,rotspeed))
                else:
                    pub.publish(Vector3(0,0,0),Vector3(0,0,-rotspeed))
        else:
            hashistogram = False
            hasangle = True
    else:
        gethistogram(data)

def gethistogram(data):
    global avoidspot
    global angleneeded
    global hashistogram
    global currentpathnode
    # print("histo gram")
    if hashistogram == True:
        progress(data)
    else:
        rospy.Subscriber('base_scan', LaserScan, CheckLaserSection)

def avoidprogress(data):
    global avoidspot
    global angleneeded
    global hasangle
    global currentpathnode
    global euler
    global hashistogram
    global lastcheckpoint
    disttonextnode = math.fabs(avoidspot[1] -  (9 + data.pose.pose.position.x)) + math.fabs(( avoidspot[0]) -  (10 - data.pose.pose.position.y))
    disttolastnode = math.fabs(lastcheckpoint[1] -  (9 + data.pose.pose.position.x)) + math.fabs(( lastcheckpoint[0]) -  (10 - data.pose.pose.position.y))
    if disttonextnode <= 0.05:
        avoidspot = (0,0)
        hasangle = False
        print(data.pose.pose.position.x + 9)
        print(10 - data.pose.pose.positioon.y)
        # currentpathnode = currentpathnode + 1
        # print(currentpathnode)
        print(astarpath[currentpathnode] )
        hashistogram = False
        print( euler[2])

    if hasangle == True:
        pub.publish(Vector3(0.45,0,0),Vector3(0,0,0))
        if disttolastnode >= 1.5:
            # pub.publish(Vector3(-0.55,0,0),Vector3(0,0,0))
            hasangle = False
            print("far from last checkpoint: ", astarpath[currentpathnode] )
            hashistogram = False

def progress(data):
    global avoidspot
    global angleneeded
    global hasangle
    global currentpathnode
    global euler
    global hashistogram
    global lastcheckpoint
    global botposition
    # botposition = (data.pose.pose.orientation.x,data.pose.pose.orientation.y,0)
    disttonextnode = math.fabs((astarpath[(currentpathnode + 1)][1] + 0.5) -  (9 + data.pose.pose.position.x)) + math.fabs(( astarpath[(currentpathnode + 1)][0] + 0.5) -  (10 - data.pose.pose.position.y))
    disttolastnode = math.fabs(lastcheckpoint[1] -  (9 + data.pose.pose.position.x)) + math.fabs(( lastcheckpoint[0]) -  (10 - data.pose.pose.position.y))
    if disttonextnode <= 0.15:
        lastcheckpoint = (astarpath[currentpathnode][0],astarpath[currentpathnode][1])
        hasangle = False
        print(data.pose.pose.position.x + 9)
        print(10 - data.pose.pose.position.y)
        currentpathnode = currentpathnode + 1
        # print(currentpathnode)
        print(astarpath[currentpathnode] )
        hashistogram = False
        print( euler[2])
    else:
        pub.publish(Vector3(0.45,0,0),Vector3(0,0,0))
    if disttolastnode >= 1.15:
        lastcheckpoint = (botposition[1],botposition[0])
        hasangle = False

        print("far from last checkpoint" )
        hashistogram = False



def goalapproach(data):
    global avoidspot
    global forwardspeed
    global rotspeed
    global astarpath
    global currentpathnode
    global avoidspot
    global hasangle
    global euler
    global hashistogram
    global angleneeded
    global botposition
    # botposition = (data.pose.pose.orientation.x,data.pose.pose.orientation.y,0)


    quaternion = [data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w]
    euler = transform.euler_from_quaternion(quaternion)
    disttonextnode = math.fabs((astarpath[((len(astarpath) - 1) )][1] + 0.5) -  (9 + data.pose.pose.position.x)) + math.fabs(( astarpath[((len(astarpath) - 1) )][0] + 0.5) -  (10 - data.pose.pose.position.y))

    angleneeded = 0.0
    if disttonextnode > 0.15:
        if astarpath[((len(astarpath) - 1) )][1] + 0.5 == round(9 + data.pose.pose.position.x,1):
            if ( astarpath[((len(astarpath) - 1) )][0] + 0.5)  <  round(10 - data.pose.pose.position.y,1):
                angleneeded = 1.5
            else:
                angleneeded = -1.5# else:
    #     progress(data)
        elif astarpath[((len(astarpath) - 1) )][1] + 0.5  > (9 + data.pose.pose.position.x):
            if ( astarpath[((len(astarpath) - 1) )][0] + 0.5)  ==  round(10 - data.pose.pose.position.y,1):
                angleneeded = 0.0
            elif ( astarpath[((len(astarpath) - 1) )][0] + 0.5)  <  round(10 - data.pose.pose.position.y,1):
                angleneeded = 0.75
            else:
                angleneeded = -0.75
        else:#if astarpath[currentpathnode][0] < (9 + data.pose.pose.position.x):
            if ( astarpath[((len(astarpath) - 1) )][0] + 0.5)  == round( 10 - data.pose.pose.position.y,1):
                angleneeded = 2.9
            elif ( astarpath[((len(astarpath) - 1) )][0] + 0.5)  < round( 10 - data.pose.pose.position.y,1):
                angleneeded = 2.25
            else:
                angleneeded = -2.25

        if math.fabs(euler[2] - angleneeded) > 0.15:
            rotspeed = math.fabs(math.fabs(euler[2] - angleneeded))
            if euler[2] < 3.0 and euler[2] > 0:
                if euler[2] < angleneeded:
                    pub.publish(Vector3(0,0,0),Vector3(0,0,rotspeed))
                else:
                    pub.publish(Vector3(0,0,0),Vector3(0,0,-rotspeed))
            else:
                if euler[2] < angleneeded:
                    pub.publish(Vector3(0,0,0),Vector3(0,0,rotspeed))
                else:
                    pub.publish(Vector3(0,0,0),Vector3(0,0,-rotspeed))
        else:
            pub.publish(Vector3(0.1,0,0),Vector3(0,0,0))
    else:
        print("I'm Home")
        pub.publish(Vector3(0,0,0),Vector3(0,0,2.3))



def astartest(data):
    global angleneeded
    global forwardspeed
    global rotspeed
    global astarpath
    global currentpathnode
    global avoidspot
    global hasangle
    global euler
    global botposition
    if len(astarpath) <= 0:
        goalx = 1
        goaly = 1
        goalx = rospy.get_param("goalx")
        goaly = rospy.get_param("goaly")
        print("goal:" ,goalx,goaly)
        startx = 0
        starty = 0
        startx = int(data.pose.pose.position.x)
        starty = int(data.pose.pose.position.y)
        print("start:" ,startx,starty)
        astarpath = astar(int(goaly),int(goalx),starty,startx);
    else:
        botposition = (data.pose.pose.orientation.x,data.pose.pose.orientation.y,0)
        quaternion = [data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w]
        euler = transform.euler_from_quaternion(quaternion)
        # disttogoal = math.fabs((astarpath[(len(astarpath) - 1 )][1] + 0.5) -  (9 + data.pose.pose.position.x)) + math.fabs(( astarpath[(len(astarpath) - 1 )][0] + 0.5) -  (10 - data.pose.pose.position.y))

        # if disttogoal < 0.6:
        #     currentpathnode = len(astarpath) - 1
        if currentpathnode < (len(astarpath) - 1):
            getangle(data)
        else:
            goalapproach(data)







# get bot world space
def SetBotIntialPosition(data):
    global botset
    global botposition
    print(data.pose.pose.position.x)
    print(data.pose.pose.position.y)
    botposition =  (data.pose.pose.position.x,data.pose.pose.position.y,0)
    botset = True

# be a cylon
def astartoaster():
    rospy.init_node('astar_toaster', anonymous=False)
    rate = rospy.Rate(1) # 10hz
    global pub
    global goalset
    global botset
    global forwardcone
    global forwardspeed
    global rotspeed
    global hashistogram
    goalposition = Vector3(0,0,0)
    botposition = Vector3(0,0,0)
    global astarpath
    # rospy.set_param('goalx', 11.0)
    # rospy.set_param('goaly', 1.0)

    hashistogram = True;
    hasangle = False
    while not rospy.is_shutdown():

        rospy.Subscriber('base_pose_ground_truth', Odometry, astartest)

        rate.sleep()


if __name__ == '__main__':
    try:
        astartoaster()
    except rospy.ROSInterruptException:
        pass
#UBIT: Dvdonato
#Daniel Donato
