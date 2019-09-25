#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist,Vector3
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
goalposition = Vector3(0,0,0)
goalset = False
wallfollow = False
wallfollowleft = False
forwardcone = [0,0,0,0,0]
forwardspeed = 0.0
rotspeed = 0.0
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'bot x - signal x %s', str(robotpos[0] - data.pose.position.x))

def callbackmove(data):
    robotpos = (data.pose.pose.position.x,data.pose.pose.position.y,data.pose.pose.position.z)
    #rospy.Subscriber('homing_signal', PoseStamped, callback)
    rospy.loginfo(rospy.get_caller_id() + 'test heard %s', str(data.pose.pose.position.y))

# def CheckLaserSection(laserdata):
#     global pub
#     rospy.loginfo(rospy.get_caller_id() + 'test heard %s', str(laserdata.intensities[180]))
#     if laserdata.intensities[160] < 1 and laserdata.intensities[205] < 1 and laserdata.intensities[180] < 1:
#         pub.publish(Vector3(1.1,0,0),Vector3(0,0,0))
#     else:
#         pub.publish(Vector3(0,0,0),Vector3(0,0,0.5))

def CheckLaserSection(laserdata):
    global wallfollow
    global forwardcone
    global forwardspeed
    global rotspeed
    forwardcone[0] = (laserdata.ranges[1] + laserdata.ranges[35] + laserdata.ranges[70]) / 3
    forwardcone[1] = (laserdata.ranges[75] + laserdata.ranges[95] + laserdata.ranges[130] ) / 3
    forwardcone[2] = (laserdata.ranges[135] +  laserdata.ranges[175] + laserdata.ranges[180] +  laserdata.ranges[185] + laserdata.ranges[225]) / 5
    forwardcone[3] = (laserdata.ranges[226] + laserdata.ranges[250] + laserdata.ranges[320]) / 3
    forwardcone[4] = (laserdata.ranges[321] + laserdata.ranges[345] + laserdata.ranges[360]) / 3
    # forwardcone[0] = int(forwardcone[0])
    # forwardcone[1] = int(forwardcone[1])
    # forwardcone[2] = int(forwardcone[2])
    # forwardcone[3] = int(forwardcone[3])
    # forwardcone[4] = int(forwardcone[4])
    if forwardcone[2] > 2.9:
        forwardspeed = 1.0
        rotspeed = 0
    else:
        forwardspeed = 0
        rotspeed = 0.5
        if forwardspeed > 0:
            forwardspeed = 0
            rotspeed = 0.5
            # if wallfollowleft == False:
            #     wallfollow = True

        # if wallfollowleft == False:
            # wallfollow = True
        forwardspeed = 0
    # rospy.loginfo(rospy.get_caller_id() + 'CheckLaserSection %s', str(laserdata.ranges[180]))
    # if wallfollow == True:
    #     WallFollow(laserdata)
    # elif wallfollowleft == True:
    #     WallFollowLeft(laserdata)
    # else:
    #     GoalSeek(laserdata)
    rospy.loginfo(rospy.get_caller_id() + 'forward and rot speed:  %s', str(forwardspeed) + " : "+ str(rotspeed))
    pub.publish(Vector3(forwardspeed,0,0),Vector3(0,0,rotspeed))

def WallFollow(laserdata):
    global wallfollow
    global wallfollowleft
    global forwardcone
    global forwardspeed
    global rotspeed
    rotspeed = 0.5
    # rospy.loginfo(rospy.get_caller_id() + 'WallFollow %s', str(wallfollow))
    if forwardcone[3] > 2:
        wallfollow = False
    elif forwardcone[4] > forwardcone[3] and forwardcone[4] > 1:
        rotspeed = -0.2
    else:
        wallfollowleft = True
        wallfollow = False

def WallFollowLeft(laserdata):
    global wallfollowleft
    global wallfollow
    global forwardcone
    global forwardspeed
    global rotspeed
    # rospy.loginfo(rospy.get_caller_id() + 'Left %s', str(wallfollow))
    if forwardcone[2] > 2:
        wallfollow = False
        wallfollowleft = False
        rotspeed = 0
    else:
        rotspeed = 0.3
        #pub.publish(Vector3(0,0,0),Vector3(0,0,-0.5))

def GoalSeek(laserdata):
    global wallfollow
    global wallfollowleft
    global forwardcone
    global forwardspeed
    global rotspeed
    # rospy.loginfo(rospy.get_caller_id() + 'goalseek %s', str(laserdata.intensities[180]))
    rotspeed = 0
    # if forwardcone[2] > 3:
    #     pub.publish(Vector3(1.1,0,0),Vector3(0,0,0))
    # elif forwardcone[2] < forwardcone[4]:
    #     wallfollowleft = False
    #     wallfollow = True
    # else:
    #     pub.publish(Vector3(0,0,0),Vector3(0,0,0.2))
    #     #pub.publish(Vector3(0,0,0),Vector3(0,0,0.5))


def SetGoalPosition(goaldata):
    global goalposition
    goalposition = (goaldata.pose.position.x,goaldata.pose.position.y,0)
    global goalset
    global wallfollow
    global wallfollowleft
    global forwardcone
    global forwardspeed
    global rotspeed
    if goalset == False:
        goalset = True
        print(str(goaldata))
    #rospy.loginfo(rospy.get_caller_id() + 'test heard %s', str(laserdata.intensities[180]))



def toast():
    rospy.init_node('my_toaster', anonymous=False)
    rate = rospy.Rate(10) # 10hz
    global pub
    global goalposition
    global goalset
    global forwardcone
    global forwardspeed
    global rotspeed
    goalposition = Vector3(0,0,0)
    while not rospy.is_shutdown():
        # negative rotation is right
        if goalset == False:
            #get the goal position, which doesnt change so it only needs to be checked once
            rospy.Subscriber('homing_signal', PoseStamped, SetGoalPosition)
        else:
            rospy.Subscriber('base_scan', LaserScan, CheckLaserSection)
        print("---")
        #rospy.Subscriber('base_scan', LaserScan, CheckLaserSection)
	    #rospy.Subscriber('odom', Odometry, callbackmove)
        rate.sleep()


if __name__ == '__main__':
    try:

	robotpos = (0,0,0)
        toast()
    except rospy.ROSInterruptException:
        pass
