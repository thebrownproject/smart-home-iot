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
            time.sleep(1)
            if self.time_sync.is_nighttime():
                self.led.on()
                self.oled.show_text("Good Evening", "Light is on")
            else:
                self.led.off()
                self.oled.show_text("Good day", "Light is off")