from comms.wifi_manager import WiFiManager
from display.oled import OLED
from utils.time_sync import TimeSync
import time
from config import WIFI_SSID

class SystemInit:
    def __init__(self):
        self.wifi_manager = WiFiManager()
        self.oled = OLED()
        self.time_sync = TimeSync()
    
    def show_welcome_message(self):
        self.oled.show_text("Welcome to", "Smart Home Lab!")
        time.sleep(2)
        self.oled.clear()
    
    def connect_to_wifi(self):
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

    def sync_time(self):
        if self.time_sync.sync_time():
            print("Time synchronized successfully")
        else:
            print("Time sync failed - continuing anyway")
        print(self.time_sync.get_local_time())
        print(f"Is nighttime: {self.time_sync.is_nighttime()}")

    def init(self):
        print("=== Smart Home System Starting ===")
        self.show_welcome_message()
        self.connect_to_wifi()
        self.sync_time()
        self.oled.show_text("System Ready", "")
        print("=== System Ready ===")