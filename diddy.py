# DIDDY; THE LEGO ROBOT SLAYER OF DOOM

# - køre tilfældigt
# - detektere sort streg / bord kant / ikke falde ned
# - defence / attack  mechanism

from ev3dev import *
from ev3dev_utils.motors import *
from observable import *

class MotorController(observer):
    def __init__(self, motorLeft, motorRight):
        self.motorLeft = motorLeft
        self.motorRight = motorRight

    def update(*args, **kwargs):
        if(type):
            pass


# SETUP MOTORS
motorRight = dc_motor(OUTPUT_A)
motorLeft  = dc_motor(OUTPUT_B)

# SETUP TOUCH SENSORS
frontTouchSensor = touch_sensor(INPUT_1)
backTouchSensor  = touch_sensor(INPUT_2)

# SETUP COLOR SENSOR
colorSensor = color_sensor(INPUT_3)

# SETUP GYRO
gyroSensor = gyro_sensor(INPUT_4)


def runRandomly(direction = 0):
    drive_for(motorLeft, motorRight, dir = direction, power = 100)

while(True)
    runRandomly()