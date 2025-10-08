from machine import Pin, PWM
import time

class Fan:
    def __init__(self):
        self.ina = PWM(Pin(19, Pin.OUT), 10000)
        self.inb = PWM(Pin(18, Pin.OUT), 10000)

    def run(self):
        self.ina.duty(0)
        self.inb.duty(700)
    
    def stop(self):
        self.ina.duty(0)
        self.inb.duty(0)

#Test the Fan class
fan = Fan()
fan.run()
time.sleep(2)
fan.stop()
time.sleep(1)
fan.run()
time.sleep(2)
fan.stop()



# from machine import Pin,PWM
# import time
# #Two pins of the motor
# INA =PWM(Pin(19,Pin.OUT),10000)#INA corresponds to IN+
# INB =PWM(Pin(18,Pin.OUT),10000)#INB corresponds to IN- 

# try:
#     while True:
#         #Counterclockwise 2s
#         INA.duty(0) #The range of duty cycle is 0-1023
#         INB.duty(700)
#         time.sleep(2)
#         #stop 1s
#         INA.duty(0)
#         INB.duty(0)
#         time.sleep(1)
#         #Turn clockwise for 2s
#         INA.duty(600)
#         INB.duty(0)
#         time.sleep(2)
#         #stop 1s
#         INA.duty(0)
#         INB.duty(0)
#         time.sleep(1)
# except:
#     INA.duty(0)
#     INB.duty(0)
#     INA.deinit()
#     INB.deinit()