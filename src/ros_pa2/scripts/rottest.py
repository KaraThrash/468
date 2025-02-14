#!/usr/bin/env python
import rospy
import math
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist,Vector3
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
import tf.transformations as transform

pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
goalposition = Vector3(0,0,0)
botposition = Vector3(0,0,0)
goalset = False
botset = False
wallfollow = False
wallfollowleft = False
forwardcone = [0,0,0,0,0,0,0,0,0,0,0]
forwardspeed = 0.0
rotspeed = 0.0
# positive is left


def CheckLaserSection(laserdata):
    global wallfollow
    global forwardcone
    global forwardspeed
    global rotspeed
    forwardcone[0] = (laserdata.ranges[1] + laserdata.ranges[35] + laserdata.ranges[45] + laserdata.ranges[55]) / 4
    forwardcone[1] = (laserdata.ranges[95] + laserdata.ranges[80] + laserdata.ranges[70] + laserdata.ranges[60] ) / 4
    forwardcone[2] = (laserdata.ranges[125] + laserdata.ranges[120] + laserdata.ranges[110] + laserdata.ranges[100] ) / 4
    # narrowleft forward
    forwardcone[3] = (laserdata.ranges[130] +  laserdata.ranges[135] + laserdata.ranges[140] +  laserdata.ranges[145] + laserdata.ranges[149]) / 5
    forwardcone[9] = (laserdata.ranges[145] + laserdata.ranges[150] +  laserdata.ranges[160] + laserdata.ranges[162] +  laserdata.ranges[165] + laserdata.ranges[168]) / 6



    forwardcone[4] = (laserdata.ranges[165] +  laserdata.ranges[175] + laserdata.ranges[170] +  laserdata.ranges[177] + laserdata.ranges[180] + laserdata.ranges[195] +  laserdata.ranges[185] + laserdata.ranges[190] + laserdata.ranges[187]) / 9
    # narrowright forward
    forwardcone[5] = (laserdata.ranges[211] +  laserdata.ranges[220] + laserdata.ranges[225] +  laserdata.ranges[230] + laserdata.ranges[235]) / 5
    forwardcone[10] = (laserdata.ranges[210] +  laserdata.ranges[205] + laserdata.ranges[195] + laserdata.ranges[192]) / 4

    forwardcone[6] = (laserdata.ranges[236] + laserdata.ranges[240] + laserdata.ranges[250] + laserdata.ranges[260]) / 4
    forwardcone[7] = (laserdata.ranges[270] + laserdata.ranges[280] + laserdata.ranges[290] + laserdata.ranges[310]) / 4
    forwardcone[8] = (laserdata.ranges[315] + laserdata.ranges[325] + laserdata.ranges[345] + laserdata.ranges[359]) / 4


    if WallFollow == True:
        WallFollow()
    else:
        AvoidObstablesAndFollowWall()

        # safety check against colliding
    if forwardcone[4] < 1.4 or forwardcone[9] < 1.4 or forwardcone[10] < 1.4:
        forwardspeed = 0
    if forwardspeed == 0 and rotspeed == 0:
        print("default")
        rotspeed = -0.1

    if math.fabs(botposition[0] - goalposition[0]) < 0.5 and math.fabs(botposition[1] - goalposition[1]) < 0.5:
        print("I'm home, now close the door and let me make toast")

    else:
        pub.publish(Vector3(forwardspeed,0,0),Vector3(0,0,rotspeed))


def quattest(data):
    global forwardspeed
    global rotspeed

    quaternion = [data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w]
    euler = transform.euler_from_quaternion(quaternion)
    print(euler)
    # print(quat_msg)
    if forwardcone[4] > 2.9 and forwardcone[9] > 2.9 and forwardcone[10] > 2.9:
        forwardspeed = 1.0
        rotspeed = 0
    if forwardcone[4] > 2.0 and forwardcone[9] > 2.2 and forwardcone[10] > 2.2:
        forwardspeed = 0.3
        rotspeed = 0
    else:
        rotspeed = -1.0
    if euler > 1:
        pub.publish(Vector3(0.1,0,0),Vector3(0,0,0.1))
    else:
        pub.publish(Vector3(0,0,0),Vector3(0,0,0.4))




def WallFollow(laserdata):
    global wallfollow
    global wallfollowleft
    global forwardcone
    global forwardspeed
    global rotspeed
    rotspeed = 0.5
    forwardspeed = 0
    if forwardcone[10] > 2.5 and forwardcone[4] > 2.5 :
        forwardspeed = 0.3
        rotspeed = 0
    else:
        rotspeed = -0.3
    if forwardcone[6] > 2 and forwardcone[7] > 2 and forwardcone[8] > 2 :
        wallfollow = False





# get bot world space
def SetBotIntialPosition(data):
    global botset
    global botposition
    botposition =  (data.pose.pose.position.x,data.pose.pose.position.y,0)
    botset = True

# be a cylon
def rotater():
    rospy.init_node('my_rotater', anonymous=False)
    rate = rospy.Rate(1) # 10hz
    global pub
    global goalset
    global botset
    global forwardcone
    global forwardspeed
    global rotspeed
    goalposition = Vector3(0,0,0)
    botposition = Vector3(0,0,0)
    while not rospy.is_shutdown():
        # negative rotation is right

        if botset == False:
            rospy.Subscriber('base_pose_ground_truth', Odometry, SetBotIntialPosition)
        else:
            rospy.Subscriber('base_pose_ground_truth', Odometry, quattest)
        rate.sleep()


if __name__ == '__main__':
    try:
        rotater()
    except rospy.ROSInterruptException:
        pass
#UBIT: Dvdonato
#Daniel Donato
