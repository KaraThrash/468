#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist,Vector3
from std_msgs.msg import Int32MultiArray
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'test heard %s', str(data.pose.pose.position.x))


def testlisten():
    #pub = rospy.Publisher('my_test', PoseStamped, queue_size=10)
    rospy.init_node('testdata', anonymous=False)
    rate = rospy.Rate(10) # 10hz



    while not rospy.is_shutdown():
        #home_pose.header.stamp = rospy.Time.now()
	#rospy.Subscriber('base_scan', LaserScan, callback)
	rospy.Subscriber('odom', Odometry, callback)
	rate.sleep()


if __name__ == '__main__':
    try:
	count = 1;
        testlisten()
    except rospy.ROSInterruptException:
        pass
