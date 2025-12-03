import time
from handlers.gas_handler import GasHandler
from comms.mqtt_client import SmartHomeMQTTClient
from comms.wifi_manager import WiFiManager

# Connect to WiFi first (required for MQTT and Supabase)
wifi = WiFiManager()
wifi.connect()

mqtt = SmartHomeMQTTClient()
mqtt.connect()

gas_handler = GasHandler()

print("="*50)
print("Testing Gas Handler")
print("="*50)

for i in range(3):
    print(f"Test {i+1}")
    gas_handler.handle_gas_detection(mqtt)
    time.sleep(1)

print("="*50)
print("Testing completed")
print("="*50)