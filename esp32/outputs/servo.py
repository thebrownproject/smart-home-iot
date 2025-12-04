from machine import Pin, PWM

'''
The duty cycle corresponding to the angle
0°----2.5%----25
45°----5%----51.2
90°----7.5%----77
135°----10%----102.4
180°----12.5%----128
'''

class Servo:
    def __init__(self, pin):
        self.servo = PWM(Pin(pin))
        self.servo.freq(50)  # Standard servo frequency (50Hz)
        self.angle_closed = 25   # 0° duty cycle
        self.angle_open = 128    # 180° duty cycle
        self.is_open = None 

    def open(self):
        self.servo.duty(self.angle_open)
        self.is_open = True

    def close(self):
        self.servo.duty(self.angle_closed)
        self.is_open = False

class DoorServoManager:
    """Manages door servo with open and close methods and a countdown timer."""
    def __init__(self):
        self.servo = Servo(pin=13)
        self.countdown = 0
        self.is_open = None
    
    def open(self, duration=5):
        self.servo.open()
        self.is_open = True
        self.countdown = duration

    def close(self):
        self.servo.close()
        self.is_open = False
        self.countdown = 0

    def update(self):
        if self.countdown > 0:
            self.countdown -= 1
            if self.countdown == 0 and self.is_open:
                self.close()