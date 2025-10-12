from utils.memory import Memory

class SteamHandler:
    def __init__(self):
        self.memory = Memory()

    def handle_steam_detection(self, mqtt):
        from sensors.steam import SteamSensor
        from outputs.rgb import RGB
        from outputs.servo import Servo
        
        steam = SteamSensor()
        rgb = RGB()
        window_servo = Servo(pin=5)  # Window servo

        if steam.is_moisture_detected():
            self.memory.collect("SteamHandler - Steam detected")
            # Flash RGB blue (FR3.3) - use RGB flash method for temporary indicator
            rgb.flash((0, 0, 255), 3)  # Blue flash 3 times
            window_servo.close()
            if mqtt.publish("home/steam", '{"detected": true}'):
                print("SteamHandler - MQTT Publish OK")
            self.memory.collect("SteamHandler - Steam detected")
        # Don't turn off RGB - let other handlers control their states
        else:
            print("SteamHandler - No steam detected")

        del steam, rgb, window_servo
        self.memory.collect("After steam handling")