from machine import Pin
import time

class LED:
    def __init__(self):
        self.led = Pin(12, Pin.OUT)
    
    def run(self):
        self.led.value(1)
    
    def stop(self):
        self.led.value(0)
    
    def blink(self, noBlinks, delay):
        i = 0
        while i < noBlinks:
            self.led.value(1)
            time.sleep(delay)
            self.led.value(0)
            time.sleep(delay)
            i += 1

led = LED()
led.run()
time.sleep(1)
led.stop()
time.sleep(1)
led.blink(5, .2)




# from machine import Pin
# import time

# led = Pin(12, Pin.OUT)# Build an LED object, connect the external LED light to pin 0, and set pin 0 to output mode
# while True:
#     led.value(1)# turn on led
#     time.sleep(1)# delay 1s
#     led.value(0)# turn off led
#     time.sleep(1)# delay 1s