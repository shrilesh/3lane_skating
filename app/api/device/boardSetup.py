import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
senorPins = [5,11,7,8,23,26]
outputpins = [22,16,18,24,29,31,10,12,13,15,19,21,32,33,38,35,36,37]
for pins in senorPins:
	GPIO.setup(pins,GPIO.IN,pull_up_down = GPIO.PUD_UP)

for output in outputpins:
	GPIO.setup(output,GPIO.OUT)
	GPIO.output(output,GPIO.LOW)





