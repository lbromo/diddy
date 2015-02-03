# DIDDY; THE LEGO ROBOT SLAYER OF DOOM

# - koere tilfaeldigt
# - detektere sort streg / bord kant / ikke falde ned
# - defence / attack  mechanism

from ev3.lego import *
from time import sleep
import pprint, signal

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
    motorRight.run_forever(50 + direction)
    motorLeft.run_forever(50 - direction)

def logStatus():
    pp.pprint([colorSensor.reflect, frontTouchSensor.is_pushed, backTouchSensor.is_pushed])

def suicide():
    print "YOU KILLED HER!"
    motorRight.stop()
    motorLeft.stop()

signal.signal(signal.SIGINT, suicide)

while(True):
    # LOGGING
    logStatus()
    # EVENTS
    if colorSensor.reflect < blackLimit:
        runRandomly(50)
    else:
        runRandomly()
    if frontTouchSensor.is_pushed:
        print "FRONT BUMPER - ATTACK!!!"
    if backTouchSensor.is_pushed:
        print "BACK BUMPER - ATTACK!!!"