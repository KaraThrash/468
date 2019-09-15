#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist,Vector3
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'bot x - signal x %s', str(robotpos[0] - data.pose.position.x))
    
def callbackmove(data):
    robotpos = (data.pose.pose.position.x,data.pose.pose.position.y,data.pose.pose.position.z)
    #rospy.Subscriber('homing_signal', PoseStamped, callback)
    rospy.loginfo(rospy.get_caller_id() + 'test heard %s', str(data.pose.pose.position.y))

def testmovelisten():
    rospy.init_node('my_moveListen', anonymous=False)
    rate = rospy.Rate(10) # 10hz


    
    while not rospy.is_shutdown():
	rospy.Subscriber('odom', Odometry, callbackmove)
	rate.sleep()


if __name__ == '__main__':
    try:

	robotpos = (0,0,0)
        testmovelisten()
    except rospy.ROSInterruptException:
        pass
