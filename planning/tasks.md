# Smart Home Automation - Development Tasks

## Project Status: Phase 1 In Progress

**Current Phase**: Phase 1 - Embedded System Core
**Started**: 2025-10-07

---

## Phase 1: Embedded System Core (Standard Requirements)

### Milestone 1.1: Environment & Database Setup ✅ (Partially Complete)

- [x] **T1.1**: Hardware validation testing

  - Validate sensors using reference code in `Docs/reference-code/`
  - Test DHT11, PIR, Gas, Steam, RFID modules individually
  - Document any hardware issues or pin conflicts
  - **Started**: 2025-10-08
  - **Completed**: 2025-10-08

- [x] **T1.2**: Create Supabase project and database schema

  - Sign up for Supabase account (free tier)
  - Create new project: "smart-home-project"
  - Execute SQL schema from `planning/database-schema.sql`
  - Create indexes for timestamp-based queries
  - Test connection with Supabase API key
  - **Started**: 2025-10-08
  - **Completed**: 2025-10-08

- [x] **T1.3**: Set up MQTT credentials in ESP32 config

  - Create `esp32/config.py` with MQTT broker details
  - Add WiFi credentials (SSID, password)
  - Add Supabase URL and anon key
  - Test MQTT connection using simple publish/subscribe test
  - **Started**: 2025-10-08
  - **Completed**: 2025-10-08

- [x] **T1.4**: Create project file structure
  - Create `esp32/` directory with subdirectories (sensors, outputs, comms, display, utils)
  - Set up `esp32/boot.py` for WiFi initialization
  - Create placeholder files for all modules listed in `prd.md`
  - Add `.gitignore` for `config.py` and sensitive files
  - **Started**: 2025-10-08
  - **Completed**: 2025-10-08

---

### Milestone 1.2: Sensor Module Implementation

- [x] **T1.5**: Implement DHT11 sensor class **(FR6.1 - HOUSE)**

  - File: `esp32/sensors/dht11.py`
  - Methods: `read_temperature()`, `read_humidity()`
  - Error handling for sensor timeouts (return None on failure)
  - Test: Read values every 2 seconds for 1 minute, verify reasonable range (-20 to 60°C)
  - **Completed**: 2025-10-08

- [x] **T1.6**: Implement PIR motion sensor class **(FR2.1 - HOUSE)**

  - File: `esp32/sensors/pir.py`
  - Methods: `is_motion_detected()`, `read()` (returns boolean)
  - Debounce logic to prevent rapid triggers
  - Test: Wave hand in front of sensor, verify detection
  - **Started**: 2025-10-08
  - **Completed**: 2025-10-09

- [x] **T1.7**: Implement Gas sensor class **(FR4.1 - HOUSE)**

  - File: `esp32/sensors/gas.py`
  - Methods: `is_gas_detected()`, `read_value()` (digital pin value)
  - Test: Trigger sensor, verify digital signal
  - **Started**: 2025-10-08
  - **Completed**: 2025-10-09

- [x] **T1.8**: Implement Steam/Moisture sensor class **(FR3.1 - HOUSE)**

  - File: `esp32/sensors/steam.py`
  - Methods: `is_moisture_detected()`, `read()`
  - Test: Simulate steam/water droplet detection
  - **Started**: 2025-10-08
  - **Completed**: 2025-10-09

- [x] **T1.9**: Implement RFID reader class **(FR5.1 - HOUSE)**
  - File: `esp32/sensors/rfid.py`
  - Use MFRC522 library from `Docs/reference-code/pj10_rc522_RFID/`
  - Methods: `scan_card()`, `get_card_id()`
  - Test: Scan known RFID card, print card ID
  - **Started**: 2025-10-08
  - **Completed**: 2025-10-09

---

### Milestone 1.3: Output Module Implementation

- [x] **T1.10**: Implement LED control class

  - File: `esp32/outputs/led.py`
  - Methods: `on()`, `off()`, `toggle()`
  - Test: Turn LED on/off programmatically
  - **Started**: 2025-10-09
  - **Completed**: 2025-10-09

- [x] **T1.11**: Implement RGB LED (SK6812) class

  - File: `esp32/outputs/rgb.py`
  - Methods: `set_color(r, g, b)`, `flash(color, times)`, `off()`
  - Support orange, blue, red colors for requirements
  - Test: Flash RGB in different colors
  - **Started**: 2025-10-09
  - **Completed**: 2025-10-09

- [x] **T1.12**: Implement Servo motor class

  - File: `esp32/outputs/servo.py`
  - Methods: `open()`, `close()`
  - Generic class accepts pin parameter for door (pin 13) and window (pin 5)
  - Test: Open/close door and window servos
  - **Started**: 2025-10-09
  - **Completed**: 2025-10-09

- [x] **T1.13**: Implement Fan control class

  - File: `esp32/outputs/fan.py`
  - Methods: `on()`, `off()`, `is_running()`
  - Test: Turn fan on/off, verify operation
  - **Started**: 2025-10-09
  - **Completed**: 2025-10-09

- [x] **T1.14**: Implement Buzzer class
  - File: `esp32/outputs/buzzer.py`
  - Methods: `beep(duration)`, `pattern(beeps, interval)`, `stop()`
  - Test: Play buzzer patterns
  - **Started**: 2025-10-09
  - **Completed**: 2025-10-09

---

### Milestone 1.4: Display & Network Integration

- [x] **T1.15**: Implement OLED display class

  - File: `esp32/display/oled.py`
  - Use LCD1602 library for I2C communication (hardware is 16x2 LCD, not OLED)
  - Methods: `show_text(line1, line2)`, `clear()`, `show_temp_humidity(temp, humidity)`
  - Test: Display "Hello World" on LCD
  - **Started**: 2025-10-09
  - **Completed**: 2025-10-09

- [x] **T1.16**: Implement WiFi connection manager

  - File: `esp32/comms/wifi_manager.py`
  - Auto-connect on boot using credentials from config.py
  - Retry logic with simple 2-second intervals (5 attempts)
  - Methods: `connect()`, `is_connected()`, `get_ip()`
  - WiFi interface reset on each connection to clear error states
  - Integrated into main.py with LCD status display showing network name
  - Test: Connect to WiFi, display network name on LCD
  - **Started**: 2025-10-10
  - **Completed**: 2025-10-10

- [x] **T1.17**: Implement MQTT client wrapper

  - File: `esp32/comms/mqtt_client.py`
  - Use `umqtt.simple` or `umqtt.robust` library
  - Methods: `connect()`, `publish(topic, payload)`, `subscribe(topic, callback)`, `check_messages()`
  - Handle connection failures gracefully
  - Test: Publish to `home/test` topic, verify on HiveMQ web console
  - **Started**: 2025-10-11
  - **Completed**: 2025-10-11

- [ ] **T1.18**: Implement Supabase HTTP client
  - File: `esp32/comms/supabase.py`
  - Methods: `insert_sensor_log(sensor_type, value, unit)`, `insert_rfid_scan(card_id, result)`
  - Use `urequests` library for HTTP POST
  - Include API key in headers
  - Test: Insert dummy sensor log, verify in Supabase dashboard

---

### Milestone 1.5: Core Automation Logic (US1-US5)

- [ ] **T1.19**: Implement time-based LED control **(FR1.1, FR1.2, FR1.3 - HOUSE)**

  - Add NTP time sync in `esp32/utils/time_sync.py`
  - Main loop: Check if time between 8pm-7am
  - Turn LED on during nighttime hours, off during day
  - Test: Set ESP32 time manually, verify LED behavior

- [ ] **T1.20**: Implement PIR motion response **(FR2.1, FR2.2, FR2.3 - HOUSE/DATABASE)**

  - Main loop: Poll PIR sensor
  - On motion: Set RGB to orange, log to `motion_events` table
  - Publish MQTT event to `home/motion`
  - Test: Trigger motion, verify RGB and MQTT message

- [ ] **T1.21**: Implement steam detection & window control **(FR3.1, FR3.2, FR3.3 - HOUSE)**

  - Main loop: Poll steam sensor
  - On moisture: Close window servo, flash RGB blue
  - Publish MQTT event to `home/steam`
  - Test: Simulate steam, verify window closes

- [ ] **T1.22**: Implement gas detection & emergency response **(FR4.1, FR4.2, FR4.3, FR4.4 - HOUSE/DATABASE)**

  - Main loop: Poll gas sensor
  - On gas detected: Turn on fan, set RGB to solid red
  - Log alert with start time to `gas_alerts` table
  - Fan runs until sensor clears, then log end time
  - Test: Trigger gas sensor, verify fan activation

- [ ] **T1.23**: Implement RFID access control **(FR5.1-FR5.5 - HOUSE/DATABASE)**
  - Query Supabase `authorised_cards` table for card validation
  - Main loop: Scan for RFID cards
  - Unknown card: Flash RGB red + buzzer (FR5.2)
  - Known card: Open door servo, show "ACCESS GRANTED" on OLED (FR5.3, FR5.5)
  - Log all scans to `rfid_scans` table (FR5.4)
  - Publish MQTT event to `home/rfid`
  - Test: Scan known/unknown cards, verify behavior

---

### Milestone 1.6: Environmental Monitoring (US6, US7)

- [ ] **T1.24**: Implement continuous temperature/humidity display **(FR6.1, FR6.2, FR6.3 - HOUSE/WEB)**

  - Main loop: Read DHT11 every 2 seconds
  - Display current values on OLED (e.g., "Temp: 24.5C\nHumid: 60%")
  - Publish to MQTT topics `home/temperature` and `home/humidity`
  - Test: Verify OLED updates and MQTT messages

- [ ] **T1.25**: Implement 30-minute sensor logging **(FR6.4 - DATABASE)**

  - Use timer to trigger database insert every 30 minutes
  - Insert temperature and humidity to `sensor_logs` table
  - Test: Wait 30 mins, verify database entry

- [ ] **T1.26**: Implement asthma alert system **(FR7.1, FR7.2, FR7.3 - HOUSE/WEB)**
  - Check conditions: humidity > 50% AND temperature > 27°C
  - If true: Display "ASTHMA ALERT" on OLED
  - Publish alert to MQTT topic `home/asthma_alert`
  - Test: Set conditions manually, verify alert

---

### Milestone 1.7: Manual Controls & State Management

- [ ] **T1.27**: Implement button controls

  - Gas alarm disable button: Turn off fan and buzzer when pressed
  - PIR toggle button: Enable/disable motion detection
  - Test: Press buttons, verify output responses

- [ ] **T1.28**: Implement MQTT control subscriptions **(FR9.1, FR9.2, FR9.3, FR9.4 - WEB/HOUSE)**

  - Subscribe to `home/control/door`, `home/control/window`, `home/control/fan`
  - Parse JSON payload and execute commands
  - Example: `{"action": "open"}` → open door servo
  - Publish status updates to `home/status/*` topics
  - Test: Publish control commands via HiveMQ console, verify actions

- [ ] **T1.29**: Build main event loop with state machine
  - File: `esp32/main.py`
  - Initialize all sensors, outputs, network connections
  - Non-blocking loop: Poll sensors, check MQTT messages, update displays
  - Handle priority events (gas > steam > motion)
  - Comprehensive error handling with recovery
  - Test: Run for 1 hour, verify no crashes

---

### Milestone 1.8: Testing & Validation

- [ ] **T1.30**: End-to-end hardware test

  - Trigger all sensors sequentially
  - Verify correct output responses
  - Check MQTT messages in HiveMQ console
  - Verify database entries in Supabase dashboard
  - Document any issues

- [ ] **T1.31**: Create test documentation
  - File: `docs/hardware-testing-log.md`
  - Document test scenarios and results
  - Include screenshots of MQTT/Supabase data
  - List any hardware bugs or workarounds

---

## Phase 2: C# API Layer (Backend)

### Milestone 2.1: C# API Setup

- [ ] **T2.1**: Create C# ASP.NET Core 9.0 Web API project

  - Create `api/` directory
  - Initialize project: `dotnet new webapi -n SmartHomeApi`
  - Install NuGet packages: `Supabase` (Supabase C# client)
  - Configure `appsettings.json` with Supabase URL and API key

- [ ] **T2.2**: Implement Supabase data access layer

  - File: `api/Services/SupabaseService.cs`
  - Create methods to query sensor_logs, rfid_scans, motion_events, gas_alerts
  - Test database connection

- [ ] **T2.3**: Create REST API endpoints (GET only)

  - File: `api/Controllers/SensorsController.cs`
  - `GET /api/sensors/temperature?hours=24` - Historical temperature
  - `GET /api/sensors/humidity?hours=24` - Historical humidity
  - `GET /api/sensors/motion?hours=1` - Motion events
  - `GET /api/sensors/gas` - Gas alerts
  - Test with Postman or curl

- [ ] **T2.4**: Create RFID controller
  - File: `api/Controllers/RfidController.cs`
  - `GET /api/rfid/scans?filter=all|success|failed` - RFID history with filtering
  - Test filtering logic

---

## Phase 3: Web Dashboard (Frontend)

### Milestone 3.1: Next.js Project Setup

- [ ] **T3.1**: Initialize Next.js project

  - Create `web/` directory
  - Run `npx create-next-app@latest` with TypeScript, Tailwind, App Router
  - Install dependencies: `mqtt`
  - Configure environment variables in `.env.local`

- [ ] **T3.2**: Set up C# API client

  - File: `web/lib/api.ts`
  - Create fetch wrapper for C# API endpoints
  - Test: Fetch sensor data from C# API

- [ ] **T3.3**: Set up MQTT client provider
  - File: `web/lib/mqtt.ts` and `web/components/MQTTProvider.tsx`
  - Connect to HiveMQ WebSocket (wss://...)
  - Subscribe to `home/#` (all topics)
  - Provide real-time updates via React Context

---

### Milestone 3.2: Dashboard UI Components (US8)

- [ ] **T3.4**: Create sensor display card component **(FR8.1, FR8.2 - WEB)**

  - File: `web/components/SensorCard.tsx`
  - Display current temperature, humidity (from MQTT via FR6.3)
  - Real-time updates when new values arrive
  - Show last update timestamp

- [ ] **T3.5**: Create motion detection display **(FR8.1 - WEB)**

  - Query C# API for motion events in last hour
  - Display count: "PIR Detections (Last Hour): 12"
  - Auto-refresh every 5 minutes

- [ ] **T3.6**: Create gas alert indicator **(FR8.2 - WEB)**

  - File: `web/components/GasAlert.tsx`
  - Show red banner when gas detected (via MQTT)
  - Display "GAS DETECTED - FAN ACTIVE"
  - Hide when alert clears

- [ ] **T3.7**: Create RFID scan history table **(FR8.3 - WEB)**

  - File: `web/components/RFIDLog.tsx`
  - Fetch from C# API (`GET /api/rfid/scans`)
  - Display: Card ID, Result (granted/denied), Timestamp, User
  - Add filter dropdown: "All", "Success", "Failed"
  - Pagination: Show last 50 scans

- [ ] **T3.8**: Create status indicators **(FR8.4, FR8.5 - WEB)**
  - Display door/window status (open/closed) from MQTT
  - Display fan status (on/off)
  - Use color-coded badges (green = open, red = closed)

---

### Milestone 3.3: Control Panel (US9)

- [ ] **T3.9**: Create output control panel

  - File: `web/components/ControlPanel.tsx`
  - Buttons: "Open Door", "Close Door", "Open Window", "Close Window"
  - Toggle for Fan: "Turn On" / "Turn Off"
  - Click handler publishes MQTT command to `home/control/*`

- [ ] **T3.10**: Add control confirmation feedback
  - Show toast notification when command sent
  - Update button state based on status MQTT messages
  - Disable buttons while command in progress

---

### Milestone 3.4: Main Dashboard Page

- [ ] **T3.11**: Build main dashboard layout

  - File: `web/app/page.tsx`
  - Grid layout: Sensor cards (top), Status indicators (middle), Control panel (bottom)
  - RFID log table on side panel
  - Responsive design (mobile-friendly)

- [ ] **T3.12**: Add asthma alert banner
  - Subscribe to `home/asthma_alert` MQTT topic
  - Show prominent yellow banner when alert active
  - Display: "⚠️ ASTHMA ALERT - Humidity: 55%, Temp: 28°C"

---

### Milestone 3.5: Testing & Polish

- [ ] **T3.13**: End-to-end web app test

  - Start ESP32 system
  - Open web dashboard
  - Trigger sensors, verify real-time updates
  - Test control commands, verify outputs respond
  - Check RFID log filtering

- [ ] **T3.14**: Add error handling

  - MQTT connection lost: Show "Disconnected" banner
  - C# API query failure: Show error message
  - Retry logic for network failures

- [ ] **T3.15**: Performance optimization
  - Debounce MQTT updates (avoid UI thrashing)
  - Lazy load RFID history (don't fetch all on initial load)
  - Add loading skeletons for async data

---

## Phase 4: Bonus Requirements (Optional)

### Milestone 4.1: User Authentication & Roles

- [ ] **T4.1**: Implement Supabase Auth in web app

  - Add login/signup pages
  - Create users table with roles (Parent, Child)
  - Protect routes based on role

- [ ] **T4.2**: Role-based access control
  - Parent role: Full control (view + control outputs)
  - Child role: View-only (no control buttons)
  - C# API enforces permissions

---

### Milestone 4.2: Advanced PIR Features

- [ ] **T4.3**: PIR arm/disarm system (ESP32)

  - Button combo: 2 clicks left, 3 clicks right, 1 click left to arm/disarm
  - When armed + motion detected: Buzzer alarm + RGB flash blue/red
  - Auto-disarm on valid RFID scan

- [ ] **T4.4**: PIR web control
  - Add "Arm PIR" / "Disarm PIR" button in web app
  - Publish MQTT command to ESP32
  - Display alarm status on dashboard

---

### Milestone 4.3: Analytics & History

- [ ] **T4.5**: Calculate average temperature per day

  - C# API: Query `sensor_logs`, group by date, calculate AVG
  - Endpoint: GET `/api/analytics/temperature/daily`
  - Display in web dashboard as chart (recharts library)

- [ ] **T4.6**: Historical data filtering

  - Web component: Date range picker
  - Filter temperature/humidity logs by date
  - Display results in table or chart

- [ ] **T4.7**: RFID card registration
  - Button combo on ESP32: Hold both buttons + scan card to register
  - Save card ID to Supabase `authorised_cards` table
  - Web interface to associate card with user name

---

## Phase 5: Assessment Deliverables

### Milestone 5.1: Documentation

- [ ] **T5.1**: Create ERD (Entity Relationship Diagram)

  - Tool: dbdiagram.io or draw.io
  - Show all tables, relationships, indexes
  - Export as PNG/PDF to `docs/erd.png`

- [ ] **T4.2**: Create web app wireframes

  - Tool: Figma or Excalidraw
  - Wireframes for: Dashboard, RFID Log, Control Panel
  - Export to `docs/wireframes/`

- [ ] **T4.3**: Write README.md

  - Project overview
  - Hardware requirements and setup
  - Software installation (ESP32 + Web app)
  - Environment variable configuration
  - How to run the system

- [ ] **T4.4**: Document MQTT topics

  - File: `docs/mqtt-topics.md`
  - List all topics with payload examples
  - Explain pub/sub patterns

- [ ] **T4.5**: Create hardware pinout diagram
  - File: `docs/hardware-pinout.md`
  - List all ESP32 pin connections
  - Include I2C addresses for RFID, OLED

---

### Milestone 4.2: Project Management

- [ ] **T4.6**: Set up GitHub Projects board

  - Create project: "Smart Home Automation"
  - Convert user stories to GitHub Issues
  - Create columns: Backlog, In Progress, Done
  - Link commits to issues

- [ ] **T4.7**: Add task timestamps
  - For each completed task in GitHub, add:
    - Date started (in issue description)
    - Date completed (when issue closed)
  - Track total development time

---

### Milestone 4.3: Learning Reflection

- [ ] **T4.8**: Write development process reflection

  - File: `docs/learning-reflection.md`
  - Sections:
    1. Challenges encountered and solutions
    2. Technical skills acquired (MicroPython, MQTT, IoT patterns)
    3. Problem-solving approach (debugging hardware, network issues)
    4. What you'd do differently next time
    5. Most valuable learning moments

- [ ] **T4.9**: Code review and cleanup
  - Remove debug print statements
  - Add comments for complex logic
  - Ensure consistent code style
  - Remove unused imports/files

---

### Milestone 4.4: Deployment & CI/CD

- [ ] **T4.10**: Set up GitHub Actions CI/CD

  - Create `.github/workflows/test.yml`
  - Run linting on commits (optional for MicroPython)
  - Auto-deploy web app to Vercel on merge to main

- [ ] **T4.11**: Deploy web app to Vercel
  - Connect GitHub repo to Vercel
  - Configure environment variables
  - Test production deployment

---

## Notes for Development Sessions

### Current Task Tracking

- **Active Milestone**: 1.1 - Environment & Database Setup
- **Next Task**: T1.2 - Create Supabase project and database schema
- **Blockers**: None currently

### Development Principles

1. **Test each module independently** before integration
2. **Commit after each completed task** with meaningful message
3. **Document hardware issues** immediately in `development-notes.md`
4. **Take breaks** between milestones to review code quality
5. **Ask for help** on blockers (hardware, network, debugging)

### Session Workflow

1. Read `tasks.md` to find next pending task
2. Mark task as in progress (change `[ ]` to `[~]`)
3. Implement and test the task
4. Mark as complete (`[x]`) and commit
5. Update `development-notes.md` with insights/issues
6. Move to next task

### Quick Reference

- **ESP32 deployment**: Use MicroPico extension in VS Code
- **MQTT testing**: HiveMQ web console for pub/sub
- **Database check**: Supabase dashboard SQL editor
- **Web app**: `cd web && npm run dev`

---

## Task Summary

**Phase 1 (Embedded)**: 31 tasks (1 complete, 30 pending)
**Phase 2 (Web App)**: 15 tasks
**Phase 3 (Bonus)**: 10 tasks
**Phase 4 (Deliverables)**: 11 tasks

**Total**: 67 tasks

**Estimated Timeline**:

- Phase 1: 3-4 weeks (core development)
- Phase 2: 1-2 weeks (web dashboard)
- Phase 3: 2-3 weeks (bonus features - optional)
- Phase 4: 1 week (documentation & deployment)

**Current Status**: Phase 1, Milestone 1.1, Task T1.2 (Supabase setup)
