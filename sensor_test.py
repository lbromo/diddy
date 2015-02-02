import time
from ev3.lego import *

ts = TouchSensor()

motor = LargeMotor()

while(True):
    if(ts.is_pushed):
        motor.run_position_limited(90, 100)
        time.sleep(0.5)
        motor.run_position_limited(-90, 100)
