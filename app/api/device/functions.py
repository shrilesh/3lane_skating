import RPi.GPIO as GPIO
# def pod1Align():
# 	global state_align
# 	GPIO.add_event_detect(start_sensor_pin,GPIO.FALLING)
# 	while not state_align:
		
# 	 	if GPIO.event_detected(start_sensor_pin):
# 	 		print 'in pod1Align'
# 			while GPIO.input(start_sensor_pin) == 0:
# 				print 'start sensor misaligned'
# 				GPIO.output(l1_green_start, GPIO.LOW)
# 				GPIO.output(l1_red_start, GPIO.LOW)
# 				GPIO.output(l1_blue_start, GPIO.HIGH)
# 				time.sleep(0.25)
# 				GPIO.output(l1_blue_start, GPIO.LOW)
# 				time.sleep(0.25)
# 		elif GPIO.event_detected(start_sensor_pin)==False:
# 			print 'in start sensor'
# 			if GPIO.input(start_sensor_pin)==1:
# 				print 'start sensor aligned'
# 				GPIO.output(l1_green_start, GPIO.LOW)
# 				GPIO.output(l1_red_start, GPIO.LOW)
# 				GPIO.output(l1_blue_start, GPIO.HIGH)

# def pod2Align():
# 	global state_align
# 	GPIO.add_event_detect(end_sensor_pin,GPIO.FALLING)
# 	while not state_align:
		
# 		if GPIO.event_detected(end_sensor_pin):
# 			while GPIO.input(end_sensor_pin) == 0:
# 				print 'end sensor misaligned'
# 				GPIO.output(l1_green_stop, GPIO.LOW)
# 				GPIO.output(l1_red_stop, GPIO.LOW)
# 				GPIO.output(l1_blue_stop, GPIO.HIGH)
# 				time.sleep(0.25)
# 				GPIO.output(l1_blue_stop, GPIO.LOW)
# 				time.sleep(0.25)

# 		elif GPIO.event_detected(end_sensor_pin) == False:
# 			print 'in end sensor'
# 			if GPIO.input(end_sensor_pin)==1:
# 				print 'end sensor aligned' 
# 				GPIO.output(l1_green_stop, GPIO.LOW)
# 				GPIO.output(l1_red_stop, GPIO.LOW)
# 				GPIO.output(l1_blue_stop, GPIO.HIGH)

# 	

def greenBlink():
	GPIO.output(l1_green_start, GPIO.HIGH)
	GPIO.output(l1_green_stop, GPIO.HIGH)
	time.sleep(0.25)
	GPIO.output(l1_green_start, GPIO.LOW)
	GPIO.output(l1_green_stop, GPIO.LOW)
	time.sleep(0.25)
	GPIO.output(l1_blue_start, GPIO.LOW)
	GPIO.output(l1_blue_stop, GPIO.LOW)
	GPIO.output(l1_red_start, GPIO.LOW)
	GPIO.output(l1_red_stop, GPIO.LOW)
