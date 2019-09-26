#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist,Vector3
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
goalposition = Vector3(0,0,0)
goalset = False
wallfollow = False
wallfollowleft = False
forwardcone = [0,0,0,0,0]

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
    forwardcone[0] = laserdata.ranges[5] + laserdata.ranges[25] + laserdata.ranges[50]
    forwardcone[1] = laserdata.ranges[90] + laserdata.ranges[130] + laserdata.ranges[55]
    forwardcone[2] = laserdata.ranges[155] + laserdata.ranges[180] + laserdata.ranges[200]
    forwardcone[3] = laserdata.ranges[205] + laserdata.ranges[230] + laserdata.ranges[250]
    forwardcone[4] = laserdata.ranges[255] + laserdata.ranges[300] + laserdata.ranges[330]
    # forwardcone[0] = int(forwardcone[0])
    # forwardcone[1] = int(forwardcone[1])
    # forwardcone[2] = int(forwardcone[2])
    # forwardcone[3] = int(forwardcone[3])
    # forwardcone[4] = int(forwardcone[4])
    rospy.loginfo(rospy.get_caller_id() + 'test heard %s', str(laserdata.intensities[180]))
    if wallfollow == True:
        WallFollow(laserdata)
    elif wallfollowleft == True:
        WallFollowLeft(laserdata)
    else:
        GoalSeek(laserdata)

def WallFollow(laserdata):
    global wallfollow
    global wallfollowleft
    global forwardcone
    direction = 0.5
    rospy.loginfo(rospy.get_caller_id() + 'WallFollow %s', str(wallfollow))
    if laserdata.ranges[250] > 1 and laserdata.ranges[255] > laserdata.ranges[250]:
        pub.publish(Vector3(0,0,0),Vector3(0,0,direction)) #rotate left
    elif laserdata.ranges[180] > 1 and laserdata.ranges[195] > 1 and laserdata.ranges[160] > 1:
        pub.publish(Vector3(0.2,0,0),Vector3(0,0,0))
        wallfollowleft = False
        wallfollow = False
    elif laserdata.ranges[350] > 2 and laserdata.ranges[300] > 2 and laserdata.ranges[180] > 1:
        pub.publish(Vector3(0.2,0,0),Vector3(0,0,0.3))
        wallfollowleft = False
        wallfollow = False
    elif laserdata.ranges[350] < 2 and laserdata.ranges[300] < 2 and laserdata.ranges[190] < 2:
        wallfollowleft = True
    else:
        pub.publish(Vector3(0,0,0),Vector3(0,0,-0.3))

def WallFollowLeft(laserdata):
    global wallfollowleft
    global wallfollow
    global forwardcone
    rospy.loginfo(rospy.get_caller_id() + 'Left %s', str(wallfollow))
    if laserdata.ranges[180] > 2 and laserdata.ranges[220] > 2 and laserdata.ranges[150] > 2:
            wallfollow = False
            wallfollowleft = False
    else:
        pub.publish(Vector3(0,0,0),Vector3(0,0,-0.5))

def GoalSeek(laserdata):
    global wallfollow
    global wallfollowleft
    global forwardcone
    rospy.loginfo(rospy.get_caller_id() + 'test heard %s', str(laserdata.intensities[180]))
    if laserdata.ranges[180] > 2 and laserdata.ranges[200] > 2 and laserdata.ranges[160] > 2:
        pub.publish(Vector3(1.1,0,0),Vector3(0,0,0))
    elif laserdata.ranges[180] > 1 and laserdata.ranges[200] > 1 and laserdata.ranges[160] > 1:
        pub.publish(Vector3(0.2,0,0),Vector3(0,0,0))
    else:
        wallfollowleft = True
        wallfollow = True
        #pub.publish(Vector3(0,0,0),Vector3(0,0,0.5))


def SetGoalPosition(goaldata):
    global goalposition
    goalposition = (goaldata.pose.position.x,goaldata.pose.position.y,0)
    global goalset
    global wallfollow
    global wallfollowleft
    global forwardcone
    if goalset == False:
        goalset = True
        print(str(goaldata))
    #rospy.loginfo(rospy.get_caller_id() + 'test heard %s', str(laserdata.intensities[180]))



def toast():
    rospy.init_node('my_toaster', anonymous=False)
    rate = rospy.Rate(1) # 10hz
    global pub
    global goalposition
    global goalset
    global forwardcone
    goalposition = Vector3(0,0,0)
    while not rospy.is_shutdown():
        if goalset == False:
            #get the goal position, which doesnt change so it only needs to be checked once
            rospy.Subscriber('homing_signal', PoseStamped, SetGoalPosition)
        else:
            rospy.Subscriber('base_scan', LaserScan, CheckLaserSection)
        print("---")
        #rospy.Subscriber('base_scan', LaserScan, CheckLaserSection)

        rate.sleep()


if __name__ == '__main__':
    try:

	robotpos = (0,0,0)
        toast()
    except rospy.ROSInterruptException:
        pass
