import time
from utils.memory import Memory
from config import WIFI_SSID

class SystemInit:
    def __init__(self):
        # Only load essentials
        self.memory = Memory()

    def init(self):
        print("=== Smart Home System Starting ===")
        self.memory.collect("Before system init")
        self._show_welcome_message()
        self._connect_to_wifi()
        self._sync_time()
        self._connect_to_mqtt()
        self._show_ready()
        self.memory.collect("After system init")
        print("=== System Ready ===")
    
    def _show_welcome_message(self):
        from display.oled import OLED
        oled = OLED()
        oled.show_text("Welcome to", "Smart Home Lab!")
        time.sleep(2)
        oled.clear()
        del oled
        self.memory.collect("After welcome message")
    
    def _connect_to_wifi(self):
        from comms.wifi_manager import WiFiManager
        from display.oled import OLED

        wifi_manager = WiFiManager()
        oled = OLED()

        print("Connecting to WiFi...")
        if wifi_manager.connect():
            ip = wifi_manager.get_ip()
            print(f"WiFi connected to {WIFI_SSID} at ip: {ip}")
            oled.clear()
            oled.show_text("WiFi Connected", WIFI_SSID)
            time.sleep(3)
        else:
            print("WiFi connection failed!")
            oled.clear()
            oled.show_text("WiFi Failed!", "Check config")
            time.sleep(3)

        del wifi_manager, oled
        self.memory.collect("After WiFi connect")

    def _sync_time(self):
        from utils.time_sync import TimeSync
        time_sync = TimeSync()

        if time_sync.sync_time():
            print("Time synchronized successfully")
            return True
        else:
            print("Time sync failed - continuing anyway")
        print(time_sync.get_local_time())
        print(f"Is nighttime: {time_sync.is_nighttime()}")

        del time_sync
        self.memory.collect("After time sync")

    def _connect_to_mqtt(self):
        from comms.mqtt_client import SmartHomeMQTTClient
        mqtt_client = SmartHomeMQTTClient()
        mqtt_client.connect()
        del mqtt_client
        self.memory.collect("After MQTT connect")

    def _show_ready(self):
        from display.oled import OLED
        oled = OLED()
        oled.show_text("System Ready", "")
        del oled
        self.memory.collect("After show ready")

    