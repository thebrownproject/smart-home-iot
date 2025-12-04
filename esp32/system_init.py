import time
from utils.memory import Memory
from config import WIFI_SSID

class SystemInit:
    def __init__(self):
        self.memory = Memory()

    def init(self):
        print("=== Smart Home System Starting ===")
        self.memory.collect("Before system init")
        self._show_welcome_message()
        self._connect_to_wifi()
        self._sync_time()
        self.memory.collect("After system init")
        print("=== System Ready ===")
    
    def _show_welcome_message(self):
        from outputs.oled import OLED
        oled = OLED()
        oled.show_text("Welcome to", "Smart Home Lab")
        time.sleep(1.5)
        oled.show_text("Please wait", "System starting")
        time.sleep(1)
        del oled
        self.memory.collect("After welcome message")
    
    def _connect_to_wifi(self):
        from comms.wifi_manager import WiFiManager
        from outputs.oled import OLED

        wifi_manager = WiFiManager()
        oled = OLED()

        print("Connecting to WiFi...")
        oled.show_text("WiFi", "Connecting...")
        if wifi_manager.connect():
            ip = wifi_manager.get_ip()
            print(f"WiFi connected to {WIFI_SSID} at ip: {ip}")
            oled.show_text("WiFi Connected", WIFI_SSID)
            time.sleep(1)
        else:
            print("WiFi connection failed!")
            oled.show_text("WiFi Error", "Check Config")
            time.sleep(2)

        del wifi_manager, oled
        self.memory.collect("After WiFi connect")

    def _sync_time(self):
        from utils.time_sync import TimeSync
        from outputs.oled import OLED

        oled = OLED()
        time_sync = TimeSync()

        oled.show_text("Time Sync", "Connecting...")
        if time_sync.sync_time():
            print("Time synchronized successfully")
            local_time = time_sync.get_local_time()  # Returns tuple (year, month, day, hour, min, sec, ...)
            hour = local_time[3]
            minute = local_time[4]

            # Convert 24-hour to 12-hour with AM/PM
            display_hour = hour % 12 or 12  # 0 becomes 12 (midnight/noon)
            period = "AM" if hour < 12 else "PM"
            time_str = "{:02d}:{:02d} {}".format(display_hour, minute, period)
            oled.show_text("Time Synced", time_str)
            time.sleep(1)
        else:
            print("Time sync failed - continuing anyway")
            oled.show_text("Time Sync", "Failed")
            time.sleep(1.5)

        print(time_sync.get_local_time())
        print(f"Is nighttime: {time_sync.is_nighttime()}")

        del time_sync, oled
        self.memory.collect("After time sync")

    