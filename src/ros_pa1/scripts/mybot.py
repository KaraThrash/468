#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist,Vector3
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
def callback(data):
    tempstring = "["
    for i in data.intensities:
	if i == 1:
	     tempstring = tempstring + "="
        else:
	     tempstring = tempstring + "x"
    tempstring = tempstring + "]"
    rospy.loginfo(rospy.get_caller_id() + 'test heard %s', tempstring)
    
def callbackmove(data):
    if data.intensities[180] == 0.0:
	pub.publish(Vector3(1,0,0),Vector3(0,0,0))
	rospy.loginfo(rospy.get_caller_id() + 'x %s', str(data.intensities[180]))

    else:
	rospy.Subscriber('odom', Odometry, callbackstopmove)
	rospy.loginfo(rospy.get_caller_id() + 'z %s', str(data.intensities[180]))

def callbackstopmove(data):
    if data.twist.twist.linear.x != 0:
	pub.publish(Vector3(0,0,0),Vector3(0,0,0.5))
	rospy.loginfo(rospy.get_caller_id() + 'Stop x %s', str(data.twist.twist.linear.x))
    else:
	pub.publish(Vector3(0,0,0),Vector3(0,0,0.5))


def testbot():
    rospy.init_node('my_bot', anonymous=False)
    rate = rospy.Rate(10) # 10hz
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    
    while not rospy.is_shutdown():
	rospy.Subscriber('base_scan', LaserScan, callbackmove)
	rate.sleep()


if __name__ == '__main__':
    try:
	pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
	count = 1
        testbot()
    except rospy.ROSInterruptException:
        pass
