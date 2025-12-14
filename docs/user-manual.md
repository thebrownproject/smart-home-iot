# Zap Smart Home - User Manual

## Table of Contents

1. [Introduction](#introduction)
2. [Hardware Setup](#hardware-setup)
3. [Software Installation](#software-installation)
4. [Environment Configuration](#environment-configuration)
5. [System Operation](#system-operation)
6. [Web Dashboard Usage](#web-dashboard-usage)
7. [Troubleshooting](#troubleshooting)
8. [Maintenance](#maintenance)

---

## Introduction

Zap Smart Home is an IoT automation system that monitors environmental conditions, manages security through RFID access control, and provides real-time web-based monitoring and control.

### System Overview

**Components:**
- ESP32 microcontroller with multiple sensors
- C# API middleware
- Next.js web dashboard
- PostgreSQL database (Supabase)
- MQTT message broker

**Features:**
- Environmental monitoring (temperature, humidity, gas, steam)
- Motion detection and security alerts
- RFID access control
- Remote control of door, window, and fan
- Real-time web dashboard

---

## Hardware Setup

### ESP32 Pin Connections

**Required Hardware:**
- ESP32 Development Board
- KS5009 Smart Home Kit sensors and outputs
- Power supply (5V USB)

**Pin Layout:**

| Component | ESP32 Pin | Notes |
|-----------|-----------|-------|
| OLED Display (SSD1306) | GPIO 21 (SDA), GPIO 22 (SCL) | I2C, Address: 0x3C |
| RFID Reader (RC522) | GPIO 21 (SDA), GPIO 22 (SCL) | I2C, Address: 0x28 |
| DHT11 Sensor | GPIO 17 | Temperature/Humidity |
| PIR Motion Sensor | GPIO 14 | Motion detection |
| Gas Sensor | GPIO 23 | Gas detection |
| Steam/Moisture Sensor | GPIO 34 | ADC, Moisture detection |
| RGB LED (SK6812) | GPIO 26 | Status indicators |
| Door Servo Motor | GPIO 13 | PWM control |
| Window Servo Motor | GPIO 5 | PWM control |
| Buzzer | GPIO 25 | Alert sounds |
| Fan Motor | GPIO 19 (INA), GPIO 18 (INB) | PWM control |
| Button | GPIO 16 | Manual input |

### Assembly Instructions

**Step 1:** Connect I2C devices
- OLED Display: Connect SDA to GPIO 21, SCL to GPIO 22
- RFID Reader: Connect SDA to GPIO 21, SCL to GPIO 22 (shared I2C bus)

**Step 2:** Connect sensors
- DHT11: Connect data pin to GPIO 17, VCC to 3.3V, GND to ground
- PIR: Connect signal to GPIO 14, VCC to 5V, GND to ground
- Gas Sensor: Connect signal to GPIO 23, VCC to 5V, GND to ground

**Step 3:** Connect outputs
- RGB LED: Connect data to GPIO 12, VCC to 5V, GND to ground
- Servo: Connect control to GPIO 13, VCC to 5V, GND to ground
- Buzzer: Connect to GPIO 4, VCC to 3.3V, GND to ground

**Step 4:** Power up
- Connect ESP32 to computer via USB cable
- Verify all connections are secure

---

## Software Installation

### ESP32 Development Environment

**Required Software:**
- Visual Studio Code
- MicroPico extension
- Python 3.8+ (for MicroPython)
- ESP32 firmware

**Installation Steps:**

1. **Install VS Code**
   - Download from https://code.visualstudio.com/
   - Install MicroPico extension

2. **Flash MicroPython firmware**
   - Download latest ESP32 MicroPython firmware
   - Use esptool.py to flash firmware
   - Command: `esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash`
   - Command: `esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 firmware.bin`

3. **Configure project**
   - Copy ESP32 code to project folder
   - Configure WiFi credentials in `config.py`
   - Upload code to ESP32 using MicroPico

### Web Dashboard Setup

**Prerequisites:**
- Node.js 18+
- npm or yarn
- Git

**Installation:**

1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd smart-home-project
   ```

2. **Install dependencies**
   ```bash
   cd web
   npm install
   ```

3. **Configure environment**
   - Copy `.env.example` to `.env.local`
   - Add required environment variables

4. **Run development server**
   ```bash
   npm run dev
   ```

5. **Access dashboard**
   - Open browser to `http://localhost:3000`

---

## Environment Configuration

### ESP32 Configuration

**File:** `esp32/config.py`

**Setup Steps:**
1. Copy the example configuration: `cp esp32/config.example.py esp32/config.py`
2. Edit `config.py` and replace placeholder values with your actual credentials
3. Never commit `config.py` to version control (it's in .gitignore)

**Configuration Reference:**
See `esp32/config.example.py` in the repository for complete configuration structure including:
- WiFi credentials
- MQTT broker settings and credentials
- Device identification
- MQTT topic definitions
- Time zone and operational settings

**Example Configuration Values:**
```python
# Device Identity
DEVICE_ID = "esp32_main"

# WiFi Configuration
WIFI_SSID = "your_network_name"
WIFI_PASSWORD = "your_wifi_password"

# MQTT Broker (HiveMQ Cloud)
MQTT_BROKER = "your-broker.hivemq.cloud"
MQTT_PORT = 8883  # SSL/TLS
MQTT_USER = "your_mqtt_username"
MQTT_PASSWORD = "your_mqtt_password"
```

### Web Dashboard Configuration

**Environment Variables:**
```
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
NEXT_PUBLIC_MQTT_BROKER=your_mqtt_broker
```

### API Configuration

**Production Settings:**
```json
{
  "SupabaseUrl": "your_supabase_url",
  "SupabaseApiKey": "your_supabase_key",
  "MqttBroker": "your_mqtt_broker",
  "DeviceUuid": "your_device_uuid"
}
```

---

## System Operation

### Boot Sequence

1. **ESP32 Initialization**
   - WiFi connection established
   - MQTT broker connection
   - Hardware initialization
   - Display startup message

2. **Sensor Reading Cycle**
   - Environmental sensors: Every 30 minutes
   - Motion detection: Continuous
   - Gas monitoring: Continuous
   - RFID scans: On demand

3. **Data Flow**
   - ESP32 → MQTT → C# API → Database
   - ESP32 → MQTT → Web Dashboard (real-time)

### Alert System

**Priority Levels:**
1. **Gas Alert** - Critical, activates fan immediately
2. **Steam Alert** - High priority, activates fan
3. **Motion Alert** - Medium priority, visual indicator
4. **Asthma Alert** - Medium priority, notification
5. **Normal Operation** - Standard monitoring

---

## Web Dashboard Usage

### Accessing the Dashboard

**URL:** https://zap-smart-home.vercel.app/

### Main Dashboard

**Real-time Data:**
- Current temperature and humidity
- Motion status
- Gas level readings
- System status indicators

**Control Panel:**
- Manual door control (open/close)
- Window control (open/close)
- Fan control (on/off/auto)
- Light control (RGB LED)

### RFID Log

**Features:**
- View recent RFID scan attempts
- Access granted/denied status
- Timestamp and card ID information
- Filter by date or result

### Historical Data

**Charts and Graphs:**
- Temperature trends over time
- Humidity levels
- Motion events
- Gas level history

**Export Options:**
- Download data as CSV
- Generate PDF reports
- Email reports (future feature)

---

## Troubleshooting

### Common Issues

**ESP32 Connection Problems:**
- Check WiFi credentials
- Verify MQTT broker settings
- Check power supply
- Restart ESP32

**Sensor Readings Incorrect:**
- Verify pin connections
- Check sensor calibration
- Test sensors individually
- Review error logs

**Web Dashboard Not Loading:**
- Check internet connection
- Verify environment variables
- Check browser console for errors
- Try different browser

**RFID Not Working:**
- Check RFID reader wiring
- Verify I2C address (0x28)
- Test with known card
- Check antenna connection

### Error Codes

**ESP32 Display Messages:**
- "WiFi Connecting..." - Normal startup
- "MQTT Connected" - Broker connected
- "Sensor Error" - Sensor reading failed
- "Alert: Gas" - Gas level critical
- "RFID OK" - Access granted
- "RFID Denied" - Access denied

### Getting Help

**Logs and Diagnostics:**
- ESP32 serial output
- Web browser console
- API logs (production)
- Database query logs

**Support Resources:**
- Project documentation
- GitHub issues
- Community forums

---

## Maintenance

### Regular Tasks

**Weekly:**
- Check sensor readings accuracy
- Review alert logs
- Test manual controls
- Verify backup power

**Monthly:**
- Clean sensors and connections
- Update firmware (if available)
- Review system performance
- Check database integrity

**Quarterly:**
- Replace batteries (if applicable)
- Test emergency procedures
- Review security settings
- Update documentation

### System Updates

**ESP32 Updates:**
- Update via MicroPico upload
- Backup current configuration
- Test all functions after update

**Web Dashboard Updates:**
- Deployed automatically via Vercel
- Check for breaking changes
- Test new features before production

**API Updates:**
- Manual deployment to DigitalOcean
- Test in staging environment
- Monitor deployment logs

---

## Appendices

### Appendix A: Technical Specifications

### Appendix B: API Reference

### Appendix C: MQTT Topics Reference

### Appendix D: Hardware Datasheets

---

**Document Version:** 1.0
**Last Updated:** December 2025
**Author:** Fraser Brown
**Project:** Zap Smart Home IoT System
