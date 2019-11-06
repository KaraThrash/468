#!/usr/bin/python
import rospy
import numpy as np
import rosbag
import sys
from tf.transformations import euler_from_quaternion
from math import sqrt
import math
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
import sys

#CONSTANTS
BAG_PREFIX = 0
bag = rosbag.Bag('grid.bag')
topics = []
topics.append('Motion')
topics.append('Observation')
pt_count = 0
DEG_TO_RADS = 0.0174532925
PLOT_DOWNSIZE = 50.0
##NOISE
MOV_NOISE_MEAN = 0.0
MOV_NOISE_VAR = 10.0
MOV_NOISE_STDDEV = sqrt(MOV_NOISE_VAR)
GAUSSIAN_PREFIX_MOV = 1.0/(math.sqrt(2*math.pi)*MOV_NOISE_STDDEV)
ROT_NOISE_VAR = 5.0 * DEG_TO_RADS
ROT_NOISE_MEAN = 0.0
GAUSSIAN_PREFIX_ROT = 1.0/(math.sqrt(2*math.pi*(ROT_NOISE_VAR)))
#print "-------------CONSTANTS---------------------------"
#print GAUSSIAN_PREFIX_MOV
#print GAUSSIAN_PREFIX_ROT


#Tag POSITIONS
tag_positions = np.ndarray((6,),dtype=np.object)
#Tag number 0 : x = 1.25m, y = 5.25m
#Tag number 1 : x = 1.25m, y = 3.25m
#Tag number 2 : x = 1.25m, y = 1.25m
#Tag number 3 : x = 4.25m, y = 1.25m
#Tag number 4 : x = 4.25m, y = 3.25m
#Tag number 5 : x = 4.25m, y = 5.25m

#700/20 cm * 700/20 cm * 360/10
grid = np.zeros((35,35,36))
CONT_THRESH = 0.08#(1.0/44100)#1/(35*35*36)

#grid = grid*(1/(35*35*36))

##init grid start position to 1
##ROBOT INIT POS
#(12,28,20)
grid[11][27][20]=1.0


class Grid_centre_class:
	#z is thetha
	x = 0.0
	y = 0.0
	z = 0.0
	def __init__(self,x,y,z):
		self.x = x
		self.y = y
		self.z = z
	def __str__(self):
     		return "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"
	pass

class Motion_model_unit:
	rotation1 = 0.0
	translation = 0.0
	rotation2 = 0.0
	def __init__(self,rotation1,translation,rotation2):
		self.rotation1 = rotation1
		self.translation = translation
		self.rotation2 = rotation2

	def __str__(self):
     		return "(r1:" + str(self.rotation1) + ", trans:" + str(self.translation) + ", r2:" + str(self.rotation2) + ")"
	pass

class Observation_unit:
	tagNum = 0.0
	range_vbl = 0.0
	bearing = 0.0
	def __init__(self,tagNum,range_vbl,bearing):
		self.tagNum = tagNum
		self.range_vbl = range_vbl
		self.bearing = bearing

	def __str__(self):
     		return "(tagNum:" + str(self.tagNum) + ", range:" + str(self.range_vbl) + ", bearing:" + str(self.bearing) + ")"
	pass

grid_centres = np.ndarray(grid.shape,dtype=np.object)
def init_grid():
	global grid_centres
	for i in range(grid.shape[0]):
		for j in range(grid.shape[1]):
			for k in range(grid.shape[2]):
				grid_centres[i][j][k] = Grid_centre_class(i*20+10,j*20+10,k*10*DEG_TO_RADS)
def init_tag_positions():
		tag_positions[0] = Grid_centre_class(125,525,0)
		tag_positions[1] = Grid_centre_class(125,325,0)
		tag_positions[2] = Grid_centre_class(125,125,0)
		tag_positions[3] = Grid_centre_class(425,125,0)
		tag_positions[4] = Grid_centre_class(425,325,0)
		tag_positions[5] = Grid_centre_class(425,525,0)

def print_grid_centres():
	global grid_centres
	for i in range(grid.shape[0]):
		for j in range(grid.shape[1]):
			for k in range(grid.shape[2]):
				print str(grid_centres[i][j][k].x) + "," + str(grid_centres[i][j][k].y) + "," + str(grid_centres[i][j][k].z)

#to,from
def get_required_rotation(line_angle,pose_cell_theta):
	if(pose_cell_theta - line_angle > 0 and pose_cell_theta - line_angle < math.pi ):
		 return -1*(math.pi - abs(abs(line_angle - pose_cell_theta) - math.pi))
	else:
		 return (math.pi - abs(abs(line_angle - pose_cell_theta) - math.pi))

def get_min_rotation(line_angle, cell_pose, act):
	diff = line_angle - cell_pose
	if diff<0:
		diff = diff + (2*math.pi)
	else:
		diff = (2*math.pi) -diff
	return diff



def dump_grid_to_file():
	f = open("grid_dump.txt", "wb")
	for i1 in range(grid.shape[0]):
		for j1 in range(grid.shape[1]):
			for k1 in range(grid.shape[2]):
				f.write(str(i1) + "," + str(j1) + "," + str(k1) +":" + str(grid[i1][j1][k1]) + "\n")
				#f.write("(" + str(grid[i1][j1][k1].x) + "," + str(grid[i1][j1][k1].y) + "," + str(grid[i1][j1][k1].z + ")"))
def draw_tags(pub):

	global pt_count
	tag_pos_marker = Marker()
	tag_pos_marker.header.frame_id = "/base_link"
	tag_pos_marker.header.stamp = rospy.Time.now()
	tag_pos_marker.action = Marker.ADD
	tag_pos_marker.scale.x = 0.6;
	tag_pos_marker.scale.y = 0.6;
	tag_pos_marker.scale.z = 0.6;
	tag_pos_marker.color.a = 1.0;
	tag_pos_marker.color.r = 0.0;
	tag_pos_marker.color.g = 0.0;
	tag_pos_marker.color.b = 1.0;
	tag_pos_marker.ns = "tags"
	tag_pos_marker.type = Marker.POINTS
	tag_pos_marker.id = pt_count
	pt_count +=1
	for zz in range(6):
		tag_pos_point = Point()

       		tag_pos_point.x = tag_positions[zz].x/PLOT_DOWNSIZE#100.0
	        tag_pos_point.y = tag_positions[zz].y/PLOT_DOWNSIZE#100.0
	       	tag_pos_point.z = 0
	       	tag_pos_marker.points.append(tag_pos_point)
	#print "Publisginh tags"
	pub.publish(tag_pos_marker)


def do_localize():

	global grid, grid_centres, CONT_THRESH, pt_count
	bag_msgs = list(bag.read_messages(topics=['Movements','Observations']))
	bag_msgs.reverse()
	act_move = None
	obs_msg = None
	cached_pt = Point()
	cached_pt.x = grid_centres[11][27][20].x/PLOT_DOWNSIZE#100.0
	cached_pt.y = grid_centres[11][27][20].y/PLOT_DOWNSIZE#100.0
	msg_count = 0
	while msg_count<3:
		topic, msg, time_stamp = bag_msgs.pop()
		if(msg==None):
			break
		if topic == 'Movements':
			#print euler_from_quaternion((msg.rotation1.x,msg.rotation1.y,msg.rotation1.z,msg.rotation1.w))[2]
			act_move = Motion_model_unit(euler_from_quaternion((msg.rotation1.x,msg.rotation1.y,msg.rotation1.z,msg.rotation1.w))[2], msg.translation*100.0, euler_from_quaternion((msg.rotation2.x,msg.rotation2.y,msg.rotation2.z,msg.rotation2.w))[2])
		topic = None
		msg = None
		time_stamp = None
		try:
			msg_count +=1
			topic, msg, time_stamp = bag_msgs.pop()
		except IndexError:
			return
		if topic == 'Observations':
			obs_msg = Observation_unit(msg.tagNum, msg.range*100, euler_from_quaternion((msg.bearing.x,msg.bearing.y,msg.bearing.z,msg.bearing.w))[2])
		print "Mov from bag:" + str(act_move)
		print "Obs from bag:" + str(obs_msg)
		new_probs = np.zeros(grid.shape,dtype=np.float64)
		for i1 in range(grid.shape[0]):
			for j1 in range(grid.shape[1]):
                        	for k1 in range(grid.shape[2]):
					#print grid[i1][j1][k1]
					#print CONT_THRESH
					#if grid[i1][j1][k1] != 0:
					#	print "Pass"
					if(grid[i1][j1][k1]<(CONT_THRESH)):
						continue
					#print "Evaluating"
					src_centre = grid_centres[i1][j1][k1]
					for i2 in range(grid.shape[0]):
						for j2 in range(grid.shape[1]):
                	        			for k2 in range(grid.shape[2]):
								if i1==i2 and j1==j2 and k1==k2 :
									continue
								dest_centre = grid_centres[i2][j2][k2]
								#print "dest:" + str(dest_centre)
								#print "src:" + str(src_centre)
								#Calculate trans
								cal_trans = math.sqrt((dest_centre.y - src_centre.y)**2 + (dest_centre.x - src_centre.x)**2)
								z_heading = math.atan2((dest_centre.y - src_centre.y),(dest_centre.x - src_centre.x))# + sys.float_info.epsilon))
								if z_heading<0:
									z_heading = 2*math.pi - abs(z_heading)
								#print "z_heading:" + str(z_heading)
								#Calcuate r1
								cal_r1 = get_required_rotation(z_heading, src_centre.z)

								#Calculate r2
								cal_r2 = get_required_rotation(dest_centre.z, z_heading)
								#print "------------cal_r1, cal_r2, cal_trans------------------------"
								#print cal_r1
								#print cal_r2
								#print cal_trans
								#raw_input("Press key to continue")

								error_r1 = cal_r1 - act_move.rotation1
								error_trans = cal_trans - act_move.translation
								error_r2 = cal_r2 - act_move.rotation2
								prob_r1 = GAUSSIAN_PREFIX_ROT*math.exp(-(error_r1**2)/(2*ROT_NOISE_VAR))
								prob_t = GAUSSIAN_PREFIX_MOV*math.exp(-(error_trans**2)/(2*MOV_NOISE_VAR))
								prob_r2 = GAUSSIAN_PREFIX_ROT*math.exp(-(error_r2**2)/(2*ROT_NOISE_VAR))
								#print "---------errors and probs--------------------------------------"
								#print error_r1
								#print error_trans
								#print error_r2
								#print prob_r1
								#print prob_t
								#print prob_r2
								new_probs[i2][j2][k2] +=  grid[i1][j1][k1]*(prob_r1 * prob_t * prob_r2)
		grid = new_probs
		#dump_grid_to_file()
		#raw_input("Press key to continue")
		#print "Correcting wrt Markers"
		print "Max prob after movement:" + str(np.amax(grid))
		#print np.argmax(grid)
		max_prob = np.unravel_index(np.argmax(grid), grid.shape)
		print "Max_prob at:" + str(max_prob)
		#Update wrt Observation
		prob_obs = np.zeros((grid.shape))
		for i1 in range(grid.shape[0]):
			for j1 in range(grid.shape[1]):
                        	for k1 in range(grid.shape[2]):
					src_pos = grid_centres[i1][j1][k1]
					tag_pos = tag_positions[obs_msg.tagNum]
					#print src_pos
					#print tag_pos
					#calculate range
					cal_range = math.sqrt((tag_pos.y - src_pos.y)**2 + (tag_pos.x - src_pos.x)**2)
					#calculate bearing
					z_heading = math.atan2((tag_pos.y-src_pos.y),(tag_pos.x-src_pos.x))
					if z_heading<0:
						z_heading = 2*math.pi - abs(z_heading)
					cal_bearing = get_required_rotation(z_heading, src_pos.z)#z_heading - src_pos.z
					#if cal_bearing > math.pi:
					#	cal_bearing = cal_bearing - (2*math.pi)
					#elif cal_bearing < -math.pi:
					#	cal_bearing = (2*math.pi) - cal_bearing

					error_range = cal_range - obs_msg.range_vbl
					error_bearing = cal_bearing - obs_msg.bearing
					#print "err_range:" + str(error_range)
					#print "err_beaering:" + str(error_bearing)
					prob_range = GAUSSIAN_PREFIX_MOV*math.exp(-(error_range**2)/(2*MOV_NOISE_VAR))
					prob_bearing = GAUSSIAN_PREFIX_ROT*math.exp(-(error_bearing**2)/(2*ROT_NOISE_VAR))
					#print "prob_range:" + str(prob_range)
					#print "prob_beating:" + str(prob_bearing)
					#raw_input("Press key to continue")
					prob_obs[i1][j1][k1] = prob_range * prob_bearing
					grid[i1][j1][k1] = grid[i1][j1][k1]*(prob_range * prob_bearing)
		normalization = np.sum(grid)
		grid = grid/normalization
		print "Max prob:" + str(np.amax(grid))
		#print np.argmax(grid)
		max_prob = np.unravel_index(np.argmax(grid), grid.shape)
		print "Max_prob at:" + str(max_prob)
		global pt_count


		#line strip marker
		line_strip = Marker()
		line_strip.header.frame_id = "/base_link"
		line_strip.header.stamp = rospy.Time.now()
		line_strip.action = Marker.ADD
		line_strip.lifetime = rospy.Time(0)
		line_strip.scale.x = 0.1;
		line_strip.scale.y = 0.1;
		line_strip.scale.z = 0.1;
		line_strip.color.a = 1.0;
		line_strip.color.r = 0.0;
		line_strip.color.g = 1.0;
		line_strip.color.b = 0.0;
		line_strip.ns = "pts_line"
		line_strip.id = (pt_count)
		line_strip.type = Marker.LINE_STRIP
		p1 = Point()
		p1.x = grid_centres[max_prob[0]][max_prob[1]][max_prob[2]].x/PLOT_DOWNSIZE#100.0
		p1.y = grid_centres[max_prob[0]][max_prob[1]][max_prob[2]].y/PLOT_DOWNSIZE#100.0

		line_strip.points.append(p1)
		line_strip.points.append(cached_pt)

		pub.publish(line_strip)
		rospy.sleep(rospy.Duration(10))
		draw_tags(pub)

		cached_pt = p1







if __name__ == '__main__':
	rospy.init_node("localizer")
	#init grid
	init_grid()
	init_tag_positions()

	pub = rospy.Publisher("/visualization_topic", Marker, queue_size=1)
	do_localize()
	rospy.spin()
