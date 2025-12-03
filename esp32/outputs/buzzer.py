from machine import Pin, PWM

class Buzzer:
    def __init__(self):
        self.buzzer = PWM(Pin(25))
        self.buzzer.duty(0)     # Ensure buzzer starts silent
        self.is_running = False

    def start(self):
        self.buzzer.freq(1000)
        self.buzzer.duty(10)  # ~10% duty cycle (quieter)
        self.is_running = True

    def stop(self):
        self.buzzer.duty(0)
        self.is_running = False

class BuzzerManager:
    def __init__(self):
        self.buzzer = Buzzer()
        self.countdown = 0
        self.is_running = False

    def start(self, duration):
        self.buzzer.start()
        self.is_running = True
        self.countdown = duration

    def stop(self):
        self.buzzer.stop()
        self.is_running = False
        self.countdown = 0

    def update(self):
        if self.countdown > 0:
            self.countdown -= 1
            if self.countdown == 0 and self.is_running:
                self.stop()
