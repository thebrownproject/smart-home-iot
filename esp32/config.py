"""
ESP32 Configuration Template

⚠️  IMPORTANT: This is a template file.

To set up your ESP32:
1. Copy this file: `cp config.example.py config.py`
2. Replace placeholder values with your actual credentials
3. Upload config.py to ESP32 (never commit it to git)
"""

# Device Idendity
DEVICE_ID = "esp32_main"

# WiFi Configuration
WIFI_SSID = "TP-LINK_DC8B"
WIFI_PASSWORD = "27653975"
WIFI_SSID = "CyFi"
WIFI_PASSWORD = "SecurityA40"

# MQTT
# MQTT Broker (HiveMQ Cloud)
MQTT_BROKER = "301d2478bf674954a8b8e5ad05732a73.s1.eu.hivemq.cloud"
MQTT_PORT = 8883  # SSL/TLS
MQTT_USER = "thebrownproject"
MQTT_PASSWORD = "StrongPassword123!"
# MQTT Topics Outgoing
# Sensor Data
TOPIC_SENSOR_DATA = f"devices/{DEVICE_ID}/data"
TOPIC_ASTHMA_ALERT = f"devices/{DEVICE_ID}/asthma_alert"
# RFID Request
TOPIC_RFID_REQUEST = f"devices/{DEVICE_ID}/rfid/check"
# Status Updates (for web dashboard display - FR8.4, FR8.5)
TOPIC_STATUS_DOOR = f"devices/{DEVICE_ID}/status/door"
TOPIC_STATUS_WINDOW = f"devices/{DEVICE_ID}/status/window"
TOPIC_STATUS_FAN = f"devices/{DEVICE_ID}/status/fan"
# MQTT Topics Incoming
# RFID Response
TOPIC_RFID_RESPONSE = f"devices/{DEVICE_ID}/rfid/response"
# Control Commands (for web remote control - FR9.1, FR9.2, FR9.3)
TOPIC_CONTROL_DOOR = f"devices/{DEVICE_ID}/control/door"
TOPIC_CONTROL_WINDOW = f"devices/{DEVICE_ID}/control/window"
TOPIC_CONTROL_FAN = f"devices/{DEVICE_ID}/control/fan"

# Time Configuration (NTP)
TIMEZONE_OFFSET_HOURS = 11  # AEDT (Melbourne/Sydney) UTC+10
NIGHT_START_HOUR = 20       # 8pm
NIGHT_END_HOUR = 7          # 7am