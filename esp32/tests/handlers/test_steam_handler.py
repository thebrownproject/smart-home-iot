from handlers.steam_handler import SteamHandler
import time
from comms.mqtt_client import SmartHomeMQTTClient
from comms.wifi_manager import WiFiManager

# Connect to WiFi first (required for MQTT)
wifi = WiFiManager()
wifi.connect()

mqtt = SmartHomeMQTTClient()
mqtt.connect()

steam_handler = SteamHandler()

print("="*50)
print("Testing Steam Handler")
print("="*50)

for i in range(3):
    print(f"Test {i+1}")
    steam_handler.handle_steam_detection(mqtt)
    time.sleep(1)

print("="*50)
print("Testing completed")
print("="*50)