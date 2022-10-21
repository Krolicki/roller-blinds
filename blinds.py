import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

PWMA = 17
AIN2 = 27
AIN1 = 22
STBY = 4

# set up GPIO pins
GPIO.setup(PWMA, GPIO.OUT) 
GPIO.setup(AIN2, GPIO.OUT) 
GPIO.setup(AIN1, GPIO.OUT) 
GPIO.setup(STBY, GPIO.OUT)


#start motor
GPIO.output(AIN1, True)
GPIO.output(AIN2, False) 

# Set the motor speed
GPIO.output(PWMA, True) 

# Disable STBY (standby)
GPIO.output(STBY, True)

print("Start")
time.sleep(5)
print("Stop")

# Reset all the GPIO pins by setting them to LOW
GPIO.output(AIN1, False) 
GPIO.output(AIN2, False) 
GPIO.output(PWMA, False) 
GPIO.output(STBY, False) 
