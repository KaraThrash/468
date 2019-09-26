#!/usr/bin/env python
import rospy
import math
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist,Vector3
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
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
# positive is left
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'bot x - signal x %s', str(robotpos[0] - data.pose.position.x))

def callbackmove(data):
    robotpos = (data.pose.pose.position.x,data.pose.pose.position.y,data.pose.pose.position.z)
    #rospy.Subscriber('homing_signal', PoseStamped, callback)
    rospy.loginfo(rospy.get_caller_id() + 'test heard %s', str(data.pose.pose.position.y))

# def CheckLaserSection(laserdata):
#     global pub
#     rospy.loginfo(rospy.get_caller_id() + 'test heard %s', str(laserdata.intensities[180]))
#     if laserdata.intensities[160] < 1 and laserdata.intensities[205] < 1 and laserdata.intensities[180] < 1:
#         pub.publish(Vector3(1.1,0,0),Vector3(0,0,0))
#     else:
#         pub.publish(Vector3(0,0,0),Vector3(0,0,0.5))

def CheckLaserSection(laserdata):
    global wallfollow
    global forwardcone
    global forwardspeed
    global rotspeed
    forwardcone[0] = (laserdata.ranges[1] + laserdata.ranges[35] + laserdata.ranges[45] + laserdata.ranges[55]) / 4
    forwardcone[1] = (laserdata.ranges[95] + laserdata.ranges[80] + laserdata.ranges[70] + laserdata.ranges[60] ) / 4
    forwardcone[2] = (laserdata.ranges[125] + laserdata.ranges[120] + laserdata.ranges[110] + laserdata.ranges[100] ) / 4
    # narrowleft forward
    forwardcone[3] = (laserdata.ranges[130] +  laserdata.ranges[135] + laserdata.ranges[140] +  laserdata.ranges[145] + laserdata.ranges[149]) / 5
    forwardcone[9] = (laserdata.ranges[150] +  laserdata.ranges[160] + laserdata.ranges[162] +  laserdata.ranges[165] + laserdata.ranges[168]) / 5



    forwardcone[4] = (laserdata.ranges[170] +  laserdata.ranges[175] + laserdata.ranges[170] +  laserdata.ranges[177] + laserdata.ranges[180] + laserdata.ranges[182] +  laserdata.ranges[185] + laserdata.ranges[190] + laserdata.ranges[187]) / 9
    # narrowright forward
    forwardcone[5] = (laserdata.ranges[211] +  laserdata.ranges[220] + laserdata.ranges[225] +  laserdata.ranges[230] + laserdata.ranges[235]) / 5
    forwardcone[10] = (laserdata.ranges[202] +  laserdata.ranges[205] + laserdata.ranges[195] + laserdata.ranges[192]) / 4

    forwardcone[6] = (laserdata.ranges[236] + laserdata.ranges[240] + laserdata.ranges[250] + laserdata.ranges[260]) / 4
    forwardcone[7] = (laserdata.ranges[270] + laserdata.ranges[280] + laserdata.ranges[290] + laserdata.ranges[310]) / 4
    forwardcone[8] = (laserdata.ranges[315] + laserdata.ranges[325] + laserdata.ranges[345] + laserdata.ranges[359]) / 4

    # forwardcone[0] = int(forwardcone[0])
    # forwardcone[1] = int(forwardcone[1])
    # forwardcone[2] = int(forwardcone[2])
    # forwardcone[3] = int(forwardcone[3])
    # forwardcone[4] = int(forwardcone[4])

    if WallFollow == True:
        WallFollow()
    else:
        AvoidObstablesAndFollowWall()

        # safety check against colliding
    if forwardcone[4] < 1.4 :
        forwardspeed = 0
    if forwardspeed == 0 and rotspeed == 0:
        print("default")
        rotspeed = -0.1

    if math.fabs(botposition[0] - goalposition[0]) < 0.5 and math.fabs(botposition[1] - goalposition[1]) < 0.5:
        print("I'm home, now close the door and let me make toast")
    else:
        pub.publish(Vector3(forwardspeed,0,0),Vector3(0,0,rotspeed))
    # if forwardcone[2] > 2.9:
    #     forwardspeed = 1.0
    #     rotspeed = 0
    # elif forwardcone[3] < forwardcone[3]:
    #     WallFollow = True
    #     forwardspeed = 0
    #     rotspeed = 1.0
    # else:
    #     WallFollowLeft = True
    #     WallFollow = False
    #     forwardspeed = 0
    #     rotspeed = -1.0
    #         # if wallfollowleft == False:
    #         #     wallfollow = True5
    #
    #     # if wallfollowleft == False:
    #         # wallfollow = True
    #     forwardspeed = 0
    # # rospy.loginfo(rospy.get_caller_id() + 'CheckLaserSection %s', str(laserdata.ranges[180]))
    #
    #
    # if wallfollow == True:
    #     WallFollow(laserdata)
    # elif wallfollowleft == True:
    #     WallFollowLeft(laserdata)
    # else:
    #     GoalSeek(laserdata)
    #botposition
    #
    # rospy.loginfo(rospy.get_caller_id() + 'forward and rot speed:  %s', str(forwardspeed) + " : "+ str(rotspeed))
    # pub.publish(Vector3(forwardspeed,0,0),Vector3(0,0,rotspeed))


def JustAvoidObstables():
    global forwardcone
    global forwardspeed
    global rotspeed
    if forwardcone[4] > 2.9 and forwardcone[9] > 2.9 and forwardcone[10] > 2.9:
        forwardspeed = 1.0
        rotspeed = 0
    if forwardcone[4] > 2.0 and forwardcone[9] > 2.2 and forwardcone[10] > 2.2:
        forwardspeed = 0.3
        rotspeed = 0
    else:
        rotspeed = -1.0
    pub.publish(Vector3(forwardspeed,0,0),Vector3(0,0,rotspeed))

def AvoidObstablesAndFollowWall():
    global forwardcone
    global forwardspeed
    global rotspeed5
    forwardspeed = 0
    rotspeed = 0
    print("avoid")
    if forwardcone[4] > 1.8 :
        if forwardcone[9] < 1.5:
            rotspeed = 0.3
        elif forwardcone[10] < 1.5:
            wallfollow = True
            rotspeed = -0.2
        else:
           forwardspeed = 1.0
    elif forwardcone[6] < 1.5:
        wallfollow = True
    else:
        rotspeed = -1.0
        #
        #
        # if forwardcone[3] > 2.0 and forwardcone[5] > 2.0:
        #     forwardspeed = 0.2
        #     rotspeed = 0
        # elif forwardcone[3] < 2.0 :
        #     forwardspeed = 0
        #     rotspeed = -0.5
        # elif forwardcone[2] < 2.0 :
        #     forwardspeed = 0
        #     rotspeed = 0.5
        # elif forwardcone[7] > 1.5 :
        #     forwardspeed = 0
        #     rotspeed = -0.5
        # elif forwardcone[6] > 1.5 :
        #     forwardspeed = 0
        #     rotspeed = -0.5
        # elif forwardcone[2] > 1.5 :
        #     forwardspeed = 0
        #     rotspeed = 0.5
        # else:
        #     print("backup")
        #     forwardspeed = -0.1
        #     rotspeed = 0.2






def AvoidObstablesAndSmartTurn():
    forwardspeed = 0
    rotspeed = 0
    global forwardcone
    global forwardspeed
    global rotspeed
    if forwardcone[4] > 2.9  and forwardcone[9] > 2.9:
        forwardspeed = 1.0
        rotspeed = 0
    elif forwardcone[4] > 1.5 and forwardcone[9] > 1.7:
        if forwardcone[3] < 1.5:
            rotspeed = -0.2
        elif forwardcone[5] > 2.0:
            rotspeed = 0.4
        else:
            print("nothing")
            forwardspeed = -0.1
            rotspeed = -1.0
    else:
        rotspeed = -1.0

    if forwardcone[4] < 1.4 or forwardcone[5] < 1.2 or forwardcone[3] < 1.2:
        forwardspeed = 0

    pub.publish(Vector3(forwardspeed,0,0),Vector3(0,0,rotspeed))


def WallFollow(laserdata):
    global wallfollow
    global wallfollowleft
    global forwardcone
    global forwardspeed
    global rotspeed
    print("wallfollow")
    rotspeed = 0.5
    forwardspeed = 0
    # rospy.loginfo(rospy.get_caller_id() + 'WallFollow %s', str(wallfollow))
    if forwardcone[10] > 2.5 and forwardcone[4] > 2.5 :
        forwardspeed = 0.3
    else:
        rotspeed = -0.3

    if forwardcone[6] > 2 and forwardcone[7] > 2 and forwardcone[8] > 2 :
        wallfollow = False


def WallFollowLeft(laserdata):
    global wallfollowleft
    global wallfollow
    global forwardcone
    global forwardspeed
    global rotspeed
    # rospy.loginfo(rospy.get_caller_id() + 'Left %s', str(wallfollow))
    rotspeed = -0.5
    forwardspeed = 0
    # rospy.loginfo(rospy.get_caller_id() + 'WallFollow %s', str(wallfollow))
    if math.fabs(forwardcone[1] - forwardcone[0]) > 0.5 and forwardcone[1] < forwardcone[0]:
        rotspeed = -0.2
    elif forwardcone[1] > 2.9 :
        rotspeed = 0.2
    elif math.fabs(forwardcone[1] - forwardcone[0]) > 0.5 and forwardcone[1] > forwardcone[0]:
        rotspeed = 0.2
    elif forwardcone[2] > 2.9:
        rotspeed = 0
        forwardspeed = 1.0
    else:
        wallfollowleft = False

def GoalSeek(laserdata):
    global wallfollow
    global wallfollowleft
    global forwardcone
    global forwardspeed
    global rotspeed
    if forwardcone[2] > 2.9:
        forwardspeed = 1.0
        rotspeed = 0
    elif forwardcone[3] < forwardcone[3]:
        WallFollow = True
        forwardspeed = 0
        rotspeed = 1.0
    else:
        WallFollowLeft = True
        WallFollow = False
        forwardspeed = 0
        rotspeed = -1.0
    # rospy.loginfo(rospy.get_caller_id() + 'goalseek %s', str(laserdata.intensities[180]))
    # rotspeed = 0
    # if forwardcone[2] > 3:
    #     pub.publish(Vector3(1.1,0,0),Vector3(0,0,0))
    # elif forwardcone[2] < forwardcone[4]:
    #     wallfollowleft = False
    #     wallfollow = True
    # else:
    #     pub.publish(Vector3(0,0,0),Vector3(0,0,0.2))
    #     #pub.publish(Vector3(0,0,0),Vector3(0,0,0.5))


def SetGoalPosition(goaldata):
    global goalposition

    global goalset
    global wallfollow
    global wallfollowleft
    global forwardcone
    global forwardspeed
    global rotspeed
    if goalset == False:
        goalposition = (-goaldata.pose.position.x, -goaldata.pose.position.y,0)
        goalset = True
        print(str(goaldata))
    #rospy.loginfo(rospy.get_caller_id() + 'test heard %s', str(laserdata.intensities[180]))

def SetBotIntialPosition(data):
    global botset
    global botposition

    botposition =  (data.pose.pose.position.x,data.pose.pose.position.y,0)
    botset = True

def toast():
    rospy.init_node('my_toaster', anonymous=False)
    rate = rospy.Rate(1) # 10hz
    global pub
    global goalset
    global botset
    global forwardcone
    global forwardspeed
    global rotspeed
    goalposition = Vector3(0,0,0)
    botposition = Vector3(0,0,0)
    while not rospy.is_shutdown():
        # negative rotation is right

        if botset == False:
            rospy.Subscriber('base_pose_ground_truth', Odometry, SetBotIntialPosition)
        elif goalset == False:
            #get the goal position, which doesnt change so it only needs to be checked once
            rospy.Subscriber('homing_signal', PoseStamped, SetGoalPosition)
        else:
            rospy.Subscriber('base_scan', LaserScan, CheckLaserSection)
        print("---")
        #rospy.Subscriber('base_scan', LaserScan, CheckLaserSection)
	    #rospy.Subscriber('odom', Odometry, callbackmove)
        rate.sleep()


if __name__ == '__main__':
    try:

	robotpos = (0,0,0)
        toast()
    except rospy.ROSInterruptException:
        pass
