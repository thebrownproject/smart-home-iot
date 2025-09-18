from machine import Pin, PWM
import time

class Buzzer:
    def __init__(self):
        self.buzzer = PWM(Pin(25))

    def run(self):
        self.buzzer.duty(100)
        buzzer.freq(100)
        time.sleep(1)
        self.buzzer.duty(0)
        
    
    def stop(self):
        self.buzzer.duty(0)

#Test the Buzzer class
buzzer = Buzzer()
buzzer.run()
time.sleep(2)
buzzer.stop()


# from machine import Pin, PWM
# from time import sleep
# buzzer = PWM(Pin(25))

# buzzer.duty(1000) 

# # Happy birthday
# buzzer.freq(294)
# sleep(0.25)
# buzzer.freq(440)
# sleep(0.25)
# buzzer.freq(392)
# sleep(0.25)
# buzzer.freq(532)
# sleep(0.25)
# buzzer.freq(494)
# sleep(0.25)
# buzzer.freq(392)
# sleep(0.25)
# buzzer.freq(440)
# sleep(0.25)
# buzzer.freq(392)
# sleep(0.25)
# buzzer.freq(587)
# sleep(0.25)
# buzzer.freq(532)
# sleep(0.25)
# buzzer.freq(392)
# sleep(0.25)
# buzzer.freq(784)
# sleep(0.25)
# buzzer.freq(659)
# sleep(0.25)
# buzzer.freq(532)
# sleep(0.25)
# buzzer.freq(494)
# sleep(0.25)
# buzzer.freq(440)
# sleep(0.25)
# buzzer.freq(698)
# sleep(0.25)
# buzzer.freq(659)
# sleep(0.25)
# buzzer.freq(532)
# sleep(0.25)
# buzzer.freq(587)
# sleep(0.25)
# buzzer.freq(532)
# sleep(0.5)
# buzzer.duty(0)