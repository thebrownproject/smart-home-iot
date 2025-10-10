from machine import Pin, PWM
import time

class Buzzer:
    def __init__(self):
        self.buzzer = PWM(Pin(25))
        self.buzzer.freq(2000)  # Set frequency once (2kHz = clear beep tone)

    def beep(self, duration=0.2):
        self.buzzer.duty(100)  # ~10% duty cycle (quieter)
        time.sleep(duration)
        self.buzzer.duty(0)

    def stop(self):
        self.buzzer.duty(0)

    def pattern(self, beeps, interval=0.1):
        for i in range(beeps):
            self.beep()
            time.sleep(interval)