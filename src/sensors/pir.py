from machine import Pin
import time

class PIRSensor:
    def __init__(self, pin_number=14):
        self.pir = Pin(pin_number, Pin.IN)
    
    def read_data(self):
        return self.pir.value()

pir = PIRSensor()

# while True:
#     print(pir.read_data())
#     time.sleep(0.5)


# from machine import Pin
# import time

# PIR = Pin(14, Pin.IN)
# while True:
#     value = PIR.value()
#     print(value, end = " ")
#     if value == 1:
#         print("Some body is in this area!")
#     else:
#         print("No one!")
#     time.sleep(0.1)