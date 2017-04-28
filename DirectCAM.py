#Direct_Cam_ver_0.3.py

####################################
### running parameters
####################################
TOOL_DIAMETER=0.125
DRILL_PLUNGE_FEED_RATE = 2
HOME_X=0
HOME_Y=0
SAFE_HEIGHT=0.6

####################################
### CAM details
####################################
CUT_STEP_DEPTH=0.02
CUT_FACING_LAYER=0.02
DRILL_STEP_DEPTH=0.04
#lateral_overlap_PCT=0.5



####################################
### calculated quantities
####################################
#CUT_STEP_LATERAL=lateral_overlap_PCT*TOOL_DIAMETER
CUT_STEP_LATERAL=CUT_FACING_LAYER
CUT_PITCH_SIZE=CUT_STEP_DEPTH
TOOL_RADIUS = TOOL_DIAMETER/2
#cut_pitches=ceil(cut_depth/CUT_STEP_DEPTH)
#cut_radius = cut_diameter/2



####################################
### cut a helix function
####################################
def Helix_Cut(cut_center_x,cut_center_y,starting_z,cut_depth,cut_radius):
	CUT_PITCH_SIZE = CUT_STEP_DEPTH
	final_z=starting_z-cut_depth
	while (starting_z>final_z+CUT_PITCH_SIZE):
		Pitch_Cut(cut_center_x,cut_center_y,starting_z,CUT_PITCH_SIZE,cut_radius)
		starting_z=starting_z-CUT_PITCH_SIZE
	Pitch_Cut(cut_center_x,cut_center_y,starting_z,starting_z-final_z,cut_radius)
	Pitch_Cut(cut_center_x,cut_center_y,final_z,0,cut_radius)

####################################
### cut a pitch function
####################################
def Pitch_Cut(cut_center_x,cut_center_y,starting_z,cut_pitch_depth,cut_radius):
	#COMPENSATION
	# ADD GLOBAL parameter ???
	#cut_radius=cut_radius-TOOL_RADIUS
	#if cut_radius<0:
	#	print ("warning radius compansaion has resulted in NEGATIVE radius tool too large")
	starting_x = cut_center_x
	starting_y = cut_center_y+cut_radius

	print "G0 x{:.4f} y{:.4f} z{:.4f}".format(starting_x,starting_y,starting_z)
	print "G17"
	print "G2 X{:.4f} Y{:.4f} Z{:.4f} I{:.4f} J{:.4f}".format(starting_x,starting_y,starting_z-cut_pitch_depth,0,-1*cut_radius)

####################################
### drill a hole function
####################################
def Drill_Plunge(cut_center_x,cut_center_y,starting_z,bottom_z):
	print "G0 x{:.4f} y{:.4f} z{:.4f}".format(cut_center_x,cut_center_y,starting_z)
	print "G1 X{:.4f} Y{:.4f} z{:.4f} f{:.4f}".format(cut_center_x,cut_center_y,bottom_z,DRILL_PLUNGE_FEED_RATE)
	print "G0 x{:.4f} y{:.4f} z{:.4f}".format(cut_center_x,cut_center_y,starting_z)

####################################
### drill a hole carefully removing material function
####################################
def Drill_MultiPlunge(cut_center_x,cut_center_y,starting_z,bottom_z):
	print "G0 x{:.4f} y{:.4f} z{:.4f}".format(cut_center_x,cut_center_y,starting_z)
	z=starting_z-DRILL_STEP_DEPTH
	while(z>bottom_z):
		print "G1 x{:.4f} y{:.4f} z{:.4f} f{:.4f}".format(cut_center_x,cut_center_y,z,DRILL_PLUNGE_FEED_RATE)
		print "G0 x{:.4f} y{:.4f} z{:.4f}".format(cut_center_x,cut_center_y,starting_z)
		z=z-DRILL_STEP_DEPTH
	z=bottom_z
	print "G1 x{:.4f} y{:.4f} z{:.4f} f{:.4f}".format(cut_center_x,cut_center_y,z,DRILL_PLUNGE_FEED_RATE)
	print "G0 x{:.4f} y{:.4f} z{:.4f}".format(cut_center_x,cut_center_y,starting_z)

####################################
### Go to Safe Hight
####################################
def Go_High():
	print "G0 z{:.4f}".format(SAFE_HEIGHT)

####################################
### Go Home
####################################
def Go_Home():
	Go_High()
	print "G0 x{:.4f} y{:.4f} z{:.4f}".format(HOME_X,HOME_Y,SAFE_HEIGHT)



#####################################
### Cut hole Function
#####################################

def Hole_cut(cut_center_x,cut_center_y,starting_z,bottom_z,cut_diameter):
	#get tool path radius
	cut_radius = cut_diameter/2
	cut_radius=cut_radius-TOOL_RADIUS
	cut_depth=starting_z-bottom_z
	#CUT_PITCH_SIZE=CUT_PITCH_SIZE

	###Open the center of the bore
	Drill_MultiPlunge(cut_center_x,cut_center_y,starting_z,bottom_z)


	#####################################
	### machine hole from inside to out
	#####################################
	current_radius=1.0*CUT_STEP_LATERAL
	while (current_radius<cut_radius):
		Helix_Cut(cut_center_x,cut_center_y,starting_z,cut_depth,current_radius)
		current_radius=current_radius+CUT_STEP_LATERAL
	####################################

	### finish hole to exact diameter
	Helix_Cut(cut_center_x,cut_center_y,starting_z,cut_depth,cut_radius)


#####################################
### Cut hole carefully Function
#####################################

def Hole_cut_layered(cut_center_x,cut_center_y,starting_z,bottom_z,cut_diameter):
	#get tool path radius
	cut_radius = cut_diameter/2
	cut_depth=starting_z-bottom_z

	#CUT_PITCH_SIZE=CUT_PITCH_SIZE

	#####################################
	### machine hole from inside to out
	#####################################
	old_z=starting_z
	z=starting_z-CUT_STEP_DEPTH
	while(z>bottom_z):
		Hole_cut(cut_center_x,cut_center_y,old_z,z,cut_diameter)
		old_z=z
		z=z-CUT_STEP_DEPTH
	if(z<bottom_z):
		z=bottom_z
		Hole_cut(cut_center_x,cut_center_y,old_z,z,cut_diameter)
	Go_High()


#COMING SOON!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#####################################
### Cartesian Pitch cut row
#####################################
def Lap_cut_x(x_min,x_max,y,cut_step_lateral,z):
	print "G1 x{:.4f} y{:.4f} z{:.4f}".format(x_min,y,z)
	print "G1 x{:.4f} y{:.4f} z{:.4f}".format(x_max,y,z)
	print "G1 x{:.4f} y{:.4f} z{:.4f}".format(x_max,y+cut_step_lateral,z)
	print "G1 x{:.4f} y{:.4f} z{:.4f}".format(x_min,y+cut_step_lateral,z)

#####################################
### Cartesian Pitch cut column
#####################################
def Lap_cut_y(y_min,y_max,x,cut_step_lateral,z):
	print "G1 x{:.4f} y{:.4f} z{:.4f}".format(x,y_min,z)
	print "G1 x{:.4f} y{:.4f} z{:.4f}".format(x,y_max,z)
	print "G1 x{:.4f} y{:.4f} z{:.4f}".format(x+cut_step_lateral,y_max,z)
	print "G1 x{:.4f} y{:.4f} z{:.4f}".format(x+cut_step_lateral,y_min,z)

#####################################
### Z face
#####################################
def Z_Face(x_min,x_max,y_min,y_max,z_min,z_start):
	#Go_High()
	#print "G0 x{:.4f} y{:.4f} z{:.4f}".format(x_min,y_min,SAFE_HEIGHT)
	print "G0 x{:.4f} y{:.4f} z{:.4f}".format(x_min,y_min,z_start)
	z = z_start
	while(z>z_min):
		z=z-CUT_FACING_LAYER
		if (z<z_min):
			z=z_min
		y=y_min
		while(y<y_max):
			Lap_cut_x(x_min,x_max,y,CUT_STEP_LATERAL,z)
			y=y+2.0*CUT_STEP_LATERAL
		y=y_max-CUT_STEP_LATERAL
		Lap_cut_x(x_min,x_max,y,CUT_STEP_LATERAL,z)

#####################################
### perimeter face
#####################################
def Perimeter_Face(end_1_x,end_1_y,end_2_x,end_2_y,face_dir_x,face_dir_y,starting_clerance,top_z,bottom_z):
	delta_x=abs(end_2_x-end_1_x)
	delta_y=abs(end_2_y-end_1_y)
	hyp=(delta_x^2+delta_y^2)
	clerance=starting_clerance
	while(clerance>0):
		x_offset=clerance*(delta_y/hyp)*face_dir_x
		y_offset=clerance*(delta_x/hyp)*face_dir_y
		Perimeter_Face_Layer(end_1_x+x_offset,end_1_y+y_offset,end_2_x+x_offset,end_2_y+y_offset,face_dir_x,face_dir_y,top_z,bottom_z)
		clerance=clerance-CUT_STEP_LATERAL
	Perimeter_Face_Layer(end_1_x,end_1_y,end_2_x,end_2_y,face_dir_x,face_dir_y,top_z,bottom_z)

#####################################
### perimeter face Layer
#####################################
def Perimeter_Face_Layer(end_1_x,end_1_y,end_2_x,end_2_y,face_dir_x,face_dir_y,top_z,bottom_z):
	delta_x=abs(end_2_x-end_1_x)
	delta_y=abs(end_2_y-end_1_y)
	hyp=(delta_x^2+delta_y^2)
	x_offset=TOOL_RADIUS*(delta_y/hyp)*face_dir_x
	y_offset=TOOL_RADIUS*(delta_x/hyp)*face_dir_y
	Trench_cut(end_1_x+x_offset,end_1_y+y_offset,end_2_x+x_offset,end_2_y+y_offset,top_z,bottom_z)


#####################################
### Trench
#####################################
def Trench_cut(end_1_x,end_1_y,end_2_x,end_2_y,top_z,bottom_z):
	z=top_z
	while(z>bottom_z):
		Trench_Pitch_Cut(end_1_x,end_1_y,end_2_x,end_2_y,z,CUT_STEP_DEPTH)
		z=z-2*CUT_STEP_DEPTH
	Trench_Pitch_Cut(end_1_x,end_1_y,end_2_x,end_2_y,bottom_z+CUT_STEP_DEPTH,CUT_STEP_DEPTH)


def Trench_Pitch_Cut(end_1_x,end_1_y,end_2_x,end_2_y,starting_z,cut_pitch_depth):
	print "G1 x{:.4f} y{:.4f} z{:.4f}".format(end_1_x,end_1_y,starting_z)
	print "G1 x{:.4f} y{:.4f} z{:.4f}".format(end_2_x,end_2_y,starting_z)
	print "G1 x{:.4f} y{:.4f} z{:.4f}".format(end_2_x,end_2_y,starting_z-cut_pitch_depth)
	print "G1 x{:.4f} y{:.4f} z{:.4f}".format(end_1_x,end_1_y,starting_z-cut_pitch_depth)


#####################################
### Square hole
#####################################
def Rectangular_Hole(x_min,x_max,y_min,y_max,z_min,z_start):
	x_min=x_min+TOOL_RADIUS
	x_max=x_max-TOOL_RADIUS
	y_min=y_min+TOOL_RADIUS
	y_max=y_max-TOOL_RADIUS
	Z_Face(x_min,x_max,y_min,y_max,z_min,z_start)
	z=z_start
	while(z>z_min):
		Lap_cut_y(y_min,y_max,x_min,CUT_STEP_LATERAL,z)
	Lap_cut_y(y_min,y_max,x_min,CUT_STEP_LATERAL,z_min)
	z=z_start
	while(z>z_min):
		Lap_cut_y(y_min,y_max,x_max,CUT_STEP_LATERAL,z)
	Lap_cut_y(y_min,y_max,x_max,CUT_STEP_LATERAL,z_min)

###################################################################################
#####################################
###G code genrating code here
#####################################
###################################################################################

####################################
### CAD details and high level code for design of piece
####################################

x_min = 0
x_max = 2
y_min = 0
y_max = 2
z_min = 0.5
z_start = 0.6
Z_Face(x_min,x_max,y_min,y_max,z_min,z_start)


cut_center_x = 1
cut_center_y = 1
cut_diameter = 0.5
starting_z=0.55
bottom_z=0
Hole_cut_layered(cut_center_x,cut_center_y,starting_z,bottom_z,cut_diameter)


####################################################################################
