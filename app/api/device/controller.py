from app import app, socketio, db
from flask import Response, request
from constants import *
from boardSetup import *
import json
from bson import json_util
import RPi.GPIO as GPIO,eventlet,greenlet,gevent
import time
import sys
import os
import threading
import multiprocessing
from multiprocessing import Pool,Process
from signal import signal,SIGTERM
from functions import *
from pymongo import MongoClient
from gevent import monkey
monkey.patch_all()

#Functionality of Code:

#This code I developed for any 3 lane game in which players data needed to record at start line and stop line.
#Change in state usually e.g alignment of sensor is given in terms of LED notifications to real world.
#Timing data e.g Start of time and stop time of player is maintained on front end using java script.
# UI(web page) is made to print real time data on monitor/TV 


## System States - 
# 	1. on 		system
#	2. align 	system
# 	3. ready 	lane
# 	4. running 	lane


# Align POST call
# attach interrupts for 6 sensors to detect change of value
# 	if state changes, change state of LEDs accordingly
# check alignment state of 6 sensors
# if sensors are misalinged before align post call , leds will glow red
# if aligned, blue stable
# if misaligned, blue blinking
def alignPod1():
	global state_align
	if  GPIO.input(l1_start_sensor_pin)  == 0:
		GPIO.output(l1_red_start, GPIO.HIGH)
		for i in l1_green_blue:
			GPIO.output(i,GPIO.LOW)
	else:
		GPIO.output(l1_blue_start, GPIO.HIGH)
		GPIO.wait_for_edge(l1_start_sensor_pin,GPIO.FALLING)
		while not state_align:
			if GPIO.input(l1_start_sensor_pin) == 0:
				GPIO.output(l1_blue_start, GPIO.HIGH)
				time.sleep(0.25)
				GPIO.output(l1_blue_start, GPIO.LOW)
				time.sleep(0.25)
				for i in l1_green_red:
					GPIO.output(i,GPIO.LOW)

			elif GPIO.input(l1_start_sensor_pin)==1:
				GPIO.output(l1_blue_start, GPIO.HIGH)
				for i in l1_green_red:
					GPIO.output(i,GPIO.LOW)

def alignPod2():
	global state_align
	
	if GPIO.input(l1_end_sensor_pin) == 0:

		GPIO.output(l1_green_stop, GPIO.LOW)
		GPIO.output(l1_green_start, GPIO.LOW)
		GPIO.output(l1_red_stop, GPIO.HIGH)
		GPIO.output(l1_blue_stop, GPIO.LOW)
	else:
		GPIO.output(l1_blue_stop, GPIO.HIGH)
		GPIO.wait_for_edge(l1_end_sensor_pin,GPIO.FALLING)
		while not state_align:
			if GPIO.input(l1_end_sensor_pin) == 0:
				GPIO.output(l1_green_stop, GPIO.LOW)
				GPIO.output(l1_green_start, GPIO.LOW)
				GPIO.output(l1_red_stop, GPIO.LOW)
				GPIO.output(l1_red_start, GPIO.LOW)
				GPIO.output(l1_blue_stop, GPIO.HIGH)
				time.sleep(0.25)
				GPIO.output(l1_blue_stop, GPIO.LOW)
				time.sleep(0.25)
			elif GPIO.input(l1_end_sensor_pin)==1: 
				GPIO.output(l1_green_stop, GPIO.LOW)
				GPIO.output(l1_green_start, GPIO.LOW)
				GPIO.output(l1_red_start, GPIO.LOW)
				GPIO.output(l1_red_stop, GPIO.LOW)
				GPIO.output(l1_blue_stop, GPIO.HIGH)

def alignPod3():
	global state_align

	if GPIO.input(l2_start_sensor_pin) == 0:

		GPIO.output(l2_green_stop, GPIO.LOW)
		GPIO.output(l2_green_start, GPIO.LOW)
		GPIO.output(l2_red_start, GPIO.HIGH)
		GPIO.output(l2_blue_start, GPIO.LOW)
	else:
		GPIO.output(l2_blue_start, GPIO.HIGH)
		GPIO.wait_for_edge(l2_start_sensor_pin,GPIO.FALLING)
		while not state_align:
			if GPIO.input(l2_start_sensor_pin) == 0:
				GPIO.output(l2_green_stop, GPIO.LOW)
				GPIO.output(l2_green_start, GPIO.LOW)
				GPIO.output(l2_red_start, GPIO.LOW)
				GPIO.output(l2_red_stop, GPIO.LOW)
				GPIO.output(l2_blue_start, GPIO.HIGH)
				time.sleep(0.25)
				GPIO.output(l2_blue_start, GPIO.LOW)
				time.sleep(0.25)
			elif GPIO.input(l2_start_sensor_pin)==1:
				GPIO.output(l2_green_stop, GPIO.LOW)
				GPIO.output(l2_green_start, GPIO.LOW)
				GPIO.output(l2_red_start, GPIO.LOW)
				GPIO.output(l2_red_stop, GPIO.LOW)
				GPIO.output(l2_blue_start, GPIO.HIGH)

def alignPod4():
	global state_align
	if GPIO.input(l2_end_sensor_pin) == 0:

		GPIO.output(l2_green_stop, GPIO.LOW)
		GPIO.output(l2_green_start, GPIO.LOW)
		GPIO.output(l2_red_stop, GPIO.HIGH)
		GPIO.output(l2_blue_stop, GPIO.LOW)
	else:

		GPIO.output(l2_blue_stop, GPIO.HIGH)
		GPIO.wait_for_edge(l2_end_sensor_pin,GPIO.FALLING)

		while not state_align:
			if GPIO.input(l2_end_sensor_pin) == 0:
				l2_green_red_low = [l2_green_stop,l2_red_start,l2_red_stop,l2_blue_stop]
				GPIO.output(l2_blue_stop, GPIO.HIGH)
				time.sleep(0.25)
				GPIO.output(l2_blue_stop, GPIO.LOW)
				time.sleep(0.25)
				for i in l2_green_red_low:
					GPIO.output(i, GPIO.LOW)

			elif GPIO.input(l2_end_sensor_pin)==1:
				GPIO.output(l2_blue_stop, GPIO.HIGH)
				green_red_pod4 = [l2_green_stop,l2_green_start,l2_red_start,l2_red_stop]
				for i in green_red_pod4:
					GPIO.output(i, GPIO.LOW)

def alignPod5():
	global state_align
	if GPIO.input(l3_start_sensor_pin) == 0:
		GPIO.output(l3_red_start, GPIO.HIGH)
		arr = [l3_green_stop,l3_green_start,l3_blue_start]
		for i in arr:
			GPIO.output(i, GPIO.LOW)
	else:

		GPIO.output(l3_blue_start, GPIO.HIGH)
		GPIO.wait_for_edge(l3_start_sensor_pin,GPIO.FALLING)
		while not state_align:
			
			if GPIO.input(l3_start_sensor_pin) == 0:
				green_red_l3 = [l3_green_stop,l3_green_start,l3_red_stop,l3_red_start]
				for i in green_red_l3:
					GPIO.output(i, GPIO.LOW)
				
				GPIO.output(l3_blue_start, GPIO.HIGH)
				time.sleep(0.25)
				GPIO.output(l3_blue_start, GPIO.LOW)
				time.sleep(0.25)

			elif GPIO.input(l3_start_sensor_pin)==1:
				GPIO.output(l3_blue_start, GPIO.HIGH)

				green_red_l3_arr[l3_green_stop,l3_green_start,l3_red_start,l3_red_stop]
				for i in green_red_l3_arr:
					GPIO.output(i, GPIO.LOW)
		
def alignPod6():
	global state_align
	if GPIO.input(l3_end_sensor_pin) == 0:

		GPIO.output(l3_red_stop, GPIO.HIGH)
		green_blue_l3 = [l3_green_stop,l3_green_start,l3_blue_stop]
		for i in green_blue_l1:
			GPIO.output(i, GPIO.LOW)

	else:
		GPIO.output(l3_blue_stop, GPIO.HIGH)
		GPIO.wait_for_edge(l3_end_sensor_pin,GPIO.FALLING)
	
		while not state_align:
			if GPIO.input(l3_end_sensor_pin) == 0:
				green_red = [l3_green_stop,l3_green_start,l3_red_stop,l3_red_start]
				for i in green_red:
					GPIO.output(i, GPIO.LOW)
				GPIO.output(l3_blue_stop, GPIO.HIGH)
				time.sleep(0.25)
				GPIO.output(l3_blue_stop, GPIO.LOW)
				time.sleep(0.25)
			elif GPIO.input(l3_end_sensor_pin)==1:
				GPIO.output(l3_blue_stop, GPIO.HIGH)
				for i in green_red:
					GPIO.output(i, GPIO.LOW)

# 6 interrupt functions of 6 sensors
# detects change in edge  
					
def l1_start_interrupt(self,):
	
	state_lane1 = 5
	LedColorsControl('1 and 2', 'lane_1' ,'green',True)
	# greenStableLane1()
	response = json.dumps({
		"lane_no": "1",
		"result" : "start",
		"message_type": "timings"
	}, default=json_util.default)
	socketio.send(response, namespace="/display", room="display_room")
	GPIO.remove_event_detect(l1_start_sensor_pin)
def l1_stop_interrupt(self):
	global stop_lane1_thread

	LedColorsControl('1 and 2', 'lane_1','stable','blue', True)

	# blueStableLane1()	
	stop_lane1_thread = True

	response = json.dumps({
			"lane_no" : "1",
			"result" : "stop",
			"message_type": "timings"
		}, default=json_util.default)
	socketio.send(response, namespace="/display", room="display_room")
	GPIO.remove_event_detect(l1_end_sensor_pin)
def l2_start_interrupt(self):
	global start_1,stop_1,state_lane2
	state_lane2 =3
	LedColorsControl('2 and 3', 'lane_2', 'green', 'stable', True)
	response = json.dumps({
			"lane_no" : "2",
			"result" : "start",
			"message_type": "timings"
		}, default=json_util.default)
	socketio.send(response, namespace="/display", room="display_room")
	GPIO.remove_event_detect(l2_start_sensor_pin)	
def l2_stop_interrupt(self):
	global stop_lane2_thread
	LedColorsControl('2 and 3', 'lane_2','blue','stable',True)
	stop_lane2_thread = True
	response = json.dumps({
			"lane_no" : "2",
			"result" : "stop",
			"message_type": "timings"
		}, default=json_util.default)
	socketio.send(response, namespace="/display", room="display_room")
	GPIO.remove_event_detect(l2_end_sensor_pin)
def l3_start_interrupt(self):
	state_lane3 = 3
	LedColorsControl('5 and 6' 'lane_3', 'green','stable', True)
	response = json.dumps({
			"lane_no" : "3",
			"result" : "start",
			"message_type": "timings"
		}, default=json_util.default)
	socketio.send(response, namespace="/display", room="display_room")
	GPIO.remove_event_detect(l3_start_sensor_pin)
def l3_stop_interrupt(self):
	global stop_lane3_thread
	LedColorsControl('5 and 6','lane_3', 'blue','stable',True)
	stop_lane3_thread = True
	response = json.dumps({
			"lane_no" : "3",
			"result" : "stop",
			"message_type": "timings"
		}, default=json_util.default)
	socketio.send(response, namespace="/display", room="display_room")
	GPIO.remove_event_detect(l3_end_sensor_pin)

# ledcolorscontrol function is used for stable lightning of lane 1 , lane 2 and lane 3
def LedColorsControl(pod ,lane_no , color , state , status):
	if status:
		if state =="stable":

			if ( pod == '1 and 2' and lane_no == 'lane_1' and color =='green'):
				GPIO.output(l1_green_start, GPIO.HIGH)
				GPIO.output(l1_green_stop, GPIO.HIGH)
				for i in allRedLow:
					GPIO.output(i, GPIO.LOW)
				for i in allBlueLow:
					GPIO.output(i, GPIO.LOW)
			
			elif (pod == 'pod 3 and 4' and lane_no == 'lane_2' and color =='green'):
				GPIO.output(l2_green_start, GPIO.HIGH)
				GPIO.output(l2_green_stop, GPIO.HIGH)
				for i in allRedLow:
					GPIO.output(i, GPIO.LOW)
				for i in allBlueLow:
					GPIO.output(i, GPIO.LOW)


			elif (pod == 'pod 5 and 6 ' and lane_no == 'lane_3' and color =='green'):
				GPIO.output(l3_green_start, GPIO.HIGH)
				GPIO.output(l3_green_stop, GPIO.HIGH)
				for i in allRedLow:
					GPIO.output(i, GPIO.LOW)
				for i in allBlueLow:
					GPIO.output(i, GPIO.LOW)


			elif (pod == '1 and 2' and lane_no == 'lane_1' and color =='red'):
				GPIO.output(l1_red_start, GPIO.HIGH)
				GPIO.output(l1_red_stop, GPIO.HIGH)
				for i in allGreenLow:
					GPIO.output(i, GPIO.LOW)
				for i in allBlueLow:
					GPIO.output(i, GPIO.LOW)

			elif ( pod == 'pod 3 and 4' and lane_no == 'lane_2' and color =='red'):
				GPIO.output(l2_red_start, GPIO.HIGH)
				GPIO.output(l2_green_stop, GPIO.HIGH)
				for i in allGreenLow:
					GPIO.output(i, GPIO.LOW)
				for i in allBlueLow:
					GPIO.output(i, GPIO.LOW)


			elif ( pod == 'pod 5 and 6' and lane_no == 'lane_3' and color =='red'):
				GPIO.output(l3_red_start, GPIO.HIGH)
				GPIO.output(l3_red_stop, GPIO.HIGH)
				for i in allGreenLow:
					GPIO.output(i, GPIO.LOW)
				for i in allBlueLow:
					GPIO.output(i, GPIO.LOW)

			elif ( pod == '1 and 2' and lane_no == 'lane_1' and color =='blue'):
				GPIO.output(l1_blue_start, GPIO.HIGH)
				GPIO.output(l1_blue_stop, GPIO.HIGH)
				for i in allGreenLow:
					GPIO.output(i, GPIO.LOW)
				for i in allRedLow:
					GPIO.output(i, GPIO.LOW)

			elif ( pod == 'pod 3 and 4' and lane_no == 'lane_2' and color =='blue'):
				GPIO.output(l2_blue_start, GPIO.HIGH)
				GPIO.output(l2_blue_stop, GPIO.HIGH)
				for i in allRedLow:
					GPIO.output(i, GPIO.LOW)
				for i in allGreenLow:
					GPIO.output(i, GPIO.LOW)

			elif ( pod == 'pod 5 and 6' and  lane_no == 'lane_3' and color =='blue'):
				GPIO.output(l3_blue_start, GPIO.HIGH)
				GPIO.output(l3_blue_stop, GPIO.HIGH)
				for i in allRedLow:
					GPIO.output(i, GPIO.LOW)
				for i in allGreenLow:
					GPIO.output(i, GPIO.LOW)
	
def yellowStable(lane_no):

	if lane_no == 'lane_1':

		GPIO.output(l1_green_start, GPIO.HIGH)
		GPIO.output(l1_green_stop, GPIO.HIGH)
		GPIO.output(l1_blue_start, GPIO.LOW)
		GPIO.output(l1_blue_stop, GPIO.LOW)
		GPIO.output(l1_red_start, GPIO.HIGH)
		GPIO.output(l1_red_stop, GPIO.HIGH)


	elif lane_no == 'lane_2':

		GPIO.output(l2_green_start, GPIO.HIGH)
		GPIO.output(l2_green_stop, GPIO.HIGH)
		GPIO.output(l2_blue_start, GPIO.LOW)
		GPIO.output(l2_blue_stop, GPIO.LOW)
		GPIO.output(l2_red_start, GPIO.HIGH)
		GPIO.output(l2_red_stop, GPIO.HIGH)


	elif lane_no == 'lane_3':

		GPIO.output(l3_green_start, GPIO.HIGH)
		GPIO.output(l3_green_stop, GPIO.HIGH)
		GPIO.output(l3_blue_start, GPIO.LOW)
		GPIO.output(l3_blue_stop, GPIO.LOW)
		GPIO.output(l3_red_start, GPIO.HIGH)
		GPIO.output(l3_red_stop, GPIO.HIGH)

def allPodsledsOff():
	lowPins = [l1_red_start,l1_red_stop,l1_green_start,l1_green_stop,l1_blue_start,l1_blue_stop,l2_red_start,l2_red_stop,l2_green_start,l2_green_stop,l2_blue_start,l2_blue_stop,l3_green_start,l3_green_stop,l3_blue_start,l3_blue_stop,l3_red_start,l3_red_stop]
	for i in lowPins:
		GPIO.output(i, GPIO.LOW)

# powerOn fucntion is the used to make all pods leds red
def powerOn():
	global power
	if power:
		print 'in power'
		LedColorsControl('1 and 2','lane_3', 'red','stable',True)
		LedColorsControl('3 and 4','lane_3', 'red','stable',True)
		LedColorsControl('5 and 6','lane_3', 'red','stable',True)





# Initialize POST call
# initializeLane function is used to indicate ready and running state of race
# Check if all sensors are aligned, else do nothing, show error message on frontend - "Sensors are not aligned. Failed to Initialize"
# keep interrupts attached
# Since all sensors are aligned, no threads will be running, since all sensors will be stable blue
# Start 6 stable yellow threads, with an independent global control variable for each 
# stable yellow color indicates start of race lane
# stable blue indicates finish of race

def initializeLane(lane_no):
	print lane_no
	global stop_lane1_thread,stop_lane2_thread,stop_lane3_thread

	if lane_no == 'lane_1':
	
		print "inside lane 1" 
		if GPIO.input(l1_start_sensor_pin) and GPIO.input(l1_end_sensor_pin)==1:
		
			yellowStable(lane_no)
			GPIO.add_event_detect(l1_start_sensor_pin, GPIO.FALLING, callback=l1_start_interrupt, bouncetime=3000)
			GPIO.add_event_detect(l1_end_sensor_pin , GPIO.FALLING, callback=l1_stop_interrupt, bouncetime=3000)
			
			if stop_lane1_thread:
				return 			
		else:
			print 'sensors are still misaligned'
			response = json.dumps({
					"status":"failure",
					"lane_no" : "1",
					"result" : "sensor is not aligned properly"
				}, default=json_util.default)
			socketio.send(response, namespace="/display", room="display_room")


	elif lane_no == 'lane_2':


		print "inside lane 2"

		if GPIO.input(l2_start_sensor_pin) and GPIO.input(l2_end_sensor_pin)==1:
		
			yellowStable(lane_no)
			GPIO.add_event_detect(l2_start_sensor_pin, GPIO.FALLING, callback=l2_start_interrupt, bouncetime=3000)
			GPIO.add_event_detect(l2_end_sensor_pin , GPIO.FALLING, callback=l2_stop_interrupt, bouncetime=3000)
			
			if stop_lane2_thread:
				return 
		else:
			print 'sensors are still misaligned'
			response = json.dumps({
					"status":"failure",
					"lane_no" : "2",
					"result" : "sensor is not aligned properly"
				}, default=json_util.default)
			socketio.send(response, namespace="/display", room="display_room")
		
	elif lane_no == 'lane_3':

		print "inside lane 3" 
		if GPIO.input(l3_start_sensor_pin) and GPIO.input(l3_end_sensor_pin)==1:
		
			yellowStable(lane_no)
			GPIO.add_event_detect(l3_start_sensor_pin, GPIO.FALLING, callback=l3_start_interrupt, bouncetime=3000)
			GPIO.add_event_detect(l3_end_sensor_pin , GPIO.FALLING, callback=l3_stop_interrupt, bouncetime=3000)

			if stop_lane3_thread:
				return 
		else:
			print 'sensors are still misaligned'
			response = json.dumps({
					"status":"failure",
					"lane_no" : "3",
					"result" : "sensor is not aligned properly"
				}, default=json_util.default)
			socketio.send(response, namespace="/display", room="display_room")	
def main():
	global p1, p2,p3,p4,p5,p6,p7,arr,i,proc,state_align

	if not state_align:
	
		p1 = multiprocessing.Process(target=alignPod1)
		p1.daemon=True
		p2 = multiprocessing.Process(target=alignPod2)
		p2.daemon=True
		p4 = multiprocessing.Process(target=alignPod3)
		p4.daemon=True
		p5 = multiprocessing.Process(target=alignPod4)
		p5.daemon=True
		p6 = multiprocessing.Process(target=alignPod5)
		p6.daemon=True
		p7 = multiprocessing.Process(target=alignPod6)
		p7.daemon=True
		p1.start()
		p2.start()
		p4.start()
		p5.start()
		p6.start()
		p7.start()
		print 'p1 id:'+str(p1.pid)
		print ' p3 id:'+str(p2.pid)
		print ' p3 id:'+str(p4.pid)
		print ' p3 id:'+str(p5.pid)
		print ' p3 id:'+str(p6.pid)
		print ' p3 id:'+str(p7.pid)
	
def mainthread():

	lane_array = ['lane_1', 'lane_2', 'lane_3'] 

	for lane_no in lane_array:
		p3 = threading.Thread(target=initializeLane, args=(lane_no, ))
		p3.start()
		p3.join()

@app.route('/device/align', methods=["GET"])
def getDeviceAlign():

	global state_align
	state_align = False
	power = False
	allPodsledsOff()
	time.sleep(1)
	main()
	
	try:

		if (GPIO.input(l1_start_sensor_pin) and GPIO.input(l1_end_sensor_pin) and GPIO.input(l2_start_sensor_pin) and GPIO.input(l2_end_sensor_pin) and GPIO.input(l3_start_sensor_pin) and GPIO.input(l3_end_sensor_pin)) == True:

			align_check_result = "success"
			
		else:

			align_check_result = "failure"

		response_align = json.dumps({
			"status": align_check_result,
			"result" : "All sensors are aligned",
			"l1_start": GPIO.input(l1_start_sensor_pin),
			"l1_stop": GPIO.input(l1_end_sensor_pin),
			"l2_start": GPIO.input(l2_start_sensor_pin),
			"l2_stop": GPIO.input(l2_end_sensor_pin),
			"l3_start": GPIO.input(l3_start_sensor_pin),
			"l3_stop": GPIO.input(l3_end_sensor_pin)
			
		}, default=json_util.default)
		socketio.send(response_align, namespace="/display", room="display_room")
				
		return Response(response_align, mimetype="application/json")
	except Exception, e:
			return Response(json.dumps({
				"status": "failure",
				"message": "Invalid request: %s" %e
			}, default=json_util.default), mimetype="application/json")
	
@app.route('/device/initialize', methods=["GET"])
def getDeviceIntialize():
	global p1, p2,p4,p5,p6,p7,arr,i,state_align,proc

	try:
		p1.terminate()
		print 'p1 terminated:'+str(p1.pid)
		p2.terminate()
		print 'p2 terminated:'+str(p2.pid)
		p4.terminate()
		print 'p4 terminated:'+str(p4.pid)
		p5.terminate()
		print 'p5 terminated:'+str(p5.pid)
		p6.terminate()
		print 'p6 terminated:'+str(p6.pid)
		p7.terminate()
		print 'p7 terminated:'+str(p7.pid)
		proc = multiprocessing.active_children()
		arr = []
		for i in proc:
			print(i.pid)
			arr.append(i.pid)

		for i in proc:
			i.terminate()
			print 'terminated chid processes'
		allPodsledsOff()
		time.sleep(1)
		mainthread()
		return Response(json.dumps({
		"status":"success",
		"message":state_align
		}, default=json_util.default),
		 mimetype="application/json")

	except Exception, e:
		return Response(json.dumps({
				"status": "failure",
				"message": "Invalid request: %s" %e
			}, default=json_util.default), mimetype="application/json")

@app.route('/device/reset', methods=["GET"])
def reset():
	global state_align
	global stop_lane1_thread,stop_lane2_thread,stop_lane3_thread

	try:
		GPIO.remove_event_detect(l1_start_sensor_pin)
		GPIO.remove_event_detect(l1_end_sensor_pin)
		GPIO.remove_event_detect(l2_start_sensor_pin)
		GPIO.remove_event_detect(l2_end_sensor_pin)
		GPIO.remove_event_detect(l3_start_sensor_pin)
		GPIO.remove_event_detect(l3_end_sensor_pin)
		allPodsledsOff()
		time.sleep(0.25)
		powerOn()
		time.sleep(0.25)
		socket_response = json.dumps({
			"status": "success",
			"result" : "Reset successfully"
		}, default=json_util.default)
		socketio.send(socket_response, namespace="/display", room="display_room")

		return Response(json.dumps({
		"status":"success",
		"message":"Device reset successfully"
		}, default=json_util.default),
		 mimetype="application/json")

	except Exception, e:
		return Response(json.dumps({
				"status": "failure",
				"message": "Invalid request: %s" %e
			}, default=json_util.default), mimetype="application/json")
if state_power ==1:
	global power
	power = True
	powerOn()
		



	




		



	
