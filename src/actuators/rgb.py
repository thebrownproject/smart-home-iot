from machine import Pin
import neopixel
import time

class RGB:
    def __init__(self):
        self.pin = Pin(26, Pin.OUT)
        self.np = neopixel.NeoPixel(self.pin, 4)
    
    def run(self, r, g, b):
        self.np.fill((r, g, b))
        self.np.write()
    
    def stop(self):
        self.np.fill((0, 0, 0))
        self.np.write()

rgb = RGB()
rgb.run(128, 0, 0)
time.sleep(1)
rgb.stop()



# #Import Pin, neopiexl and time modules.
# from machine import Pin
# import neopixel
# import time

# #Define the number of pin and LEDs connected to neopixel.
# pin = Pin(26, Pin.OUT)
# np = neopixel.NeoPixel(pin, 4) 

# #brightness :0-255
# brightness=100                                
# colors=[[brightness,0,0],                    #red
#         [0,brightness,0],                    #green
#         [0,0,brightness],                    #blue
#         [brightness,brightness,brightness],  #white
#         [0,0,0]]                             #close

# #Nest two for loops to make the module repeatedly display five states of red, green, blue, white and OFF.    
# while True:
#     for i in range(0,5):
#         for j in range(0,4):
#             np[j]=colors[i]
#             np.write()
#             time.sleep_ms(50)
#         time.sleep_ms(500)
#     time.sleep_ms(500)