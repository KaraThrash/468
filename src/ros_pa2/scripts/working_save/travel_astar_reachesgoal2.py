#!/usr/bin/env python
import rospy
import math
import astar
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist,Vector3
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
import tf.transformations as transform

pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
goalposition = Vector3(0,0,0)
botposition = Vector3(0,0,0)
goalset = False
botset = False
wallfollow = False
wallfollowleft = False
forwardcone = [0,0,0,0,0,0,0,0,0,0,0]
histogram = [[0,0,0],[0,0,0],[0,0,0]]
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
        # else:
            # avoidspot = (0,0)
            # if ((10 - botposition[1]) - astarpath[currentpathnode + 1][0]) < 0:
            #     if ((9 + botposition.x) - astarpath[currentpathnode + 1][1]) < 0:
            #         newnode = (astarpath[currentpathnode + 1][0] + 0.5, astarpath[currentpathnode + 1][1] - 0.5)
            #     else:
            #         newnode = (astarpath[currentpathnode + 1][0] + 0.5, astarpath[currentpathnode + 1][1] + 0.5)
            # else:
            #     if ((9 + botposition.x) - astarpath[currentpathnode + 1][1]) < 0:
            #         newnode = (astarpath[currentpathnode + 1][0] - 0.5, astarpath[currentpathnode + 1][1] - 0.5)
            #     else:
            #         newnode = (astarpath[currentpathnode + 1][0] - 0.5, astarpath[currentpathnode + 1][1] + 0.5)
        # newnode = ((astarpath[currentpathnode + 1][1]) + (astarpath[currentpathnode + 1][1] - (10 - botposition[1])),(astarpath[currentpathnode + 1][0]) + (astarpath[currentpathnode + 1][0] - (9 + botposition.x)))
        print("avoidspot: ",avoidspot)
        # avoidspot = (botposition[1],botposition.x)

        # astarpath.insert(currentpathnode + 1, newnode)
        hashistogram = True
        #
        # if forwardcone[3] < forwardcone[6] < 2.9:
        #     astarpath.insert(currentpathnode + 1, element)
        # else:
        #     astarpath.insert(currentpathnode + 1, element)


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



# def avoid():
def avoidgetangle(data):
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
    if hasangle == False:
        avoidspot = (0,0)
        quaternion = [data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w]
        euler = transform.euler_from_quaternion(quaternion)


        angleneeded = 0.0

        if avoidspot[1]  == round(9 + data.pose.pose.position.x,1):
            if ( avoidspot[0])  <  round(10 - data.pose.pose.position.y,1):
                angleneeded = 1.5
            else:
                angleneeded = -1.5# else:
    #     progress(data)
        elif avoidspot[1]  > (9 + data.pose.pose.position.x):
            if ( avoidspot[0])  ==  round(10 - data.pose.pose.position.y,1):
                angleneeded = 0.0
            elif ( avoidspot[0])  <  round(10 - data.pose.pose.position.y,1):
                angleneeded = 0.75
            else:
                angleneeded = -0.75
        else:#if astarpath[currentpathnode][0] < (9 + data.pose.pose.position.x):
            if ( avoidspot[0])  == round( 10 - data.pose.pose.position.y,1):
                angleneeded = 2.9
            elif ( avoidspot[0])  < round( 10 - data.pose.pose.position.y,1):
                angleneeded = 2.25
            else:
                angleneeded = -2.25

        if math.fabs(euler[2] - angleneeded) > 0.05:
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
        # if avoidspot == (0,0):
        #     progress(data)
        # else:
        #     avoidprogress(data)
    else:
        rospy.Subscriber('base_scan', LaserScan, CheckLaserSection)
        # if avoidspot == (0,0):
        #     progress(data)
        # else:
        #     avoidprogress(data)

        # print("this shouldnt happen")
        # rospy.Subscriber('base_scan', LaserScan, CheckLaserSection)
    # else:
    #     progress(data)
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
        if math.fabs((astarpath[(currentpathnode )][1] + 0.5) -  (9 + data.pose.pose.position.x)) + math.fabs(( astarpath[(currentpathnode )][0] + 0.5) -  (10 - data.pose.pose.position.y)) < 1:
            currentpathnode = len(astarpath ) - 1
        else:
            pub.publish(Vector3(0.45,0,0),Vector3(0,0,0))
    if math.fabs((astarpath[(len(astarpath ) - 1 )][1] + 0.5) -  (9 + data.pose.pose.position.x)) + math.fabs(( astarpath[(len(astarpath ) - 1 )][0] + 0.5) -  (10 - data.pose.pose.position.y)) < 1:
        currentpathnode = len(astarpath ) - 1
    if disttolastnode >= 1.15:
        lastcheckpoint = (botposition[1],botposition[0])
        hasangle = False

        print("far from last checkpoint" )
        hashistogram = False





        # if disttolastnode >= 1.5:
        #     # pub.publish(Vector3(-0.55,0,0),Vector3(0,0,0))
        #     hasangle = False
        #     print("far from last checkpoint: ", astarpath[currentpathnode] )
        #     hashistogram = False
        # else:
        #     pub.publish(Vector3(0,0,0),Vector3(0,0,0.1))


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
    disttonextnode = math.fabs((astarpath[(currentpathnode )][1] + 0.5) -  (9 + data.pose.pose.position.x)) + math.fabs(( astarpath[(currentpathnode )][0] + 0.5) -  (10 - data.pose.pose.position.y))

    angleneeded = 0.0
    if disttonextnode > 0.05:
        if astarpath[(currentpathnode )][1] + 0.5 == round(9 + data.pose.pose.position.x,1):
            if ( astarpath[(currentpathnode )][0] + 0.5)  <  round(10 - data.pose.pose.position.y,1):
                angleneeded = 1.5
            else:
                angleneeded = -1.5# else:
    #     progress(data)
        elif astarpath[(currentpathnode )][1] + 0.5  > (9 + data.pose.pose.position.x):
            if ( astarpath[(currentpathnode )][0] + 0.5)  ==  round(10 - data.pose.pose.position.y,1):
                angleneeded = 0.0
            elif ( astarpath[(currentpathnode )][0] + 0.5)  <  round(10 - data.pose.pose.position.y,1):
                angleneeded = 0.75
            else:
                angleneeded = -0.75
        else:#if astarpath[currentpathnode][0] < (9 + data.pose.pose.position.x):
            if ( astarpath[(currentpathnode )][0] + 0.5)  == round( 10 - data.pose.pose.position.y,1):
                angleneeded = 2.9
            elif ( astarpath[(currentpathnode )][0] + 0.5)  < round( 10 - data.pose.pose.position.y,1):
                angleneeded = 2.25
            else:
                angleneeded = -2.25

        if math.fabs(euler[2] - angleneeded) > 0.05:
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
            pub.publish(Vector3(1.0,0,0),Vector3(0,0,0))
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
    botposition = (data.pose.pose.orientation.x,data.pose.pose.orientation.y,0)
    quaternion = [data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w]
    euler = transform.euler_from_quaternion(quaternion)

    if currentpathnode < (len(astarpath) - 1):
        getangle(data)
    else:
        goalapproach(data)
        # if avoidspot == (0,0):
        #     getangle(data)
        # else:
        #     avoidgetangle(data)
            # else:
                #
                #
                # angleneeded = 0.0
                #
                # if astarpath[(currentpathnode + 1)][1]  == round(9 + data.pose.pose.position.x,1):
                #     if ( astarpath[(currentpathnode + 1)][0])  <  round(10 - data.pose.pose.position.y,1):
                #         angleneeded = 1.5
                #     else:
                #         angleneeded = -1.5
                # elif astarpath[(currentpathnode + 1)][1]  > (9 + data.pose.pose.position.x):
                #     if ( astarpath[(currentpathnode + 1)][0])  ==  round(10 - data.pose.pose.position.y,1):
                #         angleneeded = 0.0
                #     elif ( astarpath[(currentpathnode + 1)][0])  <  round(10 - data.pose.pose.position.y,1):
                #         angleneeded = 0.75
                #     else:
                #         angleneeded = -0.75
                # else:#if astarpath[currentpathnode][0] < (9 + data.pose.pose.position.x):
                #     if ( astarpath[(currentpathnode + 1)][0])  == round( 10 - data.pose.pose.position.y,1):
                #         angleneeded = 2.9
                #     elif ( astarpath[(currentpathnode + 1)][0])  < round( 10 - data.pose.pose.position.y,1):
                #         angleneeded = 2.25
                #     else:movespd
                #         angleneeded = -2.25    else:
            # progress(data)
                # # print( euler[2])
                # # print( angleneeded)
                # # print( astarpath[currentpathnode])
                # # print( astarpath[currentpathnode + 1])
                # disttocurrentnode = math.fabs(astarpath[(currentpathnode )][1] -  (9 + data.pose.pose.position.x)) + math.fabs(( astarpath[(currentpathnode )][0]) -  (10 - data.pose.pose.position.y))
                # disttoavoidspot = math.fabs(avoidspot[0] -  (9 + data.pose.pose.position.x)) + math.fabs(( avoidspot[1]) -  (10 - data.pose.pose.position.y))
                # if disttonextnode > disttocurrentnode:
                #     avoidspot = (0,0)
                # if math.fabs(euler[2] - angleneeded) > 0.05:
                #     rotspeed = math.fabs(math.fabs(euler[2] - angleneeded))
                #     if euler[2] < 3.0 and euler[2] > 0:
                #         if euler[2] < angleneeded:
                #             pub.publish(Vector3(0,0,0),Vector3(0,0,rotspeed))
                #         else:
                #             pub.publish(Vector3(0,0,0),Vector3(0,0,-rotspeed))
                #     else:
                #         if euler[2] < angleneeded:
                #             pub.publish(Vector3(0,0,0),Vector3(0,0,-rotspeed))
                #         else:
                #             pub.publish(Vector3(0,0,0),Vector3(0,0,rotspeed))
                # else:
                    # if waitforlaserdata == True:
                    #
                    # else:
                    # pub.publish(Vector3(1.25,0,0),Vector3(0,0,0))
    # else:
        # goalapproach();






# get bot world space
def SetBotIntialPosition(data):
    global botset
    global botposition
    print(data.pose.pose.position.x)
    print(data.pose.pose.position.y)
    botposition =  (data.pose.pose.position.x,data.pose.pose.position.y,0)
    botset = True

# be a cylon
def rotater():
    rospy.init_node('my_rotater', anonymous=False)
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
    astarpath = astar.mainx();
    hashistogram = True;
    hasangle = False
    while not rospy.is_shutdown():
        # negative rotation is right
        rospy.Subscriber('base_pose_ground_truth', Odometry, astartest)
        # if hashistogram == True:
        #     rospy.Subscriber('base_pose_ground_truth', Odometry, astartest)
        # else:
        #     rospy.Subscriber('base_scan', LaserScan, CheckLaserSection)
        # if botset == False:
        #     rospy.Subscriber('base_pose_ground_truth', Odometry, SetBotIntialPosition)
        # else:
        #     rospy.Subscriber('base_pose_ground_truth', Odometry, astartest)
        rate.sleep()


if __name__ == '__main__':
    try:
        rotater()
    except rospy.ROSInterruptException:
        pass
#UBIT: Dvdonato
#Daniel Donato
