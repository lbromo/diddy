# DIDDY; THE LEGO ROBOT SLAYER OF DOOM

# - koere tilfaeldigt
# - detektere sort streg / bord kant / ikke falde ned
# - defence / attack  mechanism

from ev3.lego import *
from time import sleep
import pprint

# SETUP MOTORS
motorRight = LargeMotor('A')
motorLeft  = LargeMotor('B')

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
    motorRight.run_forever(100)
    motorLeft.run_forever(100)

def logStatus():
    pp.pprint([colorSensor.reflect, frontTouchSensor.is_pushed, backTouchSensor.is_pushed])

while(True):
    # LOGGING
    logStatus()
    # EVENTS
    if colorSensor.reflect < blackLimit:
        print "LINE DETECTED!"
    if frontTouchSensor.is_pushed:
        print "FRONT BUMPER - ATTACK!!!"
    if backTouchSensor.is_pushed:
        print "BACK BUMPER - ATTACK!!!"
    # DRIVE
    #runRandomly()