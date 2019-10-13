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
forwardspeed = 0.0
rotspeed = 0.0
astarpath = []
avoidspot = (0,0)
currentpathnode = 1
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
    forwardcone[0] = (laserdata.ranges[1] + laserdata.ranges[35] + laserdata.ranges[45] + laserdata.ranges[55]) / 4
    forwardcone[1] = (lasglobalerdata.ranges[95] + laserdata.ranges[80] + laserdata.ranges[70] + laserdata.ranges[60] ) / 4
    forwardcone[2] = math.fabs(laserdata.ranges[125] + laserdata.ranges[120] + laserdata.ranges[110] + laserdata.ranges[100] ) / 4
    # narrowleft forward
    forwardcone[3] = (laserdata.ranges[130] +  laserdata.ranges[135] + laserdata.ranges[140] +  laserdata.ranges[145] + laserdata.ranges[149]) / 5
    forwardcone[9] = (laserdata.ranges[145] + laserdata.ranges[150] +  laserdata.ranges[160] + laserdata.ranges[162] +  laserdata.ranges[165] + laserdata.ranges[168]) / 6



    forwardcone[4] = (laserdata.ranges[165] +  laserdata.ranges[175] + laserdata.ranges[170] +  laserdata.ranges[177] + laserdata.ranges[180] + laserdata.ranges[195] +  laserdata.ranges[185] + laserdata.ranges[190] + laserdata.ranges[187]) / 9
    # narrowright forward
    forwardcone[5] = (laserdata.ranges[211] +  laserdata.ranges[220] + laserdata.ranges[225] +  laserdata.ranges[230] + laserdata.ranges[235]) / 5
    forwardcone[10] = (laserdata.ranges[210] +  laserdata.ranges[205] + laserdata.ranges[195] + laserdata.ranges[192]) / 4

    forwardcone[6] = (laserdata.ranges[236] + laserdata.ranges[240] + laserdata.ranges[250] + laserdata.ranges[260]) / 4
    forwardcone[7] = (laserdata.ranges[270] + laserdata.ranges[280] + laserdata.ranges[290] + laserdata.ranges[310]) / 4
    forwardcone[8] = (laserdata.ranges[315] + laserdata.ranges[325] + laserdata.ranges[345] + laserdata.ranges[359]) / 4


    if WallFollow == True:
        WallFollow()
    else:
        AvoidObstablesAndFollowWall()

        # safety check against colliding
    if forwardcone[4] < 1.4 or forwardcone[9] < 1.4 or forwardcone[10] < 1.4:
        forwardspeed = 0
    if forwardspeed == 0 and rotspeed == 0:
        print("default")
        rotspeed = -0.1

    if math.fabs(botposition[0] - goalposition[0]) < 0.5 and math.fabs(botposition[1] - goalposition[1]) < 0.5:
        print("I'm home, now close the door and let me make toast")

    else:
        pub.publish(Vector3(forwardspeed,0,0),Vector3(0,0,rotspeed))


def quattest(data):
    global forwardspeed
    global rotspeedhashistogram = False
    global astarpath
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
def getangle(data):
    global forwardspeed
    global rotspeed
    global astarpath
    global currentpathnode
    global avoidspot
    global hasangle
    global euler
    global hashistogram
    if hasangle == False:
        quaternion = [data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w]
        euler = transform.euler_from_quaternion(quaternion)


        angleneeded = 0.0

        if astarpath[(currentpathnode + 1)][1]  == round(9 + data.pose.pose.position.x):
            if ( astarpath[(currentpathnode + 1)][0])  <  round(10 - data.pose.pose.position.y):
                angleneeded = 1.5
            else:
                angleneeded = -1.5
        elif astarpath[(currentpathnode + 1)][1]  > (9 + data.pose.pose.position.x):
            if ( astarpath[(currentpathnode + 1)][0])  ==  round(10 - data.pose.pose.position.y):
                angleneeded = 0.0
            elif ( astarpath[(currentpathnode + 1)][0])  <  round(10 - data.pose.pose.position.y):
                angleneeded = 0.75
            else:
                angleneeded = -0.75
        else:#if astarpath[currentpathnode][0] < (9 + data.pose.pose.position.x):
            if ( astarpath[(currentpathnode + 1)][0])  == round( 10 - data.pose.pose.position.y):
                angleneeded = 2.9
            elif ( astarpath[(currentpathnode + 1)][0])  < round( 10 - data.pose.pose.position.y):
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

def gethistogram(data):
    global hashistogram
    if hashistogram == False:
        rospy.Subscriber('base_scan', LaserScan, CheckLaserSection)
    else:
        progress(data)

def progress(data):
    global hasangle
    global currentpathnode
    global euler
    global hashistogram
    disttonextnode = math.fabs(astarpath[(currentpathnode + 1)][1] -  (9 + data.pose.pose.position.x)) + math.fabs(( astarpath[(currentpathnode + 1)][0]) -  (10 - data.pose.pose.position.y))
    disttocurrentnode = math.fabs(astarpath[(currentpathnode )][1] -  (9 + data.pose.pose.position.x)) + math.fabs(( astarpath[(currentpathnode )][0]) -  (10 - data.pose.pose.position.y))
    if disttonextnode <= 0.5:
        hasangle = False
        print(data.pose.pose.position.x + 9)
        print(10 - data.pose.pose.position.y)
        currentpathnode = currentpathnode + 1
        # print(currentpathnode)
        print(astarpath[currentpathnode] )

        print( euler[2])
    if hasangle == True:
        pub.publish(Vector3(1.25,0,0),Vector3(0,0,0))

def goalapproach():
    angleneeded = 0.0

    if astarpath[(currentpathnode )][1] + 0.5  == round(9 + data.pose.pose.position.x,1):
        if ( astarpath[(currentpathnode + 1)][0]) + 0.5  <  round(10 - data.pose.pose.position.y,1):
            angleneeded = 1.5
        else:
            angleneeded = -1.5
    elif astarpath[(currentpathnode )][1] + 0.5 > (9 + data.pose.pose.position.x):
        if ( astarpath[(currentpathnode )][0]) + 0.5  ==  round(10 - data.pose.pose.position.y,1):
            angleneeded = 0.0
        elif ( astarpath[(currentpathnode )][0]) + 0.5  <  round(10 - data.pose.pose.position.y,1):
            angleneeded = 0.75
        else:
            angleneeded = -0.75
    else:#if astarpath[currentpathnode][0] < (9 + data.pose.pose.position.x):
        if ( astarpath[(currentpathnode )][0]) + 0.5 == round( 10 - data.pose.pose.position.y,1):
            angleneeded = 2.9
        elif ( astarpath[(currentpathnode )][0]) + 0.5 < round( 10 - data.pose.pose.position.y,1):
            angleneeded = 2.25
        else:
            angleneeded = -2.25
    # print( euler[2])
    # print( angleneeded)
    # print( astarpath[currentpathnode])
    # print( astarpath[currentpathnode + 1])
    if math.fabs(euler[2] - angleneeded) > 0.2:
        pub.publish(Vector3(0,0,0),Vector3(0,0,1.15))
    else:
        pub.publish(Vector3(1.25,0,0),Vector3(0,0,0))


def astartest(data):
    global forwardspeed
    global rotspeed
    global astarpath
    global currentpathnode
    global avoidspot
    global hasangle
    global euler
    quaternion = [data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w]
    euler = transform.euler_from_quaternion(quaternion)

    if currentpathnode < (len(astarpath) - 1):
        if avoidspot == (0,0):
            getangle(data)
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
                #     else:
                #         angleneeded = -2.25
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
    else:
        goalapproach();






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
    rate = rospy.Rate(10) # 10hz
    global pub
    global goalset
    global botset
    global forwardcone
    global forwardspeed
    global rotspeed
    goalposition = Vector3(0,0,0)
    botposition = Vector3(0,0,0)
    global astarpath
    astarpath = astar.mainx();
    while not rospy.is_shutdown():
        # negative rotation is right
        rospy.Subscriber('base_pose_ground_truth', Odometry, astartest)
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
