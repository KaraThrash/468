#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist,Vector3
from std_msgs.msg import Int32MultiArray
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist,Vector3
import tf.transformations as transform

goalposition = Vector3(0,0,0)
botposition = Vector3(0,0,0)
count = 0
def lasercallback(data):
        rospy.loginfo(rospy.get_caller_id() + 'laser:  %s', str(data) )
def callback(data):
    quaternion = (
    data.pose.pose.orientation.x,
    data.pose.pose.orientation.y,
    data.pose.pose.orientation.z,
    data.pose.pose.orientation.w)
    euler = transform.euler_from_quaternion(quaternion)
    roll = euler[0]
    pitch = euler[1]
    yaw = euler[2]
    print(transform.quaternion_from_euler(roll, pitch, yaw))
def SetGoalPosition(data):
    global goalposition
    global botposition
    global count
    count = 1;
    goalposition = data.pose.pose.position
def findline(data):
    print("")
    global goalposition
    global botposition
    global count
    count = 2
    botposition = data.pose.pose.position
    # rospy.loginfo(rospy.get_caller_id() + 'test heard %s', str(geometry_msgs.msg.Quaternion(*tf_conversions.transformations.quaternion_from_euler(roll, pitch, yaw))))
    #odom rospy.loginfo(rospy.get_caller_id() + 'test heard %s', str(data.pose.pose.position.x))




def testlisten():
    #pub = rospy.Publisher('my_test', PoseStamped, queue_size=10)
    rospy.init_node('testdata', anonymous=False)
    rate = rospy.Rate(10) # 10hz
    global goalposition
    global botposition
    global count
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    while not rospy.is_shutdown():
        #home_pose.header.stamp = rospy.Time.now()
	       # rospy.Subscriber('base_scan', LaserScan, lasercallback)
        rospy.Subscriber('base_pose_ground_truth', Odometry, lasercallback)
        # pub.publish(Vector3(0.1,0,0),Vector3(0,0,0.1))
        # if count == 0:
        #     rospy.Subscriber('homing_signal', PoseStamped, SetGoalPosition)
        # if count == 1:
        #     rospy.Subscriber('odom', Odometry, findline)
        # else:
        #     rospy.Subscriber('odom', Odometry, callback)
        rate.sleep()


if __name__ == '__main__':
    try:
	count = 1;
        testlisten()
    except rospy.ROSInterruptException:
        pass
