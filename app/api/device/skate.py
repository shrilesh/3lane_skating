
# import RPi.GPIO as GPIO
# from constants import *


# def boardSetup(led_pins, sensor_pins) {
# 	GPIO.setwarnings(False)
# 	GPIO.setmode(GPIO.BOARD)

# 	GPIO.setup(sensor_pins["l1_start"], GPIO.IN, pull_up_down = GPIO.PUD_UP)#start sensor
# 	GPIO.setup(sensor_pins["l1_stop"], GPIO.IN, pull_up_down = GPIO.PUD_UP)#stop sensor

	# GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP)#stop sensor
	# GPIO.setup(16, GPIO.OUT)#green
	# GPIO.setup(18, GPIO.OUT)#blue
	# GPIO.setup(24, GPIO.OUT)#blue
	# GPIO.setup(22, GPIO.OUT)#red
	# GPIO.output(16, GPIO.LOW)#green
	# GPIO.output(18, GPIO.LOW)#blue
	# GPIO.output(24, GPIO.LOW)
	# GPIO.output(22, GPIO.LOW)#red
# }


# System States - 
# 	1. on 		system
#	2. align 	system
# 	3. ready 	lane
# 	4. running 	lane

# Functions
# LED control. Arguments - 1. state (stable, blinking), 2. LED Pin
# Interrupts
# def allPodLEDsOff(lane, line):
# 	pod_leds = [led for led in led_pins if led["lane"] == lane and led["line"] == line]
# 	for led in pod_leds:
# 		ledControl("stable", lane, line, led["color"], False)

# def ledControl(state, lane, line, color, status):
# 	if state is "stable":
# 		if status:
# 			GPIO.output([pin for pin in led_pins if pin["lane"] == lane and pin["line"] == line and pin["color"] == color][0]["pin_no"], GPIO.HIGH)
# 		else:
# 			GPIO.output([pin for pin in led_pins if pin["lane"] == lane and pin["line"] == line and pin["color"] == color][0]["pin_no"], GPIO.LOW)
# 	else:
# 		print "Starting thread"
# 		# Start blinking thread

# def allLEDsOff():
# 	allPodLEDsOff(1, "start")
# 	allPodLEDsOff(1, "stop")
# 	allPodLEDsOff(2, "start")
# 	allPodLEDsOff(2, "stop")
# 	allPodLEDsOff(3, "start")
# 	allPodLEDsOff(3, "stop")

# ledControl("stable", 1, "start", "red", False)
# # Power ON
# # Setup Board
# boardSetup(led_pins, sensor_pins)

# Red Stable

# Align POST call
# attach interrupts for 6 sensors to detect change of value
# 	if state changes, change state of LEDs accordingly
# check alignment state of 6 sensors
# if aligned, blue stable
# if misaligned, blue blinking 

# Initialize POST call
# Check if all sensors are aligned, else do nothing, show error message on frontend - "Sensors are not aligned. Failed to Initialize"
# keep interrupts attached
# Since all sensors are aligned, no threads will be running, since all sensors will be stable blue
# Start 6 Green blinking threads, with an independent global control variable for each 
# Stop thread, and make green sensor stable when Interrupt is detected - check the state of the system in the interrupts

