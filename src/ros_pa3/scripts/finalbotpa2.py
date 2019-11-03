#!/usr/bin/env python
import rospy
import math
import rosbag
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist,Vector3
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
import tf.transformations as transform




def astartest(data):
    bag = rosbag.Bag('test.bag')
    for topic, msg, t in bag.read_messages(topics=['chatter', 'numbers']):
        print msg
    bag.close()
    print(data)



# be a cylon
def astartoaster():
    rospy.init_node('my_toaster', anonymous=False)
    rate = rospy.Rate(1) # 10hz

    # rospy.set_param('goalx', 11.0)
    # rospy.set_param('goaly', 1.0)
    bag = rosbag.Bag('grid.bag')
    print(bag)
    for topic, msg, t in bag.read_messages(topics=[ 'Observations']):
        print("Observations: ", msg.timeTag, " ", msg.tagNum," ", msg.range," ", msg.bearing.x," ", msg.bearing.y," ", msg.bearing.z," ", msg.bearing.w)
    for topic, msg, t in bag.read_messages(topics=[ 'Movements']):
        # print(msg)
        print("Movements1: ", msg.timeTag, " ", round(msg.rotation1.x,2)," ", round(msg.rotation1.y,2)," ", round(msg.rotation1.z,2)," ", round(msg.rotation1.w,2))
        print(" translation:", round(msg.translation,2))
        print("Movements2: ",round(msg.rotation2.x,2)," ", round(msg.rotation2.y,2)," ", round(msg.rotation2.z,2)," ", round(msg.rotation2.w,2)," ")
        # print("obs: ", msg.timeTag, " ", msg.tagNum," ", msg.range," ", msg.bearing.x," ", msg.bearing.y," ", msg.bearing.z," ", msg.bearing.w)


    while not rospy.is_shutdown():
        # rospy.loginfo('my toast')
        rospy.Subscriber('line_list', Marker, astartest)

        bag.close()
        rate.sleep()


if __name__ == '__main__':
    try:
        astartoaster()
    except rospy.ROSInterruptException:
        pass
#UBIT: Dvdonato
#Daniel Donato
