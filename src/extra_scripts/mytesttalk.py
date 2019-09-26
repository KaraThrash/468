#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped


def testtalk():
   
    rospy.init_node('my_talk', anonymous=False)
    rate = rospy.Rate(10) # 10hz
    pub = rospy.Publisher('mytalk', String, queue_size=10)
    count2 = count

    
    while not rospy.is_shutdown():
	count2 = count2 + 1
	if count2 > 10:
		count2 = 1
	hello_str = str(count2)
	pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
	count = 1
        testtalk()
    except rospy.ROSInterruptException:
        pass
