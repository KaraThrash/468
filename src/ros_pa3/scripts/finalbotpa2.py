#!/usr/bin/env python
import rospy
import math
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist,Vector3
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
import tf.transformations as transform




def astartest(data):
    print(data)



# be a cylon
def astartoaster():
    rospy.init_node('my_toaster', anonymous=False)
    rate = rospy.Rate(1) # 10hz

    # rospy.set_param('goalx', 11.0)
    # rospy.set_param('goaly', 1.0)

    while not rospy.is_shutdown():
        rospy.loginfo('my toast')
        rospy.Subscriber('line_list', Marker, astartest)

        rate.sleep()


if __name__ == '__main__':
    try:
        astartoaster()
    except rospy.ROSInterruptException:
        pass
#UBIT: Dvdonato
#Daniel Donato
