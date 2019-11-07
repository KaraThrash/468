#!/usr/bin/env python
# Ref 1: http://wiki.ros.org/rviz/DisplayTypes/Marker
# Ref 2: https://answers.ros.org/question/203782/rviz-marker-line_strip-is-not-displayed/

import rospy
import rosbag
import math
import numpy
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point

from geometry_msgs.msg import Twist,Vector3
from nav_msgs.msg import Odometry
import tf.transformations as transform

from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist,Vector3
grid = []
grida = []
rospy.loginfo('Rviz example')
botrot = 0.0
zplus = 0.0
def display_line_list(points, publisher):
    """
    A function that publishes a set of points as marker line list to Rviz.
    It will draw a line between each pair of points, so 0-1, 2-3, 4-5, ...

    Parameters:
    points (list): Each item in the list is a tuple (x, y) representing a point in xy space.
    publisher (rospy.Publisher): A publisher object used to pubish the marker

    Returns:
    None

    """

    marker = Marker()
    # The coordinate frame in which the marker is publsihed.
    # Make sure "Fixed Frame" under "Global Options" in the Display panel
    # in rviz is "/map"
    marker.header.frame_id = "/map"

    # Mark type (http://wiki.ros.org/rviz/DisplayTypes/Marker)
    # LINE_LIST: It will draw a line between each pair of points, so 0-1, 2-3, 4-5, ...
    marker.type = marker.LINE_LIST

    # Marker action (Set this as ADD)
    marker.action = marker.ADD

    # Marker scale
    marker.scale.x = 0.01
    marker.scale.y = 0.01
    marker.scale.z = 0.01

    # Marker color (Make sure a=1.0 which sets the opacity)
    marker.color.a = 1.0
    marker.color.r = 1.0
    marker.color.g = 1.0
    marker.color.b = 0.0

    # Marker orientaiton (Set it as default orientation in quaternion)
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0

    # Marker position
    # The position of the marker. In this case it the COM of all the points
    # Set this as 0,0,0
    marker.pose.position.x = 0.0
    marker.pose.position.y = 0.0
    marker.pose.position.z = 0.0

    # Marker line points
    marker.points = []


    zplus = 0.0
    for point in points:
        global zplus
        marker_point = Point()              # Create a new Point()
        marker_point.x = point[0]
        marker_point.y = point[1]
        marker_point.z = zplus
        marker.color.b = 1.0 - zplus
        marker.color.r = 1.0
        marker.color.g = 1.0 - zplus
        zplus = zplus + 0.01
        # print(zplus)
        marker.points.append(marker_point) # Append the marker_point to the marker.points list

    # Publish the Marker using the appropirate publisher
    publisher.publish(marker)


def display_cube_list(points, publisher):
    """
    A function that publishes a set of points as marker cubes in Rviz.
    Each point represents the COM of the cube to be displayed.

    Parameters:
    points (list): Each item in the list is a tuple (x, y) representing a point in xy space
                   for the COM of the cube.
    publisher (rospy.Publisher): A publisher object used to pubish the marker

    Returns:
    None

    """

    marker = Marker()
    # The coordinate frame in which the marker is published.
    # Make sure "Fixed Frame" under "Global Options" in the Display panel
    # in rviz is "/map"
    marker.header.frame_id = "/map"

    # Mark type (http://wiki.ros.org/rviz/DisplayTypes/Marker)
    # CUBE_LIST
    marker.type = marker.CUBE_LIST

    # Marker action (Set this as ADD)
    marker.action = marker.ADD

    # Marker scale (Size of the cube)
    marker.scale.x = 0.1
    marker.scale.y = 0.1
    marker.scale.z = 0.1

    # Marker color (Make sure a=1.0 which sets the opacity)
    marker.color.a = 1.0
    marker.color.r = 0.0
    marker.color.g = 1.0
    marker.color.b = 0.0

    # Marker orientation (Set it as default orientation in quaternion)
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0

    # Marker position
    # The position of the marker. In this case it the COM of all the cubes
    # Set this as 0,0,0
    marker.pose.position.x = 0.0
    marker.pose.position.y = 0.0
    marker.pose.position.z = 0.0

    # Marker line points
    marker.points = []

    for point in points:

        marker_point = Point()              # Create a new Point()
        marker_point.x = point[0]
        marker_point.y = point[1]
        marker_point.z = 0

        marker.points.append(marker_point)  # Append the marker_point to the marker.points list

    # Publish the Marker using the apporopriate publisher
    publisher.publish(marker)

def quattest(data):
    global botrot
    quaternion = (data.x,data.y,data.z,data.w)
    euler = transform.euler_from_quaternion(quaternion)

    xy = (1,1)


    rotamount = 0
    if euler[2] > -.75 and euler[2] < 0.75:
        rotamount = 0
    elif euler[2] >= -2.25 and euler[2] <= -0.75:
        rotamount = -1
    elif euler[2] > -4.25 and euler[2] < -2.25:
        rotamount = 2
    elif euler[2] <= 2.25 and euler[2] >= 0.75:
        rotamount = 1
    elif euler[2] <= 4.25 and euler[2] >= 2.25:
        rotamount = 2
    else:
        rotamount = 0

    if botrot == 0:
        if rotamount == 0:
            botrot = 0
        elif rotamount == 1:
            botrot = 1
        elif rotamount == -1:
            botrot = -1
        elif rotamount == 2:
            botrot = 2
        else:
            botrot = -2

    elif botrot == -1:
        if rotamount == 0:

            botrot = -1
        elif rotamount == 1:
            botrot = 0
        elif rotamount == -1:
            botrot = -2
        elif rotamount == 2:
            botrot = 1
        else:
            botrot = 1
    elif botrot == 1:
        if rotamount == 0:
            botrot = 1
        elif rotamount == 1:
            botrot = 2
        elif rotamount == -1:
            botrot = 0
        elif rotamount == 2:
            botrot = -1
        else:
            botrot = -1
    elif botrot == 2:

        if rotamount == 0:
            botrot = 2
        elif rotamount == 1:
            botrot = -1
        elif rotamount == -1:
            botrot = 1
        elif rotamount == 2:
            botrot = 2
        else:
            botrot = -2
    else:
        if rotamount == 0:
            botrot = 2
        elif rotamount == 1:
            botrot = -1
        elif rotamount == -1:
            botrot = 1
        elif rotamount == 2:
            botrot = 2
        else:
            botrot = -2


    if botrot == 0:
        xy = (1,0)
    elif botrot == 1:
        xy = (0,1)
    elif botrot == -1:
        xy = (0,-1)
    elif botrot == 2:
        xy = (-1,0)
    elif botrot == -2:
        xy = (-1,0)
    else:
        xy = (1,1)

    # if euler[2] > -.75 and euler[2] < 0.75:
    #     xy = (1,0)
    # elif euler[2] >= -2.25 and euler[2] <= -0.75:
    #     xy = (0,-1)
    # elif euler[2] > -4.25 and euler[2] < -2.25:
    #     xy = (-1,0)
    # elif euler[2] <= 2.25 and euler[2] >= 0.75:
    #     xy = (0,1)
    # elif euler[2] <= 4.25 and euler[2] >= 2.25:
    #     xy = (-1,0)
    # else:
    #     xy = (1,1)
    print("euler:",xy)
    return xy

def setbotrot(data):
    global botrot
    # quaternion = tf.transformations.quaternion_from_euler(roll, pitch, yaw)
    quaternion = (data.x,data.y,data.z,data.w)
    euler = transform.euler_from_quaternion(quaternion)
    # print("xxxxxxxxxxeulerxxxxxxxxxxxxxxxxxxx")
    # print(numpy.degrees(euler))
    # roll = euler[0]
    # pitch = euler[1]
    # yaw = euler[2]
    if euler[2] > -.75 and euler[2] < 0.75:
        botrot = 0
    elif euler[2] >= -2.25 and euler[2] <= -0.75:
        botrot = -1
    elif euler[2] > -4.25 and euler[2] < -2.25:
        botrot = -2
    elif euler[2] <= 2.25 and euler[2] >= 0.75:
        botrot = 1
    elif euler[2] <= 4.25 and euler[2] >= 2.25:
        botrot = 2
    else:
        botrot = 0

def test(msg):
    global grid
    global grida
    quaternion = (msg.rotation1.x,msg.rotation1.y,msg.rotation1.z,msg.rotation1.w)
    euler = transform.euler_from_quaternion(quaternion)

    degrees = numpy.degrees(euler)
    print("rot1: ", degrees)
    # numpy.degrees(euler[2])
    # print(degrees[3])
    # print("red")
    gausrots =  numpy.random.normal(degrees[2], 45, 10) #rot1
    sortedrots = [0,0,0,0]
    for normalrot in gausrots:
        if normalrot < 45 and normalrot > -45:
            sortedrots[0] = sortedrots[0] + 1
        elif normalrot < 135 and normalrot > 0:
            sortedrots[1] = sortedrots[1] + 1
        elif normalrot < -45 and normalrot > -135 :
            sortedrots[3] = sortedrots[3] + 1
        else:
            sortedrots[2] = sortedrots[2] + 1


    quaternion2 = (msg.rotation2.x,msg.rotation2.y,msg.rotation2.z,msg.rotation2.w)
    euler2 = transform.euler_from_quaternion(quaternion2)
    degrees2 = numpy.degrees(euler2)
    gausrots2 = numpy.random.normal(degrees2[2], 45, 10) #rot2
    sortedrots2 = [0,0,0,0]
    for normalrot2 in gausrots2:
        if normalrot2 < 45 and normalrot2 > -45:
            sortedrots2[0] = sortedrots2[0] + 1
        elif normalrot2 < 135 and normalrot2 > 0:
            sortedrots2[1] = sortedrots2[1] + 1
        elif normalrot2 < -45 and normalrot2 > -135 :
            sortedrots2[3] = sortedrots2[3] + 1
        else:
            sortedrots2[2] = sortedrots2[2] + 1

    travelnormal = numpy.random.normal((msg.translation * 5), 0.5, 10) # translation
    rowcount = -1
    colcount = -1

    # go through each square and if there is probabikity that the bot is there
    # Then set the values on the OTHER grid, resulting in the sum of all possible ecurrent states
    while rowcount < 35:
        # print("row: ",rowcount)
        rowcount = rowcount + 1
        colcount = -1
        while colcount < 35:
            colcount = colcount + 1
            col = grid[rowcount][colcount]

            for distnotrounded in travelnormal:
                dist = 0
                dist = int(math.ceil(distnotrounded))
                # NOTE: iterate through each possible rotation and current rotation in square to check if moving the distance is on the map
                if col[0] > 0: # right
                    if colcount + dist < 35:
                        grida[rowcount][colcount + dist][0] = grida[rowcount][colcount + dist][0] + (col[0] * sortedrots2[0] * sortedrots2[0])
                        grida[rowcount][colcount + dist][1] = grida[rowcount][colcount + dist][1] + (col[0] * sortedrots2[0] * sortedrots2[1])
                        grida[rowcount][colcount + dist][2] = grida[rowcount][colcount + dist][2] + (col[0] * sortedrots2[0] * sortedrots2[2])
                        grida[rowcount][colcount + dist][3] = grida[rowcount][colcount + dist][3] + (col[0] * sortedrots2[0] * sortedrots2[3])
                    if colcount - dist > 0:
                        grida[rowcount][colcount + dist][0] = grida[rowcount][colcount - dist][0] + (col[0] * sortedrots2[2] * sortedrots2[0])
                        grida[rowcount][colcount + dist][1] = grida[rowcount][colcount - dist][1] + (col[0] * sortedrots2[2] * sortedrots2[1])
                        grida[rowcount][colcount + dist][2] = grida[rowcount][colcount - dist][2] + (col[0] * sortedrots2[2] * sortedrots2[2])
                        grida[rowcount][colcount + dist][3] = grida[rowcount][colcount - dist][3] + (col[0] * sortedrots2[2] * sortedrots2[3])
                    if rowcount - dist > 0:
                        grida[rowcount][colcount + dist][0] = grida[rowcount - dist][colcount ][0] + (col[0] * sortedrots2[1] * sortedrots2[0])
                        grida[rowcount][colcount + dist][1] = grida[rowcount - dist][colcount ][1] + (col[0] * sortedrots2[1] * sortedrots2[1])
                        grida[rowcount][colcount + dist][2] = grida[rowcount - dist][colcount ][2] + (col[0] * sortedrots2[1] * sortedrots2[2])
                        grida[rowcount][colcount + dist][3] = grida[rowcount - dist][colcount ][3] + (col[0] * sortedrots2[1] * sortedrots2[3])
                    if rowcount + dist < 35:
                        grida[rowcount][colcount + dist][0] = grida[rowcount + dist][colcount ][0] + (col[0] * sortedrots2[3] * sortedrots2[0])
                        grida[rowcount][colcount + dist][1] = grida[rowcount + dist][colcount ][1] + (col[0] * sortedrots2[3] * sortedrots2[1])
                        grida[rowcount][colcount + dist][2] = grida[rowcount + dist][colcount ][2] + (col[0] * sortedrots2[3] * sortedrots2[2])
                        grida[rowcount][colcount + dist][3] = grida[rowcount + dist][colcount ][3] + (col[0] * sortedrots2[3] * sortedrots2[3])

                    # rot 1: the bot current facing up
                if col[1] > 0: # up
                    if colcount + dist < 35:
                        grida[rowcount][colcount + dist][0] = grida[rowcount][colcount + dist][0] + (col[1] * sortedrots2[3] * sortedrots2[0])
                        grida[rowcount][colcount + dist][1] = grida[rowcount][colcount + dist][1] + (col[1] * sortedrots2[3] * sortedrots2[1])
                        grida[rowcount][colcount + dist][2] = grida[rowcount][colcount + dist][2] + (col[1] * sortedrots2[3] * sortedrots2[2])
                        grida[rowcount][colcount + dist][3] = grida[rowcount][colcount + dist][3] + (col[1] * sortedrots2[3] * sortedrots2[3])
                    if colcount - dist > 0:
                        grida[rowcount][colcount + dist][0] = grida[rowcount][colcount - dist][0] + (col[1] * sortedrots2[0] * sortedrots2[0])
                        grida[rowcount][colcount + dist][1] = grida[rowcount][colcount - dist][1] + (col[1] * sortedrots2[0] * sortedrots2[1])
                        grida[rowcount][colcount + dist][2] = grida[rowcount][colcount - dist][2] + (col[1] * sortedrots2[0] * sortedrots2[2])
                        grida[rowcount][colcount + dist][3] = grida[rowcount][colcount - dist][3] + (col[1] * sortedrots2[0] * sortedrots2[3])
                    if rowcount - dist > 0:
                        grida[rowcount][colcount + dist][0] = grida[rowcount - dist][colcount ][0] + (col[1] * sortedrots2[1] * sortedrots2[0])
                        grida[rowcount][colcount + dist][1] = grida[rowcount - dist][colcount ][1] + (col[1] * sortedrots2[1] * sortedrots2[1])
                        grida[rowcount][colcount + dist][2] = grida[rowcount - dist][colcount ][2] + (col[1] * sortedrots2[1] * sortedrots2[2])
                        grida[rowcount][colcount + dist][3] = grida[rowcount - dist][colcount ][3] + (col[1] * sortedrots2[1] * sortedrots2[3])
                    if rowcount + dist < 35:
                        grida[rowcount][colcount + dist][0] = grida[rowcount + dist][colcount ][0] + (col[1] * sortedrots2[2] * sortedrots2[0])
                        grida[rowcount][colcount + dist][1] = grida[rowcount + dist][colcount ][1] + (col[1] * sortedrots2[2] * sortedrots2[1])
                        grida[rowcount][colcount + dist][2] = grida[rowcount + dist][colcount ][2] + (col[1] * sortedrots2[2] * sortedrots2[2])
                        grida[rowcount][colcount + dist][3] = grida[rowcount + dist][colcount ][3] + (col[1] * sortedrots2[2] * sortedrots2[3])
                if col[2] > 0: # left
                    if colcount + dist < 35:
                        grida[rowcount][colcount + dist][0] = grida[rowcount][colcount + dist][0] + (col[2] * sortedrots2[2] * sortedrots2[0])
                        grida[rowcount][colcount + dist][1] = grida[rowcount][colcount + dist][1] + (col[2] * sortedrots2[2] * sortedrots2[1])
                        grida[rowcount][colcount + dist][2] = grida[rowcount][colcount + dist][2] + (col[2] * sortedrots2[2] * sortedrots2[2])
                        grida[rowcount][colcount + dist][3] = grida[rowcount][colcount + dist][3] + (col[2] * sortedrots2[2] * sortedrots2[3])
                    if colcount - dist > 0:
                        grida[rowcount][colcount + dist][0] = grida[rowcount][colcount - dist][0] + (col[2] * sortedrots2[0] * sortedrots2[0])
                        grida[rowcount][colcount + dist][1] = grida[rowcount][colcount - dist][1] + (col[2] * sortedrots2[0] * sortedrots2[1])
                        grida[rowcount][colcount + dist][2] = grida[rowcount][colcount - dist][2] + (col[2] * sortedrots2[0] * sortedrots2[2])
                        grida[rowcount][colcount + dist][3] = grida[rowcount][colcount - dist][3] + (col[2] * sortedrots2[0] * sortedrots2[3])
                    if rowcount - dist > 0:
                        grida[rowcount][colcount + dist][0] = grida[rowcount - dist][colcount ][0] + (col[2] * sortedrots2[3] * sortedrots2[0])
                        grida[rowcount][colcount + dist][1] = grida[rowcount - dist][colcount ][1] + (col[2] * sortedrots2[3] * sortedrots2[1])
                        grida[rowcount][colcount + dist][2] = grida[rowcount - dist][colcount ][2] + (col[2] * sortedrots2[3] * sortedrots2[2])
                        grida[rowcount][colcount + dist][3] = grida[rowcount - dist][colcount ][3] + (col[2] * sortedrots2[3] * sortedrots2[3])
                    if rowcount + dist < 35:
                        grida[rowcount][colcount + dist][0] = grida[rowcount + dist][colcount ][0] + (col[2] * sortedrots2[1] * sortedrots2[0])
                        grida[rowcount][colcount + dist][1] = grida[rowcount + dist][colcount ][1] + (col[2] * sortedrots2[1] * sortedrots2[1])
                        grida[rowcount][colcount + dist][2] = grida[rowcount + dist][colcount ][2] + (col[2] * sortedrots2[1] * sortedrots2[2])
                        grida[rowcount][colcount + dist][3] = grida[rowcount + dist][colcount ][3] + (col[2] * sortedrots2[1] * sortedrots2[3])
                if col[3] > 0: # down
                    if colcount + dist < 35:
                        grida[rowcount][colcount + dist][0] = grida[rowcount][colcount + dist][0] + (col[3] * sortedrots2[1] * sortedrots2[0])
                        grida[rowcount][colcount + dist][1] = grida[rowcount][colcount + dist][1] + (col[3] * sortedrots2[1] * sortedrots2[1])
                        grida[rowcount][colcount + dist][2] = grida[rowcount][colcount + dist][2] + (col[3] * sortedrots2[1] * sortedrots2[2])
                        grida[rowcount][colcount + dist][3] = grida[rowcount][colcount + dist][3] + (col[3] * sortedrots2[1] * sortedrots2[3])
                    if colcount - dist > 0:
                        grida[rowcount][colcount + dist][0] = grida[rowcount][colcount - dist][0] + (col[3] * sortedrots2[3] * sortedrots2[0])
                        grida[rowcount][colcount + dist][1] = grida[rowcount][colcount - dist][1] + (col[3] * sortedrots2[3] * sortedrots2[1])
                        grida[rowcount][colcount + dist][2] = grida[rowcount][colcount - dist][2] + (col[3] * sortedrots2[3] * sortedrots2[2])
                        grida[rowcount][colcount + dist][3] = grida[rowcount][colcount - dist][3] + (col[3] * sortedrots2[3] * sortedrots2[3])
                    if rowcount - dist > 0:
                        grida[rowcount][colcount + dist][0] = grida[rowcount - dist][colcount ][0] + (col[3] * sortedrots2[2] * sortedrots2[0])
                        grida[rowcount][colcount + dist][1] = grida[rowcount - dist][colcount ][1] + (col[3] * sortedrots2[2] * sortedrots2[1])
                        grida[rowcount][colcount + dist][2] = grida[rowcount - dist][colcount ][2] + (col[3] * sortedrots2[2] * sortedrots2[2])
                        grida[rowcount][colcount + dist][3] = grida[rowcount - dist][colcount ][3] + (col[3] * sortedrots2[2] * sortedrots2[3])
                    if rowcount + dist < 35:
                        grida[rowcount][colcount + dist][0] = grida[rowcount + dist][colcount ][0] + (col[3] * sortedrots2[0] * sortedrots2[0])
                        grida[rowcount][colcount + dist][1] = grida[rowcount + dist][colcount ][1] + (col[3] * sortedrots2[0] * sortedrots2[1])
                        grida[rowcount][colcount + dist][2] = grida[rowcount + dist][colcount ][2] + (col[3] * sortedrots2[0] * sortedrots2[2])
                        grida[rowcount][colcount + dist][3] = grida[rowcount + dist][colcount ][3] + (col[3] * sortedrots2[0] * sortedrots2[3])




if __name__ == "__main__":
    global botrot
    global grid
    global grida
    rospy.init_node('rviz_pub_example')

    # Rviz is a node that can subscribe to topics of certain message types.
    # Here we use the Marker message type and create two publishers
    # to display the robot trejectory as a list of lines(MARKER.LINE_LIST)
    # and display the landmarks as a list of cubes (MARKER.CUBE_LIST)
    # Make sure you in rviz you subsribe to these topics in rviz by clicking
    # on Add in the display panel, selecting by topic and choosing the
    # appropraite topic.

    # Initilize a publisher for LINE_LIST makers
    pub_line_list = rospy.Publisher('line_list', Marker, queue_size=1)

    # Initilize a publisher for CUBE_LIST makers
    pub_cube_list = rospy.Publisher('cube_list', Marker, queue_size=1)

    # Example Input: Set of points to draw a square
    line_points = [(0,0), (0,0.5), (0,0.5), (0.5,0.5), (0.5,0.5), (0.5,0), (0.5,0), (0,0)]
    botspots = [(2,2,0),(0,0,0,0)]
    # Example Input: Set of cubes at four positions
    cube_points = [(0,0), (0,1), (1,0), (1,1) , (2,0), (2,2)]
    count = 0
    count2 = 0
    bag = rosbag.Bag('grid.bag')
    botpos = [(0,0)]
    #
    # while count2 < 50:
    #     for topic, msg, t in bag.read_messages(topics=[ 'Movements']):
    #         if count < 50:
    #             # print("Observations: ", msg.timeTag, " ", msg.tagNum," ", msg.range," ", msg.bearing.x," ", msg.bearing.y," ", msg.bearing.z," ", msg.bearing.w)
    #             # line_points.append((line_points[count][0] + (round(msg.rotation1.z,1)),line_points[count][1] +  round(msg.rotation1.w,1)))
    #             # count = count + 1
    #
    #             newxy = quattest(msg.rotation1)
    #             botpos.append((botpos[count][0] + (newxy[0] * msg.translation ),botpos[count][1] +  (newxy[1] * msg.translation )))
    #             line_points.append((botpos[count][0] + (newxy[0] * msg.translation ),botpos[count][1] +  (newxy[1] * msg.translation )))
    #             # setbotrot(msg.rotation2)
    #             count = count + 1
    #     count2 = count2 + 1

    count = 0
    grid = []
    grida = []

    # NOTE: for movement multiople translation by 5, result in numbert of squares distance
    while count < 36:
        grid2 = []
        grid.append(grid2)
        gridb = []
        grida.append(gridb)
        count = count + 1
        count2 = 0
        while count2 < 36:
            grid3 = [0,0,0,0] # the 4 possible rotations that could be in the square
            gridc = [0,0,0,0]
            grid2.append(grid3)
            gridb.append(gridc)
            count2 = count2 + 1
    grid[4][2] = [1,1,1,1]
    grid[14][5] = [1,1,1,1]
    grid[22][2] = [1,1,1,1]
    for topic, msg, t in bag.read_messages(topics=[ 'Movements']):
        test(msg)
    # print(grida)
    # Call the display functions in a loop to see the markers on rviz over time
    while not rospy.is_shutdown():
        display_line_list(line_points, pub_line_list)
        display_cube_list(cube_points, pub_cube_list)
