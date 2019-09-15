#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'test heard %s', str(data))
    

def testlisten():
    pub = rospy.Publisher('my_listen', PoseStamped, queue_size=10)
    rospy.init_node('my_listen', anonymous=False)
    rate = rospy.Rate(10) # 10hz

    home_pose = PoseStamped()
    home_pose.header.frame_id = "odom"

    home_pose.pose.position.x = 1.1
    home_pose.pose.position.y = 1.1
    home_pose.pose.position.z = 0

    
    while not rospy.is_shutdown():
        
        home_pose.header.stamp = rospy.Time.now()
	rospy.Subscriber('base_scan', LaserScan, callback)
	rate.sleep()


if __name__ == '__main__':
    try:
	count = 1;
        testlisten()
    except rospy.ROSInterruptException:
        pass
