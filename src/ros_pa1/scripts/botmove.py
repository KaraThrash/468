#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist,Vector3
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'test heard %s', str(data.twist.twist.linear.x))
    
def callbackmove(data):
    rospy.loginfo(rospy.get_caller_id() + 'test heard %s', str(data))

def testmovelisten():
    rospy.init_node('my_moveListen', anonymous=False)
    rate = rospy.Rate(10) # 10hz


    
    while not rospy.is_shutdown():
	rospy.Subscriber('odom', Odometry, callback)
	rate.sleep()


if __name__ == '__main__':
    try:

	count = 1
        testmovelisten()
    except rospy.ROSInterruptException:
        pass
