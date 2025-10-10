# main.py - Smart Home System Entry Point
from comms.wifi_manager import WiFiManager
from display.oled import OLED
import time
from config import WIFI_SSID
print("=== Smart Home System Starting ===")

# Initialize hardware
wifi_manager = WiFiManager()
oled = OLED()

# Show welcome message
oled.show_text("Welcome to", "Smart Home Lab!")
time.sleep(2)

# Connect to WiFi
oled.clear()
oled.show_text("Connecting to", "WiFi...")
print("Connecting to WiFi...")

if wifi_manager.connect():
    # WiFi connected successfully
    ip = wifi_manager.get_ip()
    print(f"WiFi connected to {WIFI_SSID} at ip: {ip}")
    oled.clear()
    oled.show_text("WiFi Connected", WIFI_SSID)
    time.sleep(3)
else:
    # WiFi failed
    print("WiFi connection failed!")
    oled.clear()
    oled.show_text("WiFi Failed!", "Check config")
    time.sleep(3)

# Ready
oled.clear()
oled.show_text("System Ready", "")
print("=== System Ready ===")

# TODO: Main application loop will go here
# For now, just keep system running
print("Main loop not implemented yet - entering Test Mode")
oled.clear()
oled.show_text("Test Mode", "Ready")

# app = SmartHomeApp()
# app.run()