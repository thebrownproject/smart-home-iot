# boot.py - ESP32 Boot Configuration
# This file runs automatically when the ESP32 starts up

import gc
import machine
import time
import network
from config import WIFI_SSID, WIFI_PASSWORD

print("Smart Home System - Boot Sequence Starting...")

# Enable garbage collection for memory management
gc.collect()

# Configure system-level settings
print("System Memory:", gc.mem_free(), "bytes free")

# Configure WiFi
print("Configuring WiFi...")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

# Wait for WiFi connection
timeout = 10
while not wlan.isconnected() and timeout > 0:
    print(f"Waiting for WiFi connection... ({timeout}s left)")
    time.sleep(1)
    timeout -= 1

if wlan.isconnected():
    print("WiFi connected successfully!")
    print("IP address:", wlan.ifconfig()[0])
else:
    print("WiFi connection failed!")
    print("System will continue but network features won't work")

# Boot sequence complete - main.py will run next
print("Boot sequence complete - transferring to main.py")