from handlers.environment_handler import EnvironmentHandler
from comms.mqtt_client import SmartHomeMQTTClient
from comms.wifi_manager import WiFiManager
import time

wifi = WiFiManager()
wifi.connect()

mqtt = SmartHomeMQTTClient()
mqtt.connect()

environment_handler = EnvironmentHandler()

print("="*50)
print("Testing Environment Handler")
print("="*50)

for i in range(3):
    print(f"Test {i+1}")
    environment_handler.handle_environment_detection(mqtt)
    time.sleep(1)

print("="*50)
print("Testing completed")
print("="*50)