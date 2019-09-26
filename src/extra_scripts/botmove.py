#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist,Vector3
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'bot x - signal x %s', str(robotpos[0] - data.pose.position.x))

def callbackmove(data):
    robotpos = (data.pose.pose.position.x,data.pose.pose.position.y,data.pose.pose.position.z)
    #rospy.Subscriber('homing_signal', PoseStamped, callback)
    rospy.loginfo(rospy.get_caller_id() + 'test heard %s', str(data.pose.pose.position.y))

def CheckLaserSection(laserdata):
    global pub
    rospy.loginfo(rospy.get_caller_id() + 'test heard %s', str(laserdata.intensities[180]))
    if laserdata.intensities[160] < 1 and laserdata.intensities[205] < 1 and laserdata.intensities[180] < 1:
        pub.publish(Vector3(1.1,0,0),Vector3(0,0,0))
    else:
        pub.publish(Vector3(0,0,0),Vector3(0,0,0.5))

def testmovelisten():
    rospy.init_node('my_moveListen', anonymous=False)
    rate = rospy.Rate(1) # 10hz
    global pub


    while not rospy.is_shutdown():
        rospy.Subscriber('base_scan', LaserScan, CheckLaserSection)
	#rospy.Subscriber('odom', Odometry, callbackmove)
        rate.sleep()


if __name__ == '__main__':
    try:

	robotpos = (0,0,0)
        testmovelisten()
    except rospy.ROSInterruptException:
        pass
