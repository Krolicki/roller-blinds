import RPi.GPIO as GPIO
import time
import threading
from flask import Flask, render_template, jsonify

# odstęp pomiędzy krokami, prędkość silnika
step_sleep = 0.001
 
full_step = 4096 # 5.625*(1/64) na krok, 4096 kroków to 360°, 360° = +-5 cm

max_step = 150862 # całkowita ilość kroków do otwarcia rolety

# sekwencja silnika krokowego
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]
 
steps_count = 0 # licznik kroków od góry

move = False
direction = None
light_status = False
error = False

# pin sterownika silnika = pin GPIO
in1 = 17
in2 = 18
in3 = 27
in4 = 22

# pin czujnika światła
light_sensor = 2

# pin przekaźnika
relay = 23

# definiowanie pinów
GPIO.setwarnings(False)
GPIO.setmode( GPIO.BCM )
GPIO.setup( in1, GPIO.OUT )
GPIO.setup( in2, GPIO.OUT )
GPIO.setup( in3, GPIO.OUT )
GPIO.setup( in4, GPIO.OUT )
GPIO.setup( light_sensor, GPIO.IN )
GPIO.setup( relay, GPIO.OUT)
 
# inicjalizacja
GPIO.output( in1, GPIO.LOW )
GPIO.output( in2, GPIO.LOW )
GPIO.output( in3, GPIO.LOW )
GPIO.output( in4, GPIO.LOW )
GPIO.output( relay, GPIO.LOW )
 
motor_pins = [in1,in2,in3,in4]

app = Flask(__name__)
 
def cleanup():
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )
    #GPIO.cleanup()

#odczytywanie ilości kroków z pliku
def read_steps():
    global steps_count
    f = open("/home/pi/scripts/roller-blinds/conf/steps_count.txt","r")
    steps_count = int(f.readline())
    f.close()
    
# zapisywanie ilości kroków do pliku
def save_steps():
    global steps_count
    f = open("/home/pi/scripts/roller-blinds/conf/steps_count.txt","w") #tryb nadpisywania
    f.write(str(steps_count))
    f.close()
    
def read_move():
    f = open("/home/pi/scripts/roller-blinds/conf/move_status.txt","r")
    last_move_status = f.readline()
    f.close()
    global error
    if(last_move_status == 'True'):
        error = True
    
def save_move():
    global move
    f = open("/home/pi/scripts/roller-blinds/conf/move_status.txt","w") #tryb nadpisywania
    f.write(str(move))
    f.close()

# pobieranie odczytu z czujnika światła, 1 = jest ciemno, 0 = jest jasno
def get_light():
    global light_status
    light = GPIO.input(light_sensor)
    if(light == 1):
        if(not light_status):
            GPIO.output(relay, True)
            light_status = True

def roll(steps, direction):
    global steps_count
    global move
    global error
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
    if(error):
        move = False
        print("Wystąpił błąd. Sprawdź pliki konfiguracyjne")
        return
    move = True
    save_move()
    for i in range(steps):
        #global move
        if(move == False):
            save_steps()
            save_move()
            break
        for pin in range(0, len(motor_pins)):
            GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )
        motor_step_counter = (motor_step_counter + (d * -1)) % 8
        steps_count += d
        if(steps_count <= 0 or steps_count >= max_step):
            move = False
            cleanup()
            save_steps()
            save_move()
            if(direction == 'down'):
                get_light()
            direction = None
            break
        time.sleep( step_sleep )

@app.route('/')
def index():
    global steps_count
    global light_status
    global error
    return render_template('index.html', steps = steps_count, maxStep = max_step, sleep = step_sleep, light_status = light_status, error = error)

@app.route("/roll-up", methods=["POST"])
def roll_up():
    global steps_count
    global move
    global direction
    if(move == True):
        move = False
        time.sleep( step_sleep * 2)
    direction = "up"
    x = threading.Thread(target=roll, args=(steps_count,'up'))
    x.start()
    return str(steps_count)

@app.route("/roll-down", methods=["POST"])
def roll_down():
    global steps_count
    global move
    global direction
    if(move == True):
        move = False
        time.sleep( step_sleep * 2)
    direction = "down"
    x = threading.Thread(target=roll, args=(max_step-steps_count,'down'))
    x.start()
    return str(steps_count)

@app.route("/abort", methods=["POST"])
def abort():
    global move
    if(move == True):
        move = False
        direction = None
        cleanup()
        save_steps()
    return str(steps_count)

@app.route("/light/<action>", methods=["POST"])
def light(action):
    global light_status
    if(action == "on"):
        if(light_status==False):
          GPIO.output(relay, True)
          light_status = True
    if(action == "off"):
        if(light_status==True):
          GPIO.output(relay, False)
          light_status = False
    return str(light_status)

@app.route('/status', methods=['GET'])
def steps():
    global steps_count
    global move
    global direction
    global light_status
    global error
    return jsonify({'step': steps_count,'move': move, 'direction': direction, 'light_status' : light_status, 'error' : error})

try:
    if __name__ == '__main__':
        #get_light()
        read_move()
        read_steps()
        app.run(debug=True, port=5000, host='0.0.0.0')
        
except KeyboardInterrupt:
    cleanup()
    GPIO.output(relay, False)
    exit( 1 )
