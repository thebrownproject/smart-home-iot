"""
ESP32 Configuration Template

⚠️  IMPORTANT: This is a template file.

To set up your ESP32:
1. Copy this file: `cp config.example.py config.py`
2. Replace placeholder values with your actual credentials
3. Upload config.py to ESP32 (never commit it to git)
"""

# WiFi Configuration
WIFI_SSID = "your_network"
WIFI_PASSWORD = "your_password"

# MQTT Broker (HiveMQ Cloud)
MQTT_BROKER = "broker.hivemq.cloud"
MQTT_PORT = 8883  # SSL/TLS
MQTT_USER = "your_username"
MQTT_PASSWORD = "your_password"

# Supabase (Direct HTTP)
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_ANON_KEY = "your_anon_key"
