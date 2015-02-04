# DIDDY; THE LEGO ROBOT SLAYER OF DOOM

from ev3.lego import *
from time import sleep
import pprint, signal, sys

# SETUP MOTORS
motorRight = LargeMotor('C')
motorLeft  = LargeMotor('B')
SPEED = 50

# SETUP COLOR SENSOR
colorSensor = ColorSensor(1)
blackLimit = 15

# CONTROLLER RELATED
Kp = 0.5
Ki = 0.1
Kd = 0
errorSum = 0

# PP
pp = pprint.PrettyPrinter(indent=1)

def lineTrack(ref):
    global errorSum
    # Controller
    out = colorSensor.reflect
    error = ref - out
    errorSum = errorSum + error
    u = error * Kp + errorSum * Ki

    
    if u > 50:
        u = 50
    elif u < -50:
        u = -50

    pp.pprint([out, error, u])

    # Apply to motors
    motorRight.run_forever(SPEED - u)
    motorLeft.run_forever(SPEED + u)

def logStatus():
    pp.pprint([colorSensor.reflect])

def suicide(signal, frame):
    print "YOU KILLED HER!"
    motorRight.stop()
    motorLeft.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, suicide)

while(True):
    # LOGGING
    logStatus()
    # Line Tracking
    lineTrack(17)