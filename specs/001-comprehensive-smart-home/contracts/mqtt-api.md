# MQTT API Contract: Smart Home Automation System

**Branch**: `001-comprehensive-smart-home` | **Date**: 2025-09-17
**Protocol**: MQTT via HiveMQ Cloud Broker

## Topic Structure

### Base Topics
```
smarthome/{device_id}/{category}/{action}
```

Where:
- `device_id`: ESP32 unique identifier (MAC address based)
- `category`: Data type ("environmental", "security", "access", "emergency", "system")
- `action`: Operation ("data", "alert", "status", "command")

## Published Topics (ESP32 → Cloud)

### Environmental Data
**Topic**: `smarthome/{device_id}/environmental/data`
**QoS**: 1 (at least once delivery)
**Retention**: false
**Frequency**: Every 30 seconds

```json
{
  "timestamp": "2025-09-17T10:30:00Z",
  "sensor_type": "temperature",
  "value": 23.5,
  "unit": "celsius",
  "location": "indoor",
  "status": "normal"
}
```

**Validation Schema**:
```json
{
  "type": "object",
  "required": ["timestamp", "sensor_type", "value", "unit"],
  "properties": {
    "timestamp": {"type": "string", "format": "date-time"},
    "sensor_type": {"enum": ["temperature", "humidity", "gas"]},
    "value": {"type": "number"},
    "unit": {"enum": ["celsius", "percent", "ppm"]},
    "location": {"type": "string", "maxLength": 50},
    "status": {"enum": ["normal", "warning", "critical"]}
  }
}
```

### Security Events
**Topic**: `smarthome/{device_id}/security/alert`
**QoS**: 2 (exactly once delivery)
**Retention**: false
**Frequency**: Event-driven

```json
{
  "timestamp": "2025-09-17T10:30:00Z",
  "event_type": "motion",
  "severity": "info",
  "triggered_by": "motion_sensor_pin14",
  "response_actions": ["led_on", "fan_start"],
  "location": "living_room"
}
```

### Access Control
**Topic**: `smarthome/{device_id}/access/data`
**QoS**: 2 (exactly once delivery)
**Retention**: false
**Frequency**: Event-driven

```json
{
  "timestamp": "2025-09-17T10:30:00Z",
  "card_uid": "A1B2C3D4",
  "access_granted": true,
  "door_action": "unlock",
  "user_name": "John Doe",
  "location": "main_door"
}
```

### Emergency Alerts
**Topic**: `smarthome/{device_id}/emergency/alert`
**QoS**: 2 (exactly once delivery)
**Retention**: true (last known state)
**Frequency**: Event-driven

```json
{
  "timestamp": "2025-09-17T10:30:00Z",
  "emergency_type": "gas_detected",
  "severity_level": 5,
  "triggered_by": "gas_sensor_pin23",
  "response_sequence": ["open_doors", "open_windows", "activate_fan", "sound_alarm"],
  "manual_disable": false
}
```

### System Status
**Topic**: `smarthome/{device_id}/system/status`
**QoS**: 1 (at least once delivery)
**Retention**: true (last known state)
**Frequency**: Every 60 seconds + on state change

```json
{
  "timestamp": "2025-09-17T10:30:00Z",
  "pir_enabled": true,
  "gas_alarm_active": false,
  "manual_overrides": {
    "gas_alarm": false,
    "pir_system": false
  },
  "device_status": {
    "temperature_sensor": "online",
    "motion_sensor": "online",
    "rfid_reader": "online",
    "gas_sensor": "online",
    "oled_display": "online"
  },
  "network_status": "connected",
  "uptime_seconds": 3600,
  "memory_free_bytes": 45000
}
```

## Subscribed Topics (Cloud → ESP32)

### System Commands
**Topic**: `smarthome/{device_id}/system/command`
**QoS**: 2 (exactly once delivery)

```json
{
  "command": "toggle_pir",
  "timestamp": "2025-09-17T10:30:00Z",
  "parameters": {}
}
```

**Supported Commands**:
- `toggle_pir`: Enable/disable PIR security system
- `disable_gas_alarm`: Temporarily disable gas alarm (same as button 1)
- `test_emergency`: Trigger emergency test sequence
- `reboot_system`: Restart ESP32 device
- `update_config`: Update system configuration parameters

### Configuration Updates
**Topic**: `smarthome/{device_id}/config/update`
**QoS**: 2 (exactly once delivery)

```json
{
  "config_type": "thresholds",
  "timestamp": "2025-09-17T10:30:00Z",
  "parameters": {
    "temperature_threshold": 25.0,
    "gas_threshold": 500,
    "motion_timeout_seconds": 300
  }
}
```

## MQTT Connection Parameters

### HiveMQ Cloud Configuration
```python
MQTT_CONFIG = {
    "server": "your-cluster.hivemq.cloud",
    "port": 8883,  # TLS encrypted
    "username": "esp32_device",
    "password": "[ENV_VARIABLE]",
    "client_id": f"smarthome_{device_id}",
    "keepalive": 60,
    "ssl": True,
    "ssl_params": {
        "cert_reqs": 1,  # ssl.CERT_REQUIRED
        "ca_certs": None  # Use default CA bundle
    }
}
```

### Connection Management
```python
RETRY_CONFIG = {
    "max_retries": 5,
    "backoff_base": 2,  # Exponential backoff
    "max_backoff": 300,  # 5 minutes max
    "connection_timeout": 10
}
```

## Message Flow Examples

### Normal Temperature Reading
```
1. ESP32 reads DHT11 sensor: 24.5°C
2. Publish to: smarthome/ESP32_ABC123/environmental/data
3. Cloud service receives and stores in database
4. Dashboard updates real-time display
```

### Gas Emergency Sequence
```
1. Gas sensor detects dangerous level
2. ESP32 immediately executes local emergency protocol
3. Publish emergency alert to: smarthome/ESP32_ABC123/emergency/alert
4. Cloud service receives alert and triggers notifications
5. Emergency responders notified via webhook/email
6. User presses button 1 to disable alarm
7. Publish status update with manual_disable: true
```

### Remote PIR Toggle
```
1. User toggles PIR via mobile app/dashboard
2. Cloud service publishes to: smarthome/ESP32_ABC123/system/command
3. ESP32 receives command and toggles PIR state
4. ESP32 publishes updated status to: smarthome/ESP32_ABC123/system/status
5. Dashboard reflects new PIR state
```

## Error Handling

### Connection Failures
- Local operation continues during network outages
- Messages queued locally with circular buffer (size limits per topic)
- Automatic reconnection with exponential backoff
- Critical emergency messages prioritized on reconnection

### Message Validation
- All incoming messages validated against JSON schema
- Invalid messages logged and discarded
- Malformed timestamps default to current device time
- Missing required fields trigger error response

### Quality of Service
- QoS 0: Environmental data (acceptable loss)
- QoS 1: System status (at least once delivery)
- QoS 2: Security/Emergency/Access (exactly once delivery)

## Security Considerations

### Authentication
- Username/password authentication for MQTT broker
- Device-specific credentials (not shared between devices)
- Credential rotation capability via configuration update

### Encryption
- TLS 1.2+ for all MQTT communications
- Certificate validation against CA bundle
- No plain text credentials in source code

### Authorization
- Device can only publish to own topics (enforced by broker ACLs)
- Read-only access to configuration topics
- Command topics restricted to authorized clients