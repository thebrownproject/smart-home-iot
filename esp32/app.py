import time

class SmartHomeApp:
    def __init__(self, system):
        # Store Memory reference
        self.memory = system.memory

        # Create persistent MQTT connection (can't be deleted)
        from comms.mqtt_client import SmartHomeMQTTClient
        self.mqtt = SmartHomeMQTTClient()
        self.mqtt.connect()
        self.memory.collect("After MQTT setup")

    def run(self):
        print("App running...")
        loop_count = 0
        while True:
            # Check time-based lighting every 60 seconds (1 minute)
            if loop_count % 60 == 0:
                self._handle_time_based_lighting()

            # Check motion every 5 seconds
            if loop_count % 5 == 0:
                self._handle_motion_detection()

            # Garbage collection every 10 seconds
            if loop_count % 10 == 0:
                self.memory.collect("App loop")

            loop_count += 1
            time.sleep(1)  # Loop runs every 1 second
    
    def _handle_time_based_lighting(self):
        from utils.time_sync import TimeSync
        from outputs.led import LED
        from display.oled import OLED

        time_sync = TimeSync()
        led = LED()
        oled = OLED()

        if time_sync.is_nighttime():
            led.on()
            oled.show_text("Good Evening", "lights are on")
        else:
            led.off()
            oled.show_text("Good day", "lights are off")

        del time_sync, led, oled
        self.memory.collect("After time-based lighting")

    def _handle_motion_detection(self):
        """Check PIR and respond to motion (FR2.1, FR2.2, FR2.3)"""
        from sensors.pir import PIRSensor
        from outputs.rgb import RGB

        pir = PIRSensor()
        rgb = RGB()

        if pir.is_motion_detected():
            self.memory.collect("Motion detected")

            rgb.set_color(255, 165, 0)  # Orange

            # MQTT publish (uses persistent connection)
            if self.mqtt.publish("home/motion", '{"detected": true}'):
                print("Motion - MQTT OK")

            self.memory.collect("Before DB insert")

            # Supabase insert
            try:
                from comms.supabase import Supabase
                supabase = Supabase()
                if supabase.insert_motion_event():
                    print("Motion - DB OK")
                else:
                    print("Motion - DB FAILED")
                del supabase
            except Exception as e:
                print(f"Motion - DB ERROR: {e}")

            self.memory.collect("After motion handling")
        else:
            rgb.off()

        del pir, rgb
        self.memory.collect("After motion check")
    
                