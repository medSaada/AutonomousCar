import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)

class Motor:
    def __init__(self, en_pin, in1_pin, in2_pin):
        self.in1_pin = in1_pin
        self.in2_pin = in2_pin
        self.en_pin = en_pin

        GPIO.setup(self.in1_pin, GPIO.OUT)
        GPIO.setup(self.in2_pin, GPIO.OUT)
        GPIO.setup(self.en_pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.en_pin, 100)
        self.pwm.start(0)

    def forward(self, speed):
        GPIO.output(self.in1_pin, GPIO.HIGH)
        GPIO.output(self.in2_pin, GPIO.LOW)
        self.pwm.ChangeDutyCycle(int(speed*100))

    def backward(self, speed):
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.HIGH)
        self.pwm.ChangeDutyCycle(int(speed*100))

    def stop(self):
        self.pwm.ChangeDutyCycle(0)
        
class Robot():
	def __init__(self,pin_v,pin1,pin2,pinB_v,pinB1,pinB2):
		self.left_motor = Motor(pin_v, pin1, pin2)
		self.right_motor = Motor(pinB_v, pinB1, pinB2)
	def stop(self):
		self.left_motor.stop()
		self.right_motor.stop()
	def right(self, speed):
		self.left_motor.forward(speed)
		self.right_motor.stop()
	def left(self,speed):
		self.left_motor.stop()
		self.right_motor.forward(speed)
	def infront(self, speed):
		self.left_motor.forward(speed)
		self.right_motor.forward(speed)
	
		
	
	


