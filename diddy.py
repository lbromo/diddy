#!/usr/bin/env python

# DIDDY; THE LEGO ROBOT SLAYER OF DOOM

from ev3.lego import *
from ev3.ev3dev import *
from time import sleep
import pprint, signal, sys

# SETUP MOTORS
motorRight = LargeMotor('C')
motorLeft  = LargeMotor('B')
SPEED = 50

# SETUP COLOR SENSORS
colorSensor = ColorSensor(1)
cornerSensor = LightSensor(4)
MAGIC_NUMBER = 17

# SETUP BUTTONS
diddyKeyboard = Key()

# CONTROLLER RELATED
Kp = 0.5
Ki = 0
Kd = 0
errorSum = 0

# PP
pp = pprint.PrettyPrinter(indent = 1)

def lineTrack(ref):
    global errorSum
    # Controller
    out = colorSensor.reflect
    error = ref - out
    errorSum = errorSum + error
    u = error * Kp + errorSum * Ki

    # Limit output
    if u > 50:
        u = 50
    elif u < -50:
        u = -50

    # Logging
    #pp.pprint([out, error, u, ])

    # Apply to motors
    motorRight.run_forever(SPEED - u)
    motorLeft.run_forever(SPEED + u)

def cornerDetected():
    if cornerSensor.reflect < 42:
        return True
    else:
        return False

def turnRight():
    motorRight.run_forever(-100)
    motorLeft.run_forever(-100)
    sleep(0.1)
    while colorSensor.reflect < MAGIC_NUMBER:
        motorRight.run_forever(-50)
        motorLeft.run_forever(50)

def suicide(signal, frame):
    print "YOU KILLED HER!"
    motorRight.stop()
    motorLeft.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, suicide)

while(True):
    # Line Tracking
    lineTrack(MAGIC_NUMBER)
    if diddyKeyboard.backspace:
        suicide(None, None)
    if cornerDetected():
       turnRight()