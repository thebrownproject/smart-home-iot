# Quickstart Guide: Smart Home Automation System

**Branch**: `001-comprehensive-smart-home` | **Date**: 2025-09-17
**Purpose**: Rapid deployment and validation testing

## Prerequisites

### Hardware Requirements
- KS5009 Smart Home Kit components assembled
- ESP32 microcontroller flashed with MicroPython 1.20+
- USB cable for initial programming and testing
- WiFi network with internet access
- Computer with Thonny IDE installed

### Cloud Services Setup
- Supabase account with PostgreSQL database
- HiveMQ Cloud broker account (free tier sufficient)
- Database tables created (see data-model.md for schema)

### Development Environment
- Thonny IDE with ESP32 support
- Git repository initialized with spec-kit structure
- Python 3.8+ for development tools and testing

## 5-Minute Quick Start

### Step 1: Clone and Setup (2 minutes)
```bash
# Clone the repository
git clone <repository-url>
cd SmartHomeProject

# Switch to feature branch
git checkout 001-comprehensive-smart-home

# Verify spec-kit structure
ls .specify/
ls specs/001-comprehensive-smart-home/
```

### Step 2: Hardware Connection Verification (2 minutes)
```python
# Upload to ESP32 via Thonny and run
from machine import Pin, SoftI2C
import time

# Quick hardware test
print("Testing hardware connections...")

# Test OLED (I2C)
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)
devices = i2c.scan()
print(f"I2C devices found: {[hex(addr) for addr in devices]}")

# Test sensors
motion_sensor = Pin(14, Pin.IN)
gas_sensor = Pin(23, Pin.IN, Pin.PULL_UP)
led = Pin(12, Pin.OUT)

print(f"Motion sensor: {motion_sensor.value()}")
print(f"Gas sensor: {gas_sensor.value()}")

# Test LED
led.on()
time.sleep(0.5)
led.off()
print("LED test complete")

print("Hardware verification complete!")
```

### Step 3: Basic System Test (1 minute)
```python
# Minimal system test
from dht import DHT11
from machine import Pin

# Test temperature sensor
dht = DHT11(Pin(17))
dht.measure()
print(f"Temperature: {dht.temperature()}°C")
print(f"Humidity: {dht.humidity()}%")

print("Basic system test complete!")
```

## User Story Validation Tests

### Test 1: Environmental Monitoring
**User Story**: Temperature display and window control
**Expected Result**: OLED shows current temperature, window opens when threshold exceeded

```python
# Test script: test_environmental.py
def test_temperature_display():
    """Verify continuous temperature display on OLED"""
    # Initialize OLED and DHT11
    # Read temperature every 5 seconds
    # Verify OLED updates with current reading
    pass

def test_window_control():
    """Verify automatic window opening at temperature threshold"""
    # Set temperature threshold to 25°C
    # Heat DHT11 sensor above threshold
    # Verify servo motor opens window
    # Verify OLED displays cooling message
    pass
```

**Manual Validation Steps**:
1. Power on system, verify OLED displays temperature
2. Breathe on DHT11 sensor to increase temperature
3. Confirm window servo activates when threshold exceeded
4. Verify OLED shows "Cooling..." message

### Test 2: Motion Detection and Response
**User Story**: Motion activates lights and fan with welcome message
**Expected Result**: LED turns on, fan starts, OLED shows welcome

```python
def test_motion_response():
    """Verify motion detection triggers correct responses"""
    # Initialize motion sensor on pin 14
    # Simulate motion detection
    # Verify LED activation
    # Verify fan activation
    # Verify OLED welcome message
    pass
```

**Manual Validation Steps**:
1. Wave hand in front of motion sensor
2. Confirm LED turns on immediately
3. Confirm fan starts running
4. Verify OLED displays "Welcome!" message

### Test 3: PIR Security System
**User Story**: PIR motion triggers security alert with buzzer and RGB
**Expected Result**: Buzzer sounds, RGB cycles through colors

```python
def test_pir_security():
    """Verify PIR security system functionality"""
    # Initialize PIR sensor
    # Enable security system
    # Trigger PIR motion detection
    # Verify buzzer activation
    # Verify RGB color cycling
    pass
```

**Manual Validation Steps**:
1. Ensure PIR system is enabled (default state)
2. Move in front of PIR sensor
3. Confirm buzzer sounds alert
4. Verify RGB LEDs cycle through all colors

### Test 4: RFID Access Control
**User Story**: Authorized RFID card unlocks door with status display
**Expected Result**: Door unlocks, LED shows access granted

```python
def test_rfid_access():
    """Verify RFID access control functionality"""
    # Initialize RFID reader
    # Present authorized card
    # Verify door servo unlock
    # Verify LED status indication
    # Verify OLED access granted message
    pass
```

**Manual Validation Steps**:
1. Present provided RFID card to reader
2. Confirm door servo unlocks
3. Verify LED shows green/success status
4. Check OLED displays "Access Granted" message

### Test 5: Gas Emergency Protocol
**User Story**: Gas detection triggers comprehensive emergency response
**Expected Result**: All safety measures activate (doors, windows, fan, alarms)

```python
def test_gas_emergency():
    """Verify gas emergency response protocol"""
    # Initialize gas sensor
    # Simulate gas detection
    # Verify all emergency responses:
    #   - All doors open (servo)
    #   - All windows open (servo)
    #   - Fan activates
    #   - RGB flashes warning
    #   - Buzzer sounds alarm
    pass
```

**Manual Validation Steps**:
1. Cover gas sensor or use test gas to trigger
2. Confirm all doors/windows open automatically
3. Verify fan activates for ventilation
4. Check RGB LEDs flash warning pattern
5. Confirm buzzer sounds emergency alarm

### Test 6: Manual Override Controls
**User Story**: Button controls allow manual system overrides
**Expected Result**: Button 1 disables gas alarm, Button 2 toggles PIR

```python
def test_manual_overrides():
    """Verify manual button override functionality"""
    # Test gas alarm disable (Button 1)
    # Test PIR system toggle (Button 2)
    # Verify system state changes
    # Verify OLED status updates
    pass
```

**Manual Validation Steps**:
1. Trigger gas alarm, then press Button 1
2. Confirm gas alarm disables
3. Press Button 2, verify PIR system toggles
4. Check OLED displays current system status

### Test 7: WiFi and MQTT Connectivity
**User Story**: System connects to internet and transmits data
**Expected Result**: WiFi connection established, MQTT messages sent

```python
def test_connectivity():
    """Verify network connectivity and data transmission"""
    # Test WiFi connection
    # Test MQTT broker connection
    # Send test environmental data
    # Send test security event
    # Verify cloud database storage
    pass
```

**Manual Validation Steps**:
1. Configure WiFi credentials
2. Verify ESP32 connects to network
3. Check MQTT broker receives messages
4. Confirm data appears in Supabase database

### Test 8: Database Integration
**User Story**: RFID access and sensor data stored in cloud database
**Expected Result**: All events recorded with timestamps

```python
def test_database_integration():
    """Verify cloud database integration"""
    # Generate access events
    # Generate sensor readings
    # Verify API calls succeed
    # Verify data persistence
    # Test offline caching
    pass
```

**Manual Validation Steps**:
1. Use RFID card multiple times
2. Let system run for 10 minutes
3. Check Supabase dashboard for:
   - Access records with timestamps
   - Environmental readings
   - Security events

## Integration Testing

### Full System Test Sequence
**Duration**: 15 minutes
**Purpose**: Validate all features working together

```python
def full_system_integration_test():
    """Complete system integration test"""
    print("Starting full system integration test...")

    # 1. System startup and hardware initialization
    test_hardware_initialization()

    # 2. Network connectivity
    test_network_connection()

    # 3. All sensor readings
    test_all_sensors()

    # 4. All actuator responses
    test_all_actuators()

    # 5. Emergency scenarios
    test_emergency_scenarios()

    # 6. Manual overrides
    test_manual_controls()

    # 7. Data persistence
    test_data_storage()

    print("Full system integration test complete!")
```

### Performance Validation
```python
def performance_validation():
    """Verify system meets performance requirements"""
    # Sensor response time < 100ms
    # OLED refresh rate 1Hz
    # MQTT transmission < 1s
    # Memory usage < 80% of available
    # Network reconnection < 30s
    pass
```

## Troubleshooting Quick Reference

### Common Issues and Solutions

#### Hardware Connection Problems
```python
# Debug I2C devices
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)
print("I2C scan:", [hex(addr) for addr in i2c.scan()])
# Expected: ['0x27'] for OLED, ['0x28'] for RFID if connected
```

#### WiFi Connection Issues
```python
import network
wlan = network.WLAN(network.STA_IF)
print("WiFi status:", wlan.status())
print("WiFi config:", wlan.ifconfig())
# Status should be 3 (connected)
```

#### MQTT Connection Problems
```python
# Test MQTT broker connectivity
import socket
try:
    s = socket.socket()
    s.connect(('your-broker.hivemq.cloud', 8883))
    print("MQTT broker reachable")
    s.close()
except:
    print("MQTT broker connection failed")
```

#### Sensor Reading Errors
```python
# DHT11 troubleshooting
try:
    dht.measure()
    print(f"Temp: {dht.temperature()}°C, Humidity: {dht.humidity()}%")
except OSError as e:
    print(f"DHT11 error: {e}")
    # Common: timeout errors, check wiring
```

### System Status Commands
```python
def system_diagnostic():
    """Complete system diagnostic report"""
    print("=== System Diagnostic Report ===")
    print(f"Uptime: {time.ticks_ms() // 1000} seconds")
    print(f"Free memory: {gc.mem_free()} bytes")
    print(f"WiFi status: {wlan.status()}")
    print(f"I2C devices: {i2c.scan()}")
    print("=== End Report ===")
```

## Next Steps

After successful quickstart validation:

1. **Review Implementation Tasks**: Run `/tasks` command to generate detailed implementation tasks
2. **Set Up Development Environment**: Configure Thonny IDE with project structure
3. **Begin Component Development**: Start with sensor abstraction classes
4. **Implement Core Logic**: Build automation engine and state management
5. **Add Network Features**: Integrate MQTT and database connectivity
6. **Complete Integration Testing**: Validate all user stories and edge cases

## Success Criteria Checklist

- [ ] All hardware components respond correctly
- [ ] Environmental monitoring displays on OLED
- [ ] Motion detection triggers appropriate responses
- [ ] PIR security system functions with alerts
- [ ] RFID access control operates correctly
- [ ] Gas emergency protocol activates all safety measures
- [ ] Manual button overrides work as specified
- [ ] WiFi connectivity established successfully
- [ ] MQTT messages transmitted to cloud broker
- [ ] Database integration stores all event types
- [ ] System operates reliably for 30+ minutes
- [ ] All user stories validated manually
- [ ] Performance requirements met
- [ ] Error handling gracefully manages failures

**System Ready**: When all checklist items completed, proceed to full implementation phase.