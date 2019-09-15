#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist,Vector3
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
def callback(data):
    #print(CheckLaserSection(data.intensities[0:35]) + CheckLaserSection(data.intensities[36:70]) + CheckLaserSection(data.intensities[71:86]) + CheckLaserSection(data.intensities[87:123]) + CheckLaserSection(data.intensities[124:180]))
    #print(str(data.intensities))
    callback2(data.intensities[90:270])
    #pub.publish(CheckLaserSection(data.intensities[0:35]) + CheckLaserSection(data.intensities[36:70]) + CheckLaserSection(data.intensities[71:86]) + CheckLaserSection(data.intensities[87:123]) + CheckLaserSection(data.intensities[124:180]))
    
def callback2(data):
    global count
    global tempstring
    tempstring2 = CheckLaserSection(data[0:35]) + CheckLaserSection(data[36:70]) + CheckLaserSection(data[71:86]) + CheckLaserSection(data[87:123]) + CheckLaserSection(data[124:180])
    if tempstring != tempstring2:
	count = count + 1
    pub.publish(tempstring2)
    tempstring = tempstring2
    
    #rospy.loginfo(rospy.get_caller_id() + 'test heard %s', tempstring)

def CheckLaserSection(laserdata):
    tempsting = "t"
    for i in laserdata:
      if int(i) == 1:
	tempsting = "f"
    return tempsting

def pathfindstart():
    rospy.init_node('pathfinder', anonymous=False)
    rate = rospy.Rate(10) # 10hz
    

    
    while not rospy.is_shutdown():
	rospy.Subscriber('base_scan', LaserScan, callback)
	rate.sleep()


if __name__ == '__main__':
    try:
	count = 0
        tempstring = "xxxxx"
	pub = rospy.Publisher('laserSections', String, queue_size=10)
	robotpos = (0,0,0)
        pathfindstart()
    except rospy.ROSInterruptException:
        pass
