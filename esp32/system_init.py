from comms.wifi_manager import WiFiManager
from comms.mqtt_client import SmartHomeMQTTClient
from display.oled import OLED
from outputs.buzzer import Buzzer
from outputs.fan import Fan
from outputs.led import LED
from outputs.rgb import RGB
from outputs.servo import Servo
from sensors.dht11 import DHT11Sensor
from sensors.gas import GasSensor
from sensors.pir import PIRSensor
from sensors.steam import SteamSensor
from sensors.rfid import RFIDSensor
from utils.time_sync import TimeSync
from utils.memory import Memory
import time
from config import WIFI_SSID

class SystemInit:
    def __init__(self):
        # Communication
        self.wifi_manager = WiFiManager()
        self.supabase = None  # Lazy-loaded when needed
        self.mqtt_client = SmartHomeMQTTClient()
        # Display
        self.oled = OLED()
        # Outputs
        self.buzzer = Buzzer()
        self.fan = Fan()
        self.led = LED()
        self.rgb = RGB()
        self.door_servo = Servo(pin=13)  # Door servo on pin 13
        self.window_servo = Servo(pin=5)  # Window servo on pin 5
        # Sensors
        self.dht11 = DHT11Sensor()
        self.gas = GasSensor()
        self.pir = PIRSensor()
        self.steam = SteamSensor()
        self.rfid = RFIDSensor()
        # Utils
        self.time_sync = TimeSync()
        self.memory = Memory()

    def init(self):
        print("=== Smart Home System Starting ===")
        self.memory.collect("Before system init")
        self._show_welcome_message()
        self._connect_to_wifi()
        self._sync_time()
        self._connect_to_mqtt()
        self.oled.show_text("System Ready", "")
        self.memory.collect("After system init")
        print("=== System Ready ===")
    
    def _show_welcome_message(self):
        self.oled.show_text("Welcome to", "Smart Home Lab!")
        time.sleep(2)
        self.oled.clear()
    
    def _connect_to_wifi(self):
        self.oled.clear()
        self.oled.show_text("Connecting to", "WiFi...")
        print("Connecting to WiFi...")
        if self.wifi_manager.connect():
            # WiFi connected successfully
            ip = self.wifi_manager.get_ip()
            print(f"WiFi connected to {WIFI_SSID} at ip: {ip}")
            self.oled.clear()
            self.oled.show_text("WiFi Connected", WIFI_SSID)
            time.sleep(3)
        else:
            # WiFi failed
            print("WiFi connection failed!")
            self.oled.clear()
            self.oled.show_text("WiFi Failed!", "Check config")
            time.sleep(3)

    def _sync_time(self):
        if self.time_sync.sync_time():
            print("Time synchronized successfully")
        else:
            print("Time sync failed - continuing anyway")
        print(self.time_sync.get_local_time())
        print(f"Is nighttime: {self.time_sync.is_nighttime()}")
    
    def _connect_to_mqtt(self):
        self.mqtt_client.connect()

    