from machine import Pin, PWM

class Buzzer:
    def __init__(self):
        self.buzzer = PWM(Pin(25))
        self.buzzer.duty(0)     # Ensure buzzer starts silent

    def start(self):
        self.buzzer.freq(1000)
        self.buzzer.duty(10)  # ~10% duty cycle (quieter)

    def stop(self):
        self.buzzer.duty(0)