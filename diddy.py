#!/usr/bin/env python

# =============================================================================
# DIDDY, THE ROBOT SLAYER (v.01234)
# =============================================================================
PRODUCTION = True

if PRODUCTION:
    from ev3.lego import *
    from ev3.ev3dev import *
else:
    from ev3stub import *

from ev3.event_loop import *
from time import sleep
import signal, sys, time, threading, logging

# -----------------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] %(message)s',
)

now = lambda: int(round(time.time() * 1000))

# -----------------------------------------------------------------------------
# MONKEY PATCHING 'ColorSensor' + 'LightSensor' classes w. helpers
# -----------------------------------------------------------------------------
def seesBlack(self):
    if self.reflect < self.threshold:
        return True
    else:
        return False
ColorSensor.threshold = 0
ColorSensor.seesBlack = seesBlack
LightSensor.threshold = 0
LightSensor.seesBlack = seesBlack

# =============================================================================
# MEGA-MONOLITHIC-ROBOT-CLASS-OF-DOOOOOM!
# =============================================================================
class Robot(object):
    # -------------------------------------------------------------------------
    # CONTRUCTOR; PROPERTY DEFINITIONS, SENSOR SETUP UZW.
    # -------------------------------------------------------------------------
    def __init__(self, mode):
        # MODE (debug, verbose...)
        if mode == "DEBUG":
            self.DEBUG = True
        else:
            self.DEBUG = False
        # Motors
        self.motorRight = LargeMotor('C')
        self.motorLeft  = LargeMotor('B')
        self.weaponOfDoom = MediumMotor('A')
        # Speed & Control
        self.SPEED      = 30
        self.ref        = 17
        self.Kp         = 0.6
        # Line Sensors
        self.lineSensor = ColorSensor(1)
        self.caseSensor = LightSensor(4)
        self.lineSensor.threshold = 17
        self.caseSensor.threshold = 42
        # Collision Sensors
        self.frontSensor = UltrasonicSensor(3)
        self.backSensor  = UltrasonicSensor(2)
        # Buttons
        self.keyboard    = Key()
        # BOOT LOGO
        self.bootTXT     = "boot.txt"
        # STATE
        self.doubtTimer = 0
        self.state = "NORMAL"

    # -------------------------------------------------------------------------
    # STARTING / BOOTING / INIT.
    # -------------------------------------------------------------------------
    def boot(self):
        # Display boot screen...
        with open(self.bootTXT, 'r') as f:
            print f.read()
        self.start()

    # Start the loop
    def start(self):
        # Attach KILL-signal event to exit method
        signal.signal(signal.SIGINT, self.exit)
        self.weaponOfDoom.run_forever(100)
        while True:
            logging.debug(self.state)
            self.updateState()
            if self.state == "LOST":
                self.isLost()
            if self.state == "NORMAL" or self.state == "DOUBT":
                self.isNormal()

    # -------------------------------------------------------------------------
    # STATE HANDLING
    # -------------------------------------------------------------------------
    def updateState(self):
        logging.debug("Updating state...")
        if not self.lineSensor.seesBlack() and not self.caseSensor.seesBlack():
            if self.state == "NORMAL":
                self.doubtTimer = now()
                self.state = "DOUBT"
            elif self.state == "DOUBT" and (now() > (self.doubtTimer + 1500)):
                self.state = "LOST"
        else:
            self.state = "NORMAL"

    # What to do when state is normal
    def isNormal(self):
        self.lineFollow()
        if self.cornerDetected():
            self.turnRight()

    # What to when lost
    def isLost(self):
        self.motorRight.run_forever(50)
        self.motorLeft.run_forever(50)
        if self.caseSensor.seesBlack():
            while not self.lineSensor.seesBlack():
                self.motorRight.run_forever(-10)
                self.motorLeft.run_forever(30)
                self.turnRight()

    # -------------------------------------------------------------------------
    # HELPER METHODS
    # -------------------------------------------------------------------------
    def cornerDetected(self):
        if self.caseSensor.seesBlack() and self.lineSensor.seesBlack():
            return True
        else:
            return False

    def turnRight(self):
        self.motorRight.run_forever(-50)
        self.motorLeft.run_forever(50)
        sleep(0.5)
    
    # -------------------------------------------------------------------------
    # LINE FOLLOWING
    # -------------------------------------------------------------------------
    def lineFollow(self):
        y = self.lineSensor.reflect
        error = self.ref - y
        u = error * self.Kp

        maxOutput = 100 - self.SPEED
        if u > maxOutput:
            u = maxOutput
        elif u < -maxOutput:
            u = -maxOutput

        self.motorRight.run_forever(self.SPEED - u)
        self.motorLeft.run_forever(self.SPEED + u)

    # -------------------------------------------------------------------------
    # EXITING
    # -------------------------------------------------------------------------
    def exit(self, sig, frame):
        logging.debug("Exiting...")
        self.motorRight.stop()
        self.motorLeft.stop()
        sys.exit(0)

# =============================================================================
# GENTLEMEN; START YOUR ENGINES!
# =============================================================================

# Construct DIDDY!
DIDDY = Robot("DEBUG")

# BOOT DIDDY - NO TURNING BACK!!!
DIDDY.boot()
