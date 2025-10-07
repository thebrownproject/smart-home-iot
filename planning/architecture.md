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
                    └──┬────────┬──┘
                       │        │
              MQTT     │        │  HTTPS (Direct)
              (Live)   │        │  (Persistence)
                       │        │
                       ↓        ↓
            ┌─────────────┐  ┌─────────────┐
            │   HiveMQ    │  │  Supabase   │
            │   Broker    │  │  Database   │
            │             │  │             │
            │ (Real-time) │  │ (Storage)   │
            └──────┬──────┘  └──────▲──────┘
                   │                │
                   │                │
                   ↓                │
            ┌─────────────┐         │
            │  Next.js    │         │
            │  Web App    │         │
            │             │         │
            │ • Subscribe │         │
            │   to MQTT   │    GET  │
            │ • Call C#   │─────────┤
            │   API       │         │
            └─────────────┘         │
                                    │
                             ┌──────┴──────┐
                             │   C# API    │
                             │             │
                             │ • REST GET  │
                             │   endpoints │
                             │ • Query DB  │
                             └─────────────┘
```

## Message Flow Patterns

### Pattern 1: Sensor Data → Database (Persistence)
```
ESP32 reads DHT11
    ↓
POST https://supabase.com/rest/v1/sensor_logs
    {"sensor_type": "temperature", "value": 24.5, "unit": "C"}
    ↓
Supabase stores data
    ↓
Done ✓
```

### Pattern 2: Real-time Dashboard Update
```
ESP32 reads sensor
    ↓
Publish MQTT: home/temperature {"value": 24.5}
    ↓
Next.js subscribes → Updates UI instantly (< 1 second)
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

### Pattern 4: Web Control → Actuator
```
User clicks "Open Door" (Next.js)
    ↓
Publish MQTT: home/control/door {"action": "open"}
    ↓
ESP32 subscribes → Activates servo
    ↓
ESP32 publishes: home/status/door {"state": "open"}
    ↓
Next.js updates UI
```

## MQTT Topics

### ESP32 Publishes (Sensors → Cloud)
```
home/temperature          # DHT11
home/humidity            # DHT11
home/motion              # PIR
home/gas                 # Gas sensor
home/steam               # Steam/moisture
home/rfid                # RFID scans
home/status/door         # Servo position
home/status/window       # Servo position
home/status/fan          # Fan state
```

### ESP32 Subscribes (Cloud → Actuators)
```
home/control/door        # Open/close door
home/control/window      # Open/close window
home/control/fan         # Turn on/off fan
home/control/led         # LED control
```

## Tech Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Embedded** | MicroPython on ESP32 | Read sensors, control actuators, MQTT pub/sub |
| **MQTT Broker** | HiveMQ Cloud | Message routing (ESP32 ↔ Cloud) |
| **Backend API** | C# ASP.NET Core 8 | MQTT subscriber, data validation, REST endpoints |
| **Database** | Supabase PostgreSQL | Persistent storage |
| **Frontend** | Next.js 15 + TypeScript | Dashboard UI, API calls, MQTT subscription |

## Database Schema (Simple)

```sql
-- Sensor readings
sensor_logs (id, sensor_type, value, unit, timestamp)

-- RFID access
rfid_scans (id, card_id, access_result, timestamp, user_name)

-- Motion events
motion_events (id, detected, timestamp)

-- Gas alerts
gas_alerts (id, sensor_value, alert_start, alert_end, fan_activated)
```

## Key Decisions

### ✅ ESP32 writes directly to Supabase (not through C# API)
- **Why**: Simpler - ESP32 is the source of data, should own persistence
- **How**: HTTP POST using MicroPython's `urequests` library
- **Security**: Supabase anon key stored in ESP32 config (gitignored)

### ✅ C# API only for reads (Next.js → C# → Supabase)
- **Requirement**: "C# API must be used if API layer is created separately to Web App"
- **Purpose**: Query historical data, apply filters, format responses
- **Example**: `GET /api/sensors/temperature?hours=24`

### ✅ MQTT for real-time updates only
- **ESP32 publishes**: Sensor readings to MQTT topics
- **Next.js subscribes**: Updates dashboard instantly
- **No persistence in MQTT**: Messages are ephemeral (live updates only)

### ✅ Web control via MQTT (not C# API)
- **Pattern**: Next.js publishes directly to MQTT control topics
- **ESP32 subscribes**: Receives commands, activates actuators
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

### Phase 2: C# API + Web Dashboard
1. Setup C# API project (ASP.NET Core 8)
2. Create GET endpoints (query Supabase for historical data)
3. Build Next.js dashboard
4. Next.js → C# API (fetch historical data)
5. Next.js → MQTT (subscribe for real-time, publish for control)
6. Test: Full loop (ESP32 → DB/MQTT → Next.js)

### Phase 3: Bonus Features
1. User authentication (Supabase Auth)
2. User roles (Parent/Child) in C# API
3. PIR arm/disarm system
4. Advanced analytics (avg temp per day)

## File Structure

```
SmartHomeProject/
├── api/                   # C# ASP.NET Core
│   └── SmartHomeApi/
│       ├── Controllers/
│       ├── Services/
│       └── Models/
│
├── embedded/              # ESP32 MicroPython
│   ├── main.py
│   ├── sensors/
│   ├── actuators/
│   └── network/
│
├── web/                   # Next.js
│   └── app/
│
└── planning/              # This folder
    ├── prd.md
    ├── tasks.md
    ├── architecture.md    # This file
    └── development-notes.md
```
