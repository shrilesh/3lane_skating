l1_red_start=22
l1_green_start=16
l1_blue_start=18
l1_blue_stop=24
l1_start_sensor_pin=5
l1_end_sensor_pin=11
l1_start = False
l1_stop = False
state_align  = False
state_initialize = False
start_timer = True
start_endtimer = True
lebBlinker = True
state_lane1 =2
l1_red_stop=31
l1_green_stop=29
state_power=1
state_timer = False
state_lane2=2
state_lane3=2
l2_red_start=10
l2_red_stop=12
l2_green_start=13
l2_green_stop=15
l2_blue_start=19
l2_blue_stop=21
l2_start_sensor_pin=7
l2_end_sensor_pin=8
l3_red_start=32
l3_red_stop=33
l3_green_start=35
l3_green_stop=36
l3_blue_start=37
l3_blue_stop=38
l3_start_sensor_pin=23
l3_end_sensor_pin=26
stop_lane1_thread = False
stop_lane2_thread = False
stop_lane3_thread = False
p1=None
p2=None
p3=None

allRedLow = [l1_red_start,l1_red_stop,l2_red_start,l2_red_stop,l3_red_start,l3_red_stop]
allGreenLow = [l1_green_start,l1_green_stop,l2_green_start,l2_green_stop,l3_green_start,l3_green_stop]
allBlueLow = [l1_blue_start,l1_blue_stop,l2_blue_start,l2_blue_stop,l3_blue_start,l3_blue_stop]
l1_green_blue = [l1_green_start,l1_green_stop,l1_blue_start,l1_blue_stop]
l1_green_red = [l1_green_start,l1_green_stop,l1_red_start,l1_red_stop,l1_blue_stop]





