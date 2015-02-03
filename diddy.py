# DIDDY; THE LEGO ROBOT SLAYER OF DOOM

# - koere tilfaeldigt
# - detektere sort streg / bord kant / ikke falde ned
# - defence / attack  mechanism

from ev3dev import *
from ev3dev_utils.motors import *

# SETUP MOTORS
#motorRight = dc_motor(OUTPUT_A)
#motorLeft  = dc_motor(OUTPUT_B)

# SETUP TOUCH SENSORS
#frontTouchSensor = touch_sensor(INPUT_1)
#backTouchSensor  = touch_sensor(INPUT_2)

# SETUP COLOR SENSOR
colorSensor = color_sensor(INPUT_3)
colorSensor.mode = color_sensor.mode_reflect
blackLimit = 75

# SETUP GYRO
gyroSensor = gyro_sensor(INPUT_4)

def runRandomly(direction = 0):
    pass
    #drive_for(motorLeft, motorRight, dir = direction, power = 100)

while(True):
    if colorSensor.value() > blackLimit:
        #TURN 180 deg
        print 'DREEEJJJJ'

    runRandomly()