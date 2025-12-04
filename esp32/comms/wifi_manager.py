import network
import time
from config import WIFI_SSID, WIFI_PASSWORD

class WiFiManager:
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.max_retries = 5

    def connect(self):
        if self.wlan.isconnected():
            print(f"Already connected to WiFi: {WIFI_SSID}")
            print(f"IP address: {self.wlan.ifconfig()[0]}")
            return True

        # Reset WiFi interface to clear any error states
        try:
            self.wlan.disconnect()
        except Exception:
            pass

        self.wlan.active(False)
        time.sleep(0.5)
        self.wlan.active(True)

        print(f"Connecting to WiFi: {WIFI_SSID}")
        self.wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        for attempt in range(self.max_retries):
            if self.wlan.isconnected():
                print(f"WiFi connected successfully!")
                print(f"IP address: {self.wlan.ifconfig()[0]}")
                return True

            print(f"Attempt {attempt + 1}/{self.max_retries} - waiting 2s...")
            time.sleep(2)

        print("WiFi connection failed after all retries")
        print("System will continue but network features won't work")
        return False

    def get_ip(self):
        if self.wlan.isconnected():
            return self.wlan.ifconfig()[0]
        return None