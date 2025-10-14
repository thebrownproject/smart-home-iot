# ⚠️ CRITICAL ARCHITECTURE CHANGE - ESP32 Refactor Required

## What Changed

**OLD**: ESP32 → Supabase (HTTP/REST via `urequests`) for database writes
**NEW**: ESP32 → MQTT only → C# Middleware → Supabase

## Why

- **Memory Leak Fix**: MicroPython's `urequests` library causes memory fragmentation over time
- **Security**: ESP32 no longer has Supabase credentials—all database access controlled by C# middleware
- **Centralized Logic**: RFID validation and business rules now in single maintainable layer (C# API)

## What Needs Refactoring

### ✅ Already Works
- MQTT client (`esp32/comms/mqtt_client.py`) - just needs topic updates
- All sensor classes (DHT11, PIR, Gas, Steam, RFID)
- All output classes (LED, RGB, Servo, Fan, Buzzer)

### ❌ Needs Update
1. **Remove**: `esp32/comms/supabase.py` and `esp32/comms/supabase/` directory entirely
2. **Update**: All handlers to publish to MQTT instead of writing to Supabase
3. **Update**: RFID handler to use request/response pattern via MQTT
4. **Update**: `esp32/config.py` - remove Supabase credentials, add `DEVICE_ID = "esp32_main"`

## New MQTT Topic Structure

**ESP32 Publishes:**
```
devices/esp32_main/data         # All sensor readings (temp, humidity, motion, gas)
devices/esp32_main/rfid/check   # RFID UID for validation
devices/esp32_main/status/*     # Device status updates
```

**ESP32 Subscribes:**
```
devices/esp32_main/control/*        # Control commands from web
devices/esp32_main/rfid/response    # RFID validation result from C# middleware
```

## Sensor Data Payload Example

```json
{"sensor_type": "temperature", "value": 24.5, "unit": "C", "timestamp": "2025-10-14T10:30:00Z"}
{"sensor_type": "motion", "detected": true, "timestamp": "2025-10-14T10:30:05Z"}
```

## RFID Flow (Request/Response)

1. ESP32 scans card → Publish `devices/esp32_main/rfid/check` with `{"card_id": "abc123"}`
2. C# Middleware receives → Queries Supabase `authorised_cards` table
3. C# Middleware publishes `devices/esp32_main/rfid/response` with `{"card_id": "abc123", "valid": true, "authorised_card_id": 5}`
4. ESP32 receives response → Opens door (valid) or denies access (invalid)
5. C# Middleware logs scan to `rfid_scans` table

## Database Writes

**All database writes now handled by C# middleware:**
- Sensor data written every 30 minutes
- Motion events written immediately
- Gas alerts written immediately
- RFID scans logged by middleware after validation

## Implementation Priority

1. Update `esp32/config.py` (remove Supabase, add DEVICE_ID)
2. Remove `esp32/comms/supabase.py` and subdirectory
3. Update `esp32/comms/mqtt_client.py` to subscribe to `devices/esp32_main/rfid/response`
4. Refactor `handlers/rfid_handler.py` for MQTT request/response pattern
5. Update all other handlers to publish sensor data to `devices/esp32_main/data`

## Reference

See `planning/architecture.md` for complete MQTT topic structure and payload examples.
See `planning/tasks.md` for detailed refactoring tasks (T1.17, T1.18, T1.23, T1.25).
