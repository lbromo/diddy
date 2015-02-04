#!/usr/bin/env python

# DIDDY; THE LEGO ROBOT SLAYER OF DOOM

from ev3.lego import *
from ev3.ev3dev import *
from time import sleep
import pprint, signal, sys, time

# SETUP MOTORS
motorRight = LargeMotor('C')
motorLeft  = LargeMotor('B')
SPEED = 30

# SETUP COLOR SENSORS
colorSensor = ColorSensor(1)
cornerSensor = LightSensor(4)
MAGIC_NUMBER = 17

# SETUP BUTTONS
diddyKeyboard = Key()

# CONTROLLER RELATED
Kp = 0.6

# PP
pp = pprint.PrettyPrinter(indent = 1)

def lineTrack(ref):
    global errorSum
    # Controller (proportional controller)
    out = colorSensor.reflect
    error = ref - out
    u = error * Kp

    # Limit output to maximum output
    maxOutput = 100 - SPEED
    if u > maxOutput:
        u = maxOutput
    elif u < -maxOutput:
        u = -maxOutput

    # Logging
    #pp.pprint([out, error, u, ])

    # Apply to motors
    motorRight.run_forever(SPEED - u)
    motorLeft.run_forever(SPEED + u)

def cornerDetected():
    if cornerSensor.reflect < 42 and isBlack():
        return True
    else:
        return False

def isBlack():
    if colorSensor.reflect < MAGIC_NUMBER:
        return True
    else:
        return False

def turnRight():
    motorRight.run_forever(-50)
    motorLeft.run_forever(50)
    sleep(0.5)

def printLogo():
    print """
                                  /
                   __       //
                   -\= \=\ //
                 --=_\=---//=--
               -_==/  \/ //\/--
                ==/   /O   O\==--
   _ _ _ _     /_/    \  ]  /--
  /\ ( (- \    /       ] ] ]==-
 (\ _\_\_\-\__/     \  (,_,)--
(\_/                 \     \-
\/      /       (   ( \  ] /)
/      (         \   \_ \./ )
(       \         \      )  \\
(       /\_ _ _ _ /---/ /\_  \\
 \     / \     / ____/ /   \  \\
  (   /   )   / /  /__ )   (  )
  (  )   / __/ '---`       / /
  \  /   \ \             _/ /
  ] ]     )_\_         /__\/
  /_\     ]___\\
 (___)
    """

def suicide(signal, frame):
    print "YOU KILLED HER!"
    motorRight.stop()
    motorLeft.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, suicide)

# PRINT LOGO
printLogo()

now = lambda: int(round(time.time() * 1000))

maybeLostTime = 0
diddyIsMaybeLost = False
diddyIsLost = False

while(True):
    
    # Check state
    if not isBlack() and not cornerDetected():
        print "GREY.ALL.OVER!"
        if (not diddyIsMaybeLost):
            print "FIRST TIME MAYBE LOST!"
            maybeLostTime = now()
            diddyIsMaybeLost = True
        elif (diddyIsMaybeLost and now() > maybeLostTime + 1500):
            diddyIsLost = True
    else:
        diddyIsMaybeLost = False
        diddyIsLost = False

    if diddyIsLost:
        print "LOST - RUN STRAIGHT"
        motorRight.run_forever(30)
        motorLeft.run_forever(30)

    if not diddyIsLost:
        lineTrack(MAGIC_NUMBER)
        if cornerDetected():
            turnRight()

    if diddyKeyboard.backspace:
        suicide(None, None)