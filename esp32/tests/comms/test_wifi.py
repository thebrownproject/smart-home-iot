from comms.wifi_manager import WiFiManager

wifi_manager = WiFiManager()

print("=" * 50)
print("WiFi Manager Test")
print("=" * 50)

print("Connecting to WiFi...")
wifi_manager.connect()

print("IP address:", wifi_manager.get_ip())

print("=" * 50)
print("Test Completed")
print("=" * 50)