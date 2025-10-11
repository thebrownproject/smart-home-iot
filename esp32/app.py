import time
import gc

class SmartHomeApp:
    def __init__(self, system):
        # Communication
        self.wifi_manager = system.wifi_manager
        self.supabase = None  # Lazy-loaded when needed
        self.mqtt_client = system.mqtt_client
        # Display
        self.oled = system.oled
        # Outputs
        self.buzzer = system.buzzer
        self.fan = system.fan
        self.led = system.led
        self.rgb = system.rgb
        self.door_servo = system.door_servo
        self.window_servo = system.window_servo
        # Sensors
        self.dht11 = system.dht11
        self.gas = system.gas
        self.pir = system.pir
        self.steam = system.steam
        self.rfid = system.rfid
        # Utils
        self.time_sync = system.time_sync
        self.memory = system.memory

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
        if self.time_sync.is_nighttime():
            self.led.on()
            self.oled.show_text("Good Evening", "lights are on")
        else:
            self.led.off()
            self.oled.show_text("Good day", "lights are off")

    def _handle_motion_detection(self):
        """Check PIR and respond to motion (FR2.1, FR2.2, FR2.3)"""
        if self.pir.is_motion_detected():
            # Free memory BEFORE network operations
            self.memory.collect("Motion detection")

            self.rgb.set_color(255, 165, 0)  # Orange

            # MQTT publish (lightweight, ~1KB)
            if self.mqtt_client.publish("home/motion", '{"detected": true}'):
                print("Motion - MQTT OK")

            # Aggressive cleanup before HTTP
            self.memory.collect("Before DB insert")

            # Lazy-load Supabase only when needed
            try:
                from comms.supabase import Supabase
                supabase = Supabase()
                if supabase.insert_motion_event():
                    print("Motion - DB OK")
                else:
                    print("Motion - DB FAILED")
                # Delete reference immediately to free memory
                del supabase
            except Exception as e:
                print(f"Motion - DB ERROR: {e}")

            # Final cleanup
            self.memory.collect("After DB insert")
        else:
            self.rgb.off()
    
                