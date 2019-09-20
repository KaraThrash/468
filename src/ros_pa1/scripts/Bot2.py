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
    rospy.loginfo(rospy.get_caller_id() + 'test heard %s', str(laserdata.intensities[180]))
    if wallfollow == True:
        WallFollow(laserdata)
    else:
        GoalSeek(laserdata)

def WallFollow(laserdata):
    global wallfollow
    rospy.loginfo(rospy.get_caller_id() + 'test heard %s', str(wallfollow))
    if laserdata.intensities[160] > 0:
        pub.publish(Vector3(0,0,0),Vector3(0,0,0.5)) #rotate left
    elif laserdata.intensities[180] < 1 and  laserdata.intensities[195] < 1:
        pub.publish(Vector3(1.0,0,0),Vector3(0,0,0))

    elif laserdata.intensities[30] < 1:
        wallfollow = False
    else:
        pub.publish(Vector3(1.1,0,0),Vector3(0,0,0))


def GoalSeek(laserdata):
    global wallfollow
    rospy.loginfo(rospy.get_caller_id() + 'test heard %s', str(laserdata.intensities[180]))
    if laserdata.intensities[160] < 1 and laserdata.intensities[205] < 1 and laserdata.intensities[180] < 1:
        pub.publish(Vector3(1.1,0,0),Vector3(0,0,0))
    else:
        wallfollow = True
        #pub.publish(Vector3(0,0,0),Vector3(0,0,0.5))


def SetGoalPosition(goaldata):
    global goalposition
    goalposition = (goaldata.pose.position.x,goaldata.pose.position.y,0)
    global goalset
    global wallfollow
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
    goalposition = Vector3(0,0,0)
    while not rospy.is_shutdown():
        if goalset == False:
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
