#!/usr/bin/env python
import rospy
import math
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist,Vector3
from std_msgs.msg import Int32MultiArray
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist,Vector3
import tf.transformations as transform
pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
goalposition = Vector3(0,0,0)
botposition = Vector3(0,0,0)
goalangle = 0.0
count = 0
line = [[0,0]]
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
    global line
    global goalangle
    if count < 2:
        quaternion = (
        data.pose.pose.orientation.x,
        data.pose.pose.orientation.y,
        data.pose.pose.orientation.z,
        data.pose.pose.orientation.w)
        euler = transform.euler_from_quaternion(quaternion)
        roll = euler[0]
        pitch = euler[1]
        yaw = euler[2]



        # print(transform.quaternion_from_euler(roll, pitch, yaw)  )
        # print(math.atan2( goalposition.y - data.pose.pose.position.y, goalposition.x - data.pose.pose.position.x))
        # rospy.loginfo(rospy.get_caller_id() + 'test heard %s', str(geometry_msgs.msg.Quaternion(*tf_conversions.transformations.quaternion_from_euler(roll, pitch, yaw))))
        #odom rospy.loginfo(rospy.get_caller_id() + 'test heard %s', str(data.pose.pose.position.x))
        """
        Rotate a point counterclockwise by a given angle around a given origin.

        The angle should be given in radians.
        """
        px = -goalposition.x
        py = -goalposition.y
        ox = data.pose.pose.position.x
        oy = data.pose.pose.position.y
        angle = math.atan2( goalposition.y - data.pose.pose.position.y, goalposition.x - data.pose.pose.position.x)
        angle = angle * (90/math.pi);
        #angle = math.atan2(  data.pose.pose.position.y - goalposition.y,  data.pose.pose.position.x - goalposition.x )
        qx = ox + math.cos(math.degrees(angle)) * (px - ox) - math.sin(math.degrees(angle)) * (py - oy)
        qy = oy + math.sin(math.degrees(angle)) * (px - ox) + math.cos(math.degrees(angle)) * (py - oy)
        print( str(qx) + " : "  + str(qy))
        print(str(data.pose.pose.orientation.z) +  " : " + str(data.pose.pose.orientation.w))
        print(angle + 90)
        print(math.degrees(yaw))
        goalangle = math.atan((goalposition.y - data.pose.pose.position.y) / (goalposition.y - data.pose.pose.position.y)) - math.degrees(yaw)
        # goalangle = (angle + 90)
        fwdspeed = 0
        rotspeed = 0.2
        count = 2

def move(data):
    print("")
    global goalposition
    global botposition
    global count
    global line
    global goalangle

    quaternion = (
    data.pose.pose.orientation.x,
    data.pose.pose.orientation.y,
    data.pose.pose.orientation.z,
    data.pose.pose.orientation.w)
    euler = transform.euler_from_quaternion(quaternion)
    roll = euler[0]
    pitch = euler[1]
    yaw = euler[2]



    # print(transform.quaternion_from_euler(roll, pitch, yaw)  )
    # print(math.atan2( goalposition.y - data.pose.pose.position.y, goalposition.x - data.pose.pose.position.x))
    # rospy.loginfo(rospy.get_caller_id() + 'test heard %s', str(geometry_msgs.msg.Quaternion(*tf_conversions.transformations.quaternion_from_euler(roll, pitch, yaw))))
    #odom rospy.loginfo(rospy.get_caller_id() + 'test heard %s', str(data.pose.pose.position.x))

    #angle = math.atan2(  data.pose.pose.position.y - goalposition.y,  data.pose.pose.position.x - goalposition.x )

    # print( str(qx) + " : "  + str(qy))
    # print(str(data.pose.pose.orientation.z) +  " : " + str(data.pose.pose.orientation.w))
    # print(angle + 90)
    print("goal angle: " + str(goalangle) + " : " + str(math.degrees(yaw)))

    fwdspeed = 0
    rotspeed = 1.2
    count = 3
    # if angle < 0:
    #      angle = 360 - (-angle);

    if math.fabs(goalangle - math.degrees(yaw)) < 5.5:
        fwdspeed = 0.1
        rotspeed = 0
    elif math.fabs(goalangle - math.degrees(yaw)) > 25.5:
        fwdspeed = 0
        rotspeed = 1.2
    else:
        fwdspeed = 0
        rotspeed = 1.2
    pub.publish(Vector3(fwdspeed,0,0),Vector3(0,0,rotspeed))


def testlisten():
    #pub = rospy.Publisher('my_test', PoseStamped, queue_size=10)
    rospy.init_node('testdata', anonymous=False)
    rate = rospy.Rate(1) # 10hz
    global goalposition
    global botposition
    global count
    global line
    global pub
    while not rospy.is_shutdown():
        #home_pose.header.stamp = rospy.Time.now()
	#rospy.Subscriber('base_scan', LaserScan, callback)
        if count == 0:
            rospy.Subscriber('homing_signal', PoseStamped, SetGoalPosition)
        if count == 1:
            rospy.Subscriber('odom', Odometry, findline)
        else:
            rospy.Subscriber('odom', Odometry, move)

	rate.sleep()


if __name__ == '__main__':
    try:
	count = 1;
        testlisten()
    except rospy.ROSInterruptException:
        pass
