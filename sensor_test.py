import time
from ev3.lego import *

ts = TouchSensor()

motor = LargeMotor()

while(True):
    if(ts.is_pushed):
        motor.reset()
        motor.run_position_limited(90, 90)
        time.sleep(5)
	motor.reset()
        motor.run_position_limited(90, 90)
        time.sleep(5)
