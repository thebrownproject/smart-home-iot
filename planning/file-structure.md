# Project File Structure

```
SmartHomeProject/
├── embedded/                    # ESP32 MicroPython code
│   ├── main.py                 # Entry point, main loop
│   ├── boot.py                 # Network setup, runs on startup
│   ├── config.py               # WiFi, MQTT, Supabase credentials
│   ├── sensors/
│   │   ├── dht11.py           # Temperature/humidity sensor
│   │   ├── pir.py             # Motion detection
│   │   ├── gas.py             # Gas/flame sensor
│   │   ├── steam.py           # Moisture sensor
│   │   └── rfid.py            # RFID reader (RC522)
│   ├── actuators/
│   │   ├── led.py             # Simple LED control
│   │   ├── rgb.py             # SK6812 RGB LED strip
│   │   ├── servo.py           # Servo motor (door/window)
│   │   ├── fan.py             # Fan control
│   │   └── buzzer.py          # Buzzer alerts
│   ├── display/
│   │   └── oled.py            # OLED display (SSD1306)
│   ├── network/
│   │   ├── mqtt_client.py     # MQTT pub/sub handler
│   │   └── supabase.py        # Supabase HTTP client
│   └── utils/
│       ├── time_sync.py       # NTP time synchronization
│       └── logger.py          # Debug logging utility
│
├── api/                        # C# .NET Web API (Phase 2)
│   ├── SmartHomeApi.sln       # Solution file
│   ├── SmartHomeApi/
│   │   ├── SmartHomeApi.csproj    # Project file (.NET 9.0)
│   │   ├── Program.cs             # API entry point, DI configuration
│   │   ├── appsettings.json       # Supabase URL/key, MQTT config
│   │   ├── appsettings.Development.json  # Dev overrides
│   │   ├── Controllers/
│   │   │   ├── SensorsController.cs   # GET current/history readings
│   │   │   ├── RfidController.cs      # GET scans with filtering
│   │   │   ├── MotionController.cs    # GET events (last hour)
│   │   │   ├── StatusController.cs    # GET door/window/fan status
│   │   │   └── ControlController.cs   # POST actuator commands
│   │   ├── Models/
│   │   │   ├── SensorReadingModel.cs  # Maps to sensor_logs table
│   │   │   ├── RfidScanModel.cs       # Maps to rfid_scans table
│   │   │   ├── MotionEventModel.cs    # Maps to motion_events table
│   │   │   ├── GasAlertModel.cs       # Maps to gas_alerts table
│   │   │   └── DeviceStatusModel.cs   # Maps to device_status table
│   │   └── Contracts/
│   │       ├── ControlRequest.cs      # {"device": "door", "action": "open"}
│   │       └── FilterRequest.cs       # Query params for filtering
│   └── SmartHomeApi.Tests/            # Unit tests (optional Phase 1)
│
├── web/                        # Next.js web application (Phase 3)
│   ├── app/
│   │   ├── page.tsx           # Main dashboard
│   │   └── layout.tsx         # Root layout
│   ├── components/
│   │   ├── SensorCard.tsx     # Display sensor readings
│   │   ├── RFIDLog.tsx        # RFID scan history
│   │   ├── ControlPanel.tsx   # Actuator controls
│   │   └── MQTTProvider.tsx   # MQTT connection provider
│   ├── lib/
│   │   ├── api-client.ts      # Axios wrapper for C# API
│   │   └── mqtt.ts            # MQTT client setup
│   └── package.json
│
├── docs/                       # Project documentation
│   ├── api-endpoints.md       # REST API documentation
│   ├── hardware-pinout.md     # ESP32 pin configuration
│   ├── mqtt-topics.md         # MQTT topic structure
│   └── database-schema.md     # Supabase table design
│
├── planning/
│   ├── prd.md                 # Product requirements document
│   ├── architecture.md        # System architecture & data flow
│   ├── database-schema.sql    # PostgreSQL schema
│   ├── file-structure.md      # This file
│   ├── environment-setup.md   # Environment variable configuration
│   └── tasks.md               # Development task breakdown
│
├── project-brief/
│   └── smart_home_requirements.md  # Teacher requirements
│
├── development-notes.md        # Session log
└── README.md                   # Setup instructions
```

## Directory Purposes

### `/embedded` - ESP32 MicroPython Code

**Purpose**: All code that runs on the ESP32 hardware

**Key Files**:
- `main.py` - Main event loop, coordinates sensors/actuators
- `boot.py` - WiFi connection, runs before main.py
- `config.py` - Credentials (gitignored)

**Subdirectories**:
- `sensors/` - Classes for reading hardware sensors
- `actuators/` - Classes for controlling outputs (LED, servo, etc.)
- `display/` - OLED screen driver
- `network/` - MQTT and Supabase HTTP clients
- `utils/` - Helper functions (logging, time sync)

### `/api` - C# ASP.NET Core Backend

**Purpose**: REST API layer for querying historical data from Supabase

**Key Files**:
- `Program.cs` - Entry point, dependency injection, middleware
- `appsettings.json` - Configuration (Supabase URL, CORS)

**Subdirectories**:
- `Controllers/` - API endpoints (GET requests)
- `Models/` - Data models mapping to database tables
- `Contracts/` - Request/response DTOs

**Pattern**: MVC architecture without Views (API-only)

### `/web` - Next.js Frontend

**Purpose**: Web dashboard for monitoring and controlling the smart home

**Key Files**:
- `app/page.tsx` - Main dashboard page
- `lib/api-client.ts` - Axios wrapper for C# API
- `lib/mqtt.ts` - MQTT client for real-time updates

**Subdirectories**:
- `components/` - React components (sensor cards, control buttons)

### `/planning` - Design Documents

**Purpose**: Architecture decisions, requirements, database schema

**Files**:
- `prd.md` - Functional requirements with user stories
- `architecture.md` - Data flow diagrams, MQTT topics, API endpoints
- `database-schema.sql` - Supabase table definitions
- `file-structure.md` - This file
- `environment-setup.md` - Environment variable configuration

### `/docs` - Technical Documentation

**Purpose**: Reference documentation for implementation

**Files**:
- `api-endpoints.md` - REST API documentation
- `hardware-pinout.md` - ESP32 GPIO pin assignments
- `mqtt-topics.md` - MQTT topic structure
- `database-schema.md` - Database ERD and table descriptions

## Configuration Files

| File | Purpose | Gitignored |
|------|---------|-----------|
| `embedded/config.py` | WiFi, MQTT, Supabase credentials for ESP32 | ✅ Yes |
| `api/appsettings.Development.json` | C# API dev overrides | ✅ Yes |
| `web/.env.local` | Next.js environment variables | ✅ Yes |
| `api/appsettings.json` | C# API base config (no secrets) | ❌ No |

## Development Workflow

1. **Read planning docs** - `prd.md` for requirements, `architecture.md` for data flow
2. **Check file structure** - Identify which layer to modify (HOUSE/API/WEB)
3. **Implement feature** - Follow modular structure (one class per sensor/actuator)
4. **Test incrementally** - Don't wait until all features are complete
5. **Commit with FR reference** - Link code changes to functional requirements

## Related Documentation

- **Setup instructions**: See `README.md`
- **MQTT topics**: See `planning/architecture.md`
- **Database schema**: See `planning/database-schema.sql`
- **Environment setup**: See `planning/environment-setup.md`
