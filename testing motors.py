from motor  import *
import time
import RPi.GPIO as GPIO

robot = Motor(40, 38, 36, 33, 31, 29)
while True:
	robot.move(0.2, 0)
	
GPIO.cleanup()
