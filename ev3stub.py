# Stubs for EV3

# LargeMotor class
class LargeMotor(object):
    def __init__(self, port):
        self.port = port

    def stop(self):
        pass

    def run_forever(self, speed):
        return "SPEED = ", speed

class MediumMotor(object):
    def __init__(self, port):
        self.port = port

    def stop(self):
        pass

    def run_forever(self, speed):
        return "SPEED = ", speed


# ColorSensor class
class ColorSensor(object):
    def __init__(self, port):
        self.port = port

    @property
    def reflect(self):
        return 17

# LightSensor class
class LightSensor(object):
    def __init__(self, port):
        self.port = port

    @property
    def reflect(self):
        return 38

# UltrasonicSensor class
class UltrasonicSensor(object):
    def __init__(self, port):
        self.port = port

    @property
    def dist_cm(self):
        return 42

# Key class
class Key(object):
    @property
    def backspace(self):
        return 0
