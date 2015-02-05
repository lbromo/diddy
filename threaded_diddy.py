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

# Shared variables
enemy_flag_lock = threading.Lock()
enemy_flag = False

def incomingEnemy():
    global enemy_flag, enemy_flag_lock
    frontSensor = UltrasonicSensor(3)
    backSensor  = UltrasonicSensor(2)

    while True:
        with enemy_flag_lock:
            enemy_flag = True if (frontSensor.dist_cm < 30) or ( (backSensor.dist_cm/10) < 30 ) else False
        sleep(0.1)


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
        self.motorRight           = LargeMotor('C')
        self.motorLeft            = LargeMotor('B')
        # Speed & Control
        self.ref                  = 17
        # Line Sensors
        self.lineSensor           = ColorSensor(1)
        self.caseSensor           = LightSensor(4)
        self.lineSensor.threshold = 17
        self.caseSensor.threshold = 42
        # Buttons
        self.keyboard             = Key()
        # BOOT LOGO
        self.bootTXT              = "boot.txt"
        # STATE
        self.doubtTimer           = 0
        self.state                = "NORMAL"

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

        while True:
            #logging.debug(self.state)
            self.updateState()
            if self.state == "LOST":
                self.isLost()
            if self.state == "NORMAL" or self.state == "DOUBT":
                self.isNormal()
            if self.keyboard.backspace:
                self.exit(None, None)

    # -------------------------------------------------------------------------
    # STATE HANDLING
    # -------------------------------------------------------------------------
    def updateState(self):
        #logging.debug("Updating state...")
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
        global enemy_flag_lock, enemy_flag
        with enemy_flag_lock:
            if enemy_flag:
                speed = 80
                kp = 0.85
            else:
                speed = 30
                kp = 0.6

        self.lineFollow(speed, kp)
        if self.cornerDetected():
            self.turnRight()

    # What to when lost
    def isLost(self):
        self.motorRight.run_forever(50)
        self.motorLeft.run_forever(50)
        # !! M{ikke dansk bogstaver}SKE SKIDT => ER SET FOR{ikke danske bogstaver}RSAGE UENDELIG L{ikke danske bogstaver}KKE !!
        if self.caseSensor.seesBlack():
            while not self.lineSensor.seesBlack():
                self.motorRight.run_forever(-10)
                self.motorLeft.run_forever(30)
                self.turnRight()

    # -------------------------------------------------------------------------
    # HELPER METHODS
    # -------------------------------------------------------------------------
    def incomingEnemy(self):
        if self.frontSensor.dist_cm < 30: #or (self.backSensor.dist_cm/10) < 30:
            return True
        else:
            return False

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
    def lineFollow(self, speed, kp):
        y = self.lineSensor.reflect
        error = self.ref - y
        u = error * kp
        
        maxOutput = 100 - speed
        if u >= maxOutput:
            u = maxOutput
        elif u <= -maxOutput:
            u = -maxOutput
            
        self.motorRight.run_forever(speed - u)
        self.motorLeft.run_forever(speed + u)

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

t = threading.Thread(target = incomingEnemy)

if __name__ == '__main__':
    t.setDaemon(True)
    t.start()

    # Construct DIDDY!
    DIDDY = Robot("DEBUG")

    # START DIDDY - NO TURNING BACK!!!
    DIDDY.start()
