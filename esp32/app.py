import time

class SmartHomeApp:
    def __init__(self, system):
        # Communication
        self.wifi_manager = system.wifi_manager
        self.supabase = system.supabase
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

    def run(self):
        print("App running...")
        while True:
            self._handle_time_based_lighting()
            self._handle_motion_detection()
            time.sleep(1)
    
    def _handle_time_based_lighting(self):
        if self.time_sync.is_nighttime():
            self.led.on()
            self.oled.show_text("Good Evening", "Light is on")
        else:
            self.led.off()
            self.oled.show_text("Good day", "Light is off")

    def _handle_motion_detection(self):
        if self.pir.is_motion_detected():
            self.rgb.set_color(0, 165, 165)
            self.mqtt_client.publish("home/motion", "Motion detected")
            # todo: log to database
                