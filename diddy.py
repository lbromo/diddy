# DIDDY; THE LEGO ROBOT SLAYER OF DOOM

# - koere tilfaeldigt
# - detektere sort streg / bord kant / ikke falde ned
# - defence / attack  mechanism

from ev3.lego import *
from time import sleep
import pprint

# SETUP MOTORS
#motorRight = dc_motor(OUTPUT_A)
#motorLeft  = dc_motor(OUTPUT_B)

# SETUP TOUCH SENSORS
frontTouchSensor = TouchSensor(1)
backTouchSensor  = TouchSensor(2)

# SETUP COLOR SENSOR
colorSensor = ColorSensor(3)
blackLimit = 15

# SETUP GYRO
gyroSensor = GyroSensor(4)

# PP
pp = pprint.PrettyPrinter(indent=1)

def runRandomly(direction = 0):
    pass
    #drive_for(motorLeft, motorRight, dir = direction, power = 100)

def logStatus():
    pp.pprint([colorSensor.reflect])

while(True):
    # LOGGING
    logStatus()
    # EVENTS
    if colorSensor.reflect < blackLimit:
        print "LINE DETECTED!"
    if frontTouchSensor.isPushed:
        print "FRONT BUMPER - ATTACK!!!"
    if backTouchSensor.isPushed:
        print "BACK BUMPER - ATTACK!!!"
    # DRIVE
    #runRandomly()