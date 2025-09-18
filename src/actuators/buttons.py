from machine import Pin
import time

class Button1:
    def __init__(self):
        self.button1 = Pin(16, Pin.IN, Pin.PULL_UP)
    
    def read_data(self):
        return self.button1.value()

class Button2:
    def __init__(self):
        self.button2 = Pin(27, Pin.IN, Pin.PULL_UP)

    def read_data(self):
        return self.button2.value()


button1 = Button1()
button2 = Button2()

while True:
    print(button1.read_data())
    print(button2.read_data())
    time.sleep(1)
