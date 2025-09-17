# Hardware Validation Tests

## Overview

This directory contains comprehensive hardware validation tests for the KS5009 Smart Home system. These tests verify that all hardware components are properly connected and functional before software implementation begins.

## Files

- `test_connections.py` - Main hardware component testing
- `test_wifi.py` - WiFi connectivity validation
- `run_all_tests.py` - Complete test suite runner
- `i2c_lcd.py` - LCD display library (copied from reference code)
- `lcd_api.py` - LCD API library (copied from reference code)

## Hardware Components Tested

### I2C Devices
- **LCD Display**: I2C address 0x27, pins SDA:21, SCL:22
- **RFID Reader**: I2C address 0x28, pins SDA:21, SCL:22

### Digital I/O
- **PIR Motion Sensor**: Pin 14 (digital input)
- **Gas Sensor**: Pin 23 (digital input, pull-up)
- **LED Control**: Pin 12 (digital output)
- **Control Button**: Pin 16 (digital input, pull-up)

### PWM/Analog
- **DHT11 Sensor**: Pin 17 (temperature/humidity)
- **Servo Motor**: Pin 13 (PWM control)
- **Fan Motor**: Pins 19 (INA), 18 (INB) (PWM control)
- **RGB LEDs**: Pin 26 (NeoPixel/SK6812)

### Network
- **WiFi Connectivity**: ESP32 built-in
- **Internet Access**: HTTP requests
- **Signal Strength**: RSSI monitoring

## ESP32 Deployment Instructions

### 1. Prepare Development Environment

1. Install **Thonny IDE** (recommended for MicroPython)
2. Connect ESP32 to computer via USB cable
3. In Thonny: `Run > Select Interpreter > ESP32`

### 2. Upload Required Libraries

Upload these files to ESP32 root directory:

```python
# Core libraries (upload to ESP32)
i2c_lcd.py
lcd_api.py
```

### 3. Upload Test Files

Upload test files to ESP32:

```python
# Test files (upload to ESP32)
test_connections.py
test_wifi.py
run_all_tests.py
```

### 4. Configure WiFi Credentials

Before running WiFi tests, edit `test_wifi.py`:

```python
# Update these lines with your network details:
WIFI_SSID = 'Your_WiFi_Name'
WIFI_PASSWORD = 'Your_WiFi_Password'
```

### 5. Run Hardware Validation

#### Option A: Complete Test Suite
```python
# In Thonny, run:
exec(open('run_all_tests.py').read())
```

#### Option B: Individual Tests
```python
# Hardware components only:
exec(open('test_connections.py').read())

# WiFi connectivity only:
exec(open('test_wifi.py').read())
```

## Expected Output

### Successful Test Run
```
🏠 KS5009 SMART HOME HARDWARE VALIDATION SUITE
================================================================

💻 SYSTEM INFORMATION
Platform: ESP32
Available Memory: 105000 bytes

🔧 HARDWARE CONNECTION TESTS
✅ I2C devices detected at addresses: ['0x27', '0x28']
✅ All hardware tests passed!

📡 WIFI CONNECTIVITY TESTS
✅ Connected successfully!
✅ All WiFi tests passed!

🎯 SYSTEM READINESS: 🟢 READY FOR SOFTWARE IMPLEMENTATION
```

### Common Issues and Solutions

#### I2C Device Not Found
- Check SDA/SCL connections (pins 21/22)
- Verify 5V power supply to LCD/RFID
- Ensure pull-up resistors are connected

#### WiFi Connection Failed
- Verify SSID and password in `test_wifi.py`
- Check 2.4GHz network (ESP32 doesn't support 5GHz)
- Ensure network allows new device connections

#### Sensor Readings Invalid
- Check DHT11 connection to pin 17
- Verify 3.3V power supply
- Allow sensor warm-up time (2-3 seconds)

#### PWM Devices Not Responding
- Check servo connection to pin 13
- Verify PWM frequency (50Hz for servo)
- Ensure adequate power supply for motors

## Pin Configuration Summary

| Component | Pin(s) | Type | Notes |
|-----------|--------|------|-------|
| LCD Display | SDA:21, SCL:22 | I2C | Address 0x27 |
| RFID Reader | SDA:21, SCL:22 | I2C | Address 0x28 |
| DHT11 Sensor | 17 | Digital | Temperature/Humidity |
| PIR Motion | 14 | Digital Input | Motion detection |
| Gas Sensor | 23 | Digital Input | Pull-up enabled |
| LED Control | 12 | Digital Output | Status indicator |
| Control Button | 16 | Digital Input | Pull-up enabled |
| Servo Motor | 13 | PWM | 50Hz frequency |
| Fan Motor | 19,18 | PWM | INA/INB pins |
| RGB LEDs | 26 | NeoPixel | SK6812 compatible |

## Next Steps

After successful hardware validation:

1. ✅ **T002 Complete** - Hardware connections verified
2. 🔄 **T003** - Configure development environment
3. 🔄 **T004** - Additional hardware validation scripts
4. 🔄 **T005** - WiFi connectivity test refinement
5. 🔄 **Phase 3.2** - Begin contract tests (TDD approach)

## Troubleshooting

### Memory Issues
- Run `gc.collect()` between tests
- Upload only necessary files to ESP32
- Use `gc.mem_free()` to monitor memory

### Library Import Errors
- Install missing libraries via Thonny package manager
- Check file upload to ESP32 root directory
- Verify library compatibility with MicroPython

### Hardware Component Failures
- Review KS5009 kit documentation
- Check component wiring against reference code
- Test components individually before integration