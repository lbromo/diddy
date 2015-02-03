# DIDDY; THE LEGO ROBOT SLAYER OF DOOM

# - koere tilfaeldigt
# - detektere sort streg / bord kant / ikke falde ned
# - defence / attack  mechanism

from ev3dev import *
from ev3dev_utils.motors import *
from time import sleep
import pprint

# SETUP MOTORS
#motorRight = dc_motor(OUTPUT_A)
#motorLeft  = dc_motor(OUTPUT_B)

# SETUP TOUCH SENSORS
frontTouchSensor = touch_sensor(INPUT_1)
backTouchSensor  = touch_sensor(INPUT_2)

# SETUP COLOR SENSOR
colorSensor = color_sensor(INPUT_3)
colorSensor.mode = color_sensor.mode_reflect
blackLimit = 15

# SETUP GYRO
gyroSensor = gyro_sensor(INPUT_4)

# PP
pp = pprint.PrettyPrinter(indent=1)

def runRandomly(direction = 0):
    pass
    #drive_for(motorLeft, motorRight, dir = direction, power = 100)

def logStatus():
    pp.pprint([colorSensor.value()])

while(True):
    # LOGGING
    logStatus()
    # EVENTS
    if colorSensor.value() < blackLimit:
        print "LINE DETECTED!"
    if frontTouchSensor.value():
        print "FRONT BUMPER - ATTACK!!!"
    if backTouchSensor.value():
        print "BACK BUMPER - ATTACK!!!"
    # DRIVE
    runRandomly()