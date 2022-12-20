import RPi.GPIO as GPIO
import time
import threading
from flask import Flask, render_template, jsonify
 
in1 = 17
in2 = 18
in3 = 27
in4 = 22
 
# careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
#step_sleep = 0.002
step_sleep = 0.02
 
full_step = 4096  #5.625*(1/64) per step, 4096 steps is 360°, 1 step = +-5 cm

#max_step = 151552 #4096 * 37
max_step = 1000
# defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]
 
steps_count = 0 # steps form top

move = False

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

app = Flask(__name__)
 
def cleanup():
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )
    #GPIO.cleanup()
        
def read_steps():
    global steps_count
    f = open("/home/pi/scripts/roller-blinds/steps_count.txt","r")
    steps_count = int(f.readline())
    f.close()
        
def save_steps():
    global steps_count
    f = open("/home/pi/scripts/roller-blinds/steps_count.txt","w")#write mode
    f.write(str(steps_count))
    f.close()

def roll(steps, direction):
    global steps_count
    global move
    i = 0
    motor_step_counter = 0
    d = 0
    if(direction == 'up'):
        d = -1
        if(steps_count <= 0):
            move = False
            return
    elif(direction == 'down'):
        d = 1
        if(steps_count >= max_step):
            move = False
            return
    move = True
    for i in range(steps):
        #global move
        if(move == False):
            save_steps()
            break
        #for pin in range(0, len(motor_pins)):
            #GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )
        motor_step_counter = (motor_step_counter + d) % 8
        steps_count += d
        print(steps_count)
        time.sleep( step_sleep )
        if(steps_count <= 0 or steps_count >= max_step):
            print("stop")
            move = False
            cleanup()
            save_steps()
            break

@app.route('/')
def index():
    global steps_count
    return render_template('index.html', steps = steps_count, maxStep = max_step, sleep = step_sleep)

@app.route("/roll-up", methods=["POST"])
def roll_up():
    global steps_count
    global move
    if(move == True):
        move = False
        time.sleep( step_sleep )
    x = threading.Thread(target=roll, args=(steps_count,'up'))
    x.start()
    return str(steps_count)

@app.route("/roll-down", methods=["POST"])
def roll_down():
    global steps_count
    global move
    if(move == True):
        move = False
        time.sleep( step_sleep )
    x = threading.Thread(target=roll, args=(max_step-steps_count,'down'))
    x.start()
    return str(steps_count)

@app.route("/abort", methods=["POST"])
def abort():
    global move
    if(move == True):
        move = False
        cleanup()
        save_steps()
    return str(steps_count)

@app.route('/steps', methods=['GET'])
def steps():
    global steps_count
    global move
    #return str(steps_count)
    return jsonify({'step': steps_count,'move': move})

try:
     print("start")
#     #time.sleep(4)
#     move = True
#     read_steps()
#     print(steps_count)
#     x = threading.Thread(target=roll, args=(2048,'up'))
#     x.start()
#     print(steps_count)
#     #time.sleep(1)
#     #move = False
#     time.sleep(5)
#     save_steps()
#     print(steps_count)

except KeyboardInterrupt:
    cleanup()
    exit( 1 )
 
# cleanup()
# exit( 0 )

if __name__ == '__main__':
    read_steps()
    app.run(debug=True, port=5000, host='0.0.0.0')
