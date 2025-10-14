# System Architecture

## Data Flow Diagram

### Full System
```
                    ┌──────────────┐
                    │    ESP32     │  (MicroPython)
                    │              │
                    │  • DHT11     │
                    │  • PIR       │
                    │  • Gas       │
                    │  • RFID      │
                    │  • Steam     │
                    └──────┬───────┘
                           │
                           │  MQTT ONLY
                           │  (Publish sensor data)
                           │  (Subscribe to validation responses)
                           │
                           ↓
                    ┌─────────────┐
                    │   HiveMQ    │
                    │   Broker    │
                    │             │
                    │ (SSL/TLS)   │
                    └──┬──────┬───┘
                       │      │
              ┌────────┘      └────────┐
              ↓                        ↓
       ┌─────────────┐          ┌─────────────┐
       │  Next.js    │          │  C# API     │
       │  Web App    │          │ Middleware  │
       │             │          │             │
       │ • Subscribe │          │ • Subscribe │
       │   to MQTT   │          │   to MQTT   │
       │ • Display   │          │ • Validate  │
       │   Live Data │          │   RFID      │
       └──────┬──────┘          │ • Write to  │
              │                 │   Supabase  │
              │                 └──────┬──────┘
              │                        │
              │                        │  HTTPS
              │     GET (Historical)   │  (All DB Access)
              │  ◄─────────────────────┤
              │                        ↓
              │                 ┌─────────────┐
              └─────────────────┤  Supabase   │
                                │  Database   │
                                │             │
                                │ (Storage)   │
                                └─────────────┘
```

## Message Flow Patterns

### Pattern 1: Sensor Data → Database (Persistence)
```
ESP32 reads DHT11
    ↓
Publish MQTT: devices/esp32_main/data
    {"sensor_type": "temperature", "value": 24.5, "unit": "C", "timestamp": "2025-10-14T10:30:00Z"}
    ↓
C# Middleware subscribes to devices/+/data
    ↓
C# validates and transforms payload
    ↓
POST https://supabase.com/rest/v1/sensor_logs (from C# only)
    {"device_id": 1, "sensor_type": "temperature", "value": 24.5, "unit": "C"}
    ↓
Done ✓
```

### Pattern 2: Real-time Dashboard Update
```
ESP32 reads sensor
    ↓
Publish MQTT: devices/esp32_main/data {"sensor_type": "temperature", "value": 24.5}
    ↓
Next.js subscribes to devices/+/data → Updates UI instantly (< 1 second)
C# Middleware also receives (for logging)
```

### Pattern 3: Web Reads Historical Data
```
Next.js needs to show "Temperature (Last 24 Hours)"
    ↓
GET /api/sensors/temperature?hours=24
    ↓
C# API queries Supabase
    ↓
Returns JSON to Next.js
    ↓
Chart displays data
```

### Pattern 4: RFID Validation Flow (NEW)
```
ESP32 scans RFID card (UID: "abc123")
    ↓
Publish MQTT: devices/esp32_main/rfid/check {"card_id": "abc123"}
    ↓
C# Middleware subscribes to devices/+/rfid/check
    ↓
C# queries Supabase: SELECT * FROM authorised_cards WHERE card_id='abc123' AND is_active=true
    ↓
C# publishes validation result: devices/esp32_main/rfid/response {"card_id": "abc123", "valid": true, "authorised_card_id": 5}
    ↓
ESP32 subscribes to devices/esp32_main/rfid/response
    ↓
If valid: Open door servo, green LED
If invalid: Red LED + buzzer
    ↓
C# logs scan to database: INSERT INTO rfid_scans (card_id, access_result, authorised_card_id)
```

### Pattern 5: Web Control → Output
```
User clicks "Open Door" (Next.js)
    ↓
Publish MQTT: devices/esp32_main/control/door {"action": "open"}
    ↓
ESP32 subscribes → Activates servo
    ↓
ESP32 publishes: devices/esp32_main/status/door {"state": "open"}
    ↓
Next.js updates UI
```

## REST API Endpoints (C# .NET)

### Sensors Controller
```
GET  /api/sensors/current
     → Returns latest temperature and humidity reading
     Response: { "temperature": 24.5, "humidity": 65, "timestamp": "..." }

GET  /api/sensors/history?hours=24&type=temperature
     → Returns historical sensor readings
     Query params: hours (default 24), type (temperature|humidity|all)
     Response: [{ "value": 24.5, "unit": "C", "timestamp": "..." }, ...]
```

### RFID Controller
```
GET  /api/rfid/scans
     → Returns all RFID scans
     Response: [{ "cardId": "abc123", "success": true, "userName": "John", "timestamp": "..." }, ...]

GET  /api/rfid/scans?status=failed
     → Filters by success/failed
     Query params: status (success|failed|all)
     Response: [{ "cardId": "unknown", "success": false, "timestamp": "..." }, ...]
```

### Motion Controller
```
GET  /api/motion/recent?hours=1
     → Returns motion events in last N hours (default 1)
     Response: { "count": 15, "events": [{ "timestamp": "..." }, ...] }
```

### Gas Controller
```
GET  /api/gas/alerts
     → Returns gas detection events
     Response: [{ "sensorValue": 850, "alertStart": "...", "alertEnd": "...", "fanActivated": true }, ...]
```

### Status Controller
```
GET  /api/status
     → Returns current status of all devices
     Response: {
       "door": "open",
       "window": "closed",
       "fan": "off",
       "led": "on",
       "lastUpdate": "..."
     }
```

### Control Controller (Optional - Alternative to MQTT)
```
POST /api/control
     Body: { "device": "door", "action": "open" }
     → Publishes to MQTT control topic
     Response: { "success": true, "message": "Command sent" }

     Supported devices: door, window, fan, led
     Supported actions: open, close, on, off
```

**Note**: Control commands are primarily via MQTT (Next.js → MQTT → ESP32). The Control API is optional for scenarios where MQTT isn't available.

## MQTT Topics

### Topic Structure
All topics follow the pattern: `devices/{deviceId}/{category}/{subcategory}`

**Device ID**: `esp32_main` (single device for Phase 1, scalable to multiple devices)

### ESP32 Publishes (Device → Cloud)
```
devices/esp32_main/data                # All sensor readings (DHT11, PIR, gas, steam)
devices/esp32_main/rfid/check          # RFID UID for validation
devices/esp32_main/status/door         # Door servo position
devices/esp32_main/status/window       # Window servo position
devices/esp32_main/status/fan          # Fan state (on/off)
devices/esp32_main/status/led          # LED state
```

**Payload Examples**:
```json
// devices/esp32_main/data
{"sensor_type": "temperature", "value": 24.5, "unit": "C", "timestamp": "2025-10-14T10:30:00Z"}
{"sensor_type": "humidity", "value": 65, "unit": "%", "timestamp": "2025-10-14T10:30:00Z"}
{"sensor_type": "motion", "detected": true, "timestamp": "2025-10-14T10:30:05Z"}
{"sensor_type": "gas", "detected": true, "value": 850, "timestamp": "2025-10-14T10:30:10Z"}

// devices/esp32_main/rfid/check
{"card_id": "abc123", "timestamp": "2025-10-14T10:30:15Z"}

// devices/esp32_main/status/door
{"state": "open", "timestamp": "2025-10-14T10:30:20Z"}
```

### ESP32 Subscribes (Cloud → Device)
```
devices/esp32_main/control/door        # Open/close door
devices/esp32_main/control/window      # Open/close window
devices/esp32_main/control/fan         # Turn on/off fan
devices/esp32_main/control/led         # LED control
devices/esp32_main/rfid/response       # RFID validation result from C# middleware
```

**Payload Examples**:
```json
// devices/esp32_main/control/door
{"action": "open"}
{"action": "close"}

// devices/esp32_main/rfid/response
{"card_id": "abc123", "valid": true, "authorised_card_id": 5}
{"card_id": "xyz789", "valid": false}
```

### C# Middleware Subscribes (Device → Middleware)
```
devices/+/data                         # All device sensor data (wildcard for multiple devices)
devices/+/rfid/check                   # RFID validation requests
devices/+/status/#                     # All device status updates
```

### C# Middleware Publishes (Middleware → Device)
```
devices/{deviceId}/rfid/response       # RFID validation results
```

**Tech Stack**: See `planning/prd.md` for complete technology details
**Database Schema**: See `planning/database-schema.sql` for full table definitions

## Key Decisions

### ✅ MQTT-Only Communication for ESP32 (NO HTTP/REST)
- **Why**: MicroPython's `urequests` library has memory leaks—persistent MQTT connection is more stable
- **How**: ESP32 maintains single MQTT connection, publishes all data to broker
- **Security**: ESP32 has no Supabase credentials—all database access controlled by C# middleware

### ✅ C# Middleware as Single Database Gateway
- **Requirement**: "C# API must be used if API layer is created separately to Web App"
- **Purpose**:
  - Subscribe to MQTT device messages
  - Validate RFID cards against Supabase
  - Write all sensor data to Supabase
  - Provide REST endpoints for historical queries
- **Benefits**: Centralized business logic, secure credential management, easy to add validation rules

### ✅ MQTT for Both Real-Time AND Persistence
- **ESP32 publishes**: All sensor readings to `devices/{id}/data` topic
- **C# Middleware subscribes**: Receives messages, writes to Supabase every 30 minutes (or on critical events)
- **Next.js subscribes**: Updates dashboard instantly with same MQTT messages
- **Result**: Single publish event serves dual purpose (real-time + persistence)

### ✅ Request/Response Pattern for RFID Validation
- **ESP32 publishes**: UID to `devices/{id}/rfid/check`
- **C# Middleware**: Queries database, publishes result to `devices/{id}/rfid/response`
- **ESP32 subscribes**: Waits for validation response, then acts (open door or deny)
- **Why**: Keeps authorised card list in database only, no hardcoded UIDs on device

### ✅ Web control via MQTT (direct to device)
- **Pattern**: Next.js publishes directly to `devices/{id}/control/*` topics
- **ESP32 subscribes**: Receives commands, activates outputs
- **Why**: Lower latency, no backend needed for simple commands

### ✅ Event Priority (State Machine)
```
GAS_ALERT (priority 3)      → Fan on, RGB red
    ↓ (if no gas)
STEAM_DETECTED (priority 2)  → Window close, RGB blue flash
    ↓ (if no steam)
MOTION_DETECTED (priority 1) → RGB orange
    ↓ (if no motion)
IDLE (priority 0)
```

## Development Phases

### Phase 1: Embedded Core
1. Build ESP32 sensor modules (DHT11, PIR, Gas, RFID, Steam)
2. ESP32 → Supabase (HTTP POST for data logging)
3. ESP32 → MQTT (publish sensor events)
4. ESP32 ← MQTT (subscribe to control commands)
5. Test: Sensor → DB + MQTT publish working

### Phase 2: C# API Layer
1. Setup C# API project (ASP.NET Core 9.0)
2. Configure Supabase client with dependency injection
3. **Implement MQTT Background Service** (MQTTnet library)
   - Subscribe to `devices/+/data` for sensor readings
   - Subscribe to `devices/+/rfid/check` for RFID validation
   - Write sensor data to Supabase every 30 minutes
4. **Implement RFID Validation Service**
   - Query `authorised_cards` table
   - Publish validation result to `devices/{id}/rfid/response`
   - Log scan to `rfid_scans` table
5. Create Models mapping to database tables
6. Build Controllers with GET endpoints (query Supabase for historical data)
7. Add CORS for Next.js frontend
8. Enable Swagger for API documentation
9. Test MQTT subscription and database writes
10. Test REST endpoints with Postman/Swagger UI

### Phase 3: Web Dashboard
1. Build Next.js dashboard with MQTT client
2. Create API client wrapper (axios) for C# backend
3. Next.js → C# API (fetch historical data)
4. Next.js → MQTT (subscribe for real-time, publish for control)
5. Test: Full loop (ESP32 → DB/MQTT → API → Next.js)

### Phase 4: Bonus Features
1. User authentication (Supabase Auth)
2. User roles (Parent/Child) in C# API
3. PIR arm/disarm system
4. Advanced analytics (avg temp per day)

---

## Related Documentation

- **Functional requirements**: `planning/prd.md`
- **File structure**: `planning/file-structure.md`
- **Database schema**: `planning/database-schema.sql`
- **Environment setup**: `planning/environment-setup.md`
