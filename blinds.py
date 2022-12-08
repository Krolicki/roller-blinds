import RPi.GPIO as GPIO
import time
 
in1 = 17
in2 = 18
in3 = 27
in4 = 22
 
# careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
step_sleep = 0.002
 
step_count = 4096  #5.625*(1/64) per step, 4096 steps is 360°, 1 step = +-5 cm
 
# defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]
 
# setting up
GPIO.setmode( GPIO.BCM )
GPIO.setup( in1, GPIO.OUT )
GPIO.setup( in2, GPIO.OUT )
GPIO.setup( in3, GPIO.OUT )
GPIO.setup( in4, GPIO.OUT )
 
# initializing
GPIO.output( in1, GPIO.LOW )
GPIO.output( in2, GPIO.LOW )
GPIO.output( in3, GPIO.LOW )
GPIO.output( in4, GPIO.LOW )
 
 
motor_pins = [in1,in2,in3,in4]
 
def cleanup():
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )
    GPIO.cleanup()
 
def forward(steps):
    i = 0
    motor_step_counter = 0
    for i in range(steps):
        for pin in range(0, len(motor_pins)):
            GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )
        motor_step_counter = (motor_step_counter - 1) % 8
        time.sleep( step_sleep )
 
def backward(steps):
    i = 0
    motor_step_counter = 0
    for i in range(steps):
        for pin in range(0, len(motor_pins)):
            GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )
        motor_step_counter = (motor_step_counter + 1) % 8
        time.sleep( step_sleep )

try:
    print("start")
    #time.sleep(4)
    #forward(2048)
    #backward(1024)
    #backward(4096 *37 - 1024)

except KeyboardInterrupt:
    cleanup()
    exit( 1 )
 
cleanup()
exit( 0 )