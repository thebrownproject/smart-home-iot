# Smart Home Automation System - PRD

## Project Goal
Build an ESP32-based smart home automation system that demonstrates IoT integration, embedded programming, and full-stack development skills for Cert IV assessment. The system monitors environmental conditions, manages security, controls access, and responds to emergencies—all while logging data to the cloud and providing real-time web monitoring.

---

## User Stories & Functional Requirements

### Phase 1: Embedded System (Standard Requirements)

#### US1: Time-Based Lighting
**As a homeowner, I want the LED to automatically turn on during nighttime hours**

- **FR1.1 (HOUSE)**: LED lights up between 8pm and 7am
- **FR1.2 (HOUSE)**: System tracks current time via NTP or RTC
- **FR1.3 (HOUSE)**: LED turns off automatically outside nighttime hours

#### US2: Motion Detection & Response
**As a homeowner, I want the system to respond when motion is detected**

- **FR2.1 (HOUSE)**: PIR sensor detects motion
- **FR2.2 (HOUSE)**: RGB LED lights up orange when motion detected
- **FR2.3 (DATABASE)**: Motion events logged to database with timestamp

#### US3: Steam Detection & Window Control
**As a homeowner, I want the window to close automatically when steam is detected**

- **FR3.1 (HOUSE)**: Steam sensor detects moisture/water droplets
- **FR3.2 (HOUSE)**: Servo motor closes window when moisture detected
- **FR3.3 (HOUSE)**: RGB LED flashes blue as visual indicator

#### US4: Gas Detection & Emergency Response
**As a homeowner, I want comprehensive safety response when gas/flame is detected**

- **FR4.1 (HOUSE)**: Gas sensor continuously monitors for gas/flame
- **FR4.2 (HOUSE)**: Fan activates when gas detected, runs until sensor clears
- **FR4.3 (HOUSE)**: RGB LED shows solid red during gas alert
- **FR4.4 (DATABASE)**: All detections logged with timestamp and sensor value

#### US5: RFID Access Control
**As a homeowner, I want secure door access using RFID cards**

- **FR5.1 (HOUSE)**: RFID reader scans cards
- **FR5.2 (HOUSE)**: Unknown cards trigger red flashing RGB + buzzer
- **FR5.3 (HOUSE)**: Valid cards open door (servo motor)
- **FR5.4 (DATABASE)**: All scans logged: card ID, success/fail, timestamp
- **FR5.5 (HOUSE)**: Display access status on LCD/OLED

#### US6: Environmental Monitoring
**As a homeowner, I want to see current environmental conditions**

- **FR6.1 (HOUSE)**: DHT11 sensor reads temperature (celsius) and humidity (%)
- **FR6.2 (HOUSE)**: Display current values on OLED continuously
- **FR6.3 (WEB)**: Data published via MQTT for web dashboard
- **FR6.4 (DATABASE)**: Temperature/humidity logged every 30 minutes

#### US7: Asthma Alert System
**As a homeowner, I want alerts when conditions trigger asthma risk**

- **FR7.1 (HOUSE)**: Monitor humidity > 50% AND temperature > 27°C
- **FR7.2 (HOUSE + WEB)**: Display "ASTHMA ALERT" on OLED and web dashboard when conditions met
- **FR7.3 (WEB)**: Alert status published via MQTT

#### US8: Real-Time System Monitoring
**As a user, I want to monitor system status via web dashboard**

- **FR8.1 (WEB)**: Display PIR detections in last hour (from database)
- **FR8.2 (WEB)**: Show gas detection alerts in real-time
- **FR8.3 (WEB)**: List all RFID scans with filter (success/failed)
- **FR8.4 (WEB)**: Display door and window status (open/closed)
- **FR8.5 (WEB)**: Display fan status (on/off)

#### US9: Remote Control
**As a user, I want to control actuators from the web app**

- **FR9.1 (WEB)**: Open window via web interface (publishes MQTT command)
- **FR9.2 (WEB)**: Open door via web interface
- **FR9.3 (WEB)**: Turn on/off fan via web interface
- **FR9.4 (HOUSE)**: ESP32 subscribes to control MQTT topics and executes commands

---

## Tech Stack

### Embedded System (ESP32)
- **Language**: MicroPython 1.20+
- **Hardware**: ESP32 microcontroller + KS5009 smart home kit
- **Sensors**: DHT11, PIR, Gas, Steam/Moisture, RFID (RC522)
- **Actuators**: LED, RGB (SK6812), Servo motors, Fan, Buzzer
- **Display**: OLED (SSD1306) via I2C
- **Connectivity**: WiFi (ESP32 built-in), MQTT client

### Cloud Services
- **MQTT Broker**: HiveMQ Cloud (free tier, SSL/TLS support)
- **Database**: Supabase PostgreSQL (cloud-hosted)
- **Communication Pattern**:
  - ESP32 → Supabase (direct HTTPS for data persistence)
  - ESP32 → HiveMQ → Web App (MQTT for real-time updates)

### Web Application (Phase 2)
- **Frontend**: Next.js 15 (App Router) + TypeScript
- **Styling**: Tailwind CSS
- **MQTT Client**: `mqtt` npm package (subscribes to sensor topics)
- **Database Client**: `@supabase/supabase-js` (reads sensor logs)

### Development Environment
- **IDE**: VS Code with MicroPico extension
- **Deployment**: ESP32 via USB, Web app localhost (Phase 1)
- **Version Control**: Git + GitHub
- **Project Management**: GitHub Projects (user stories, tasks)

**Architecture**: See `planning/architecture.md` for data flow diagrams

---

## Code Philosophy

### Embedded Code (MicroPython)
**ROBUST & EFFICIENT - This code runs 24/7 on constrained hardware**

#### DO:
✅ Handle sensor failures gracefully (timeouts, bad reads)
✅ Use non-blocking patterns (avoid long sleep() in main loop)
✅ Implement retry logic for network operations
✅ Memory-efficient data structures (ESP32 has limited RAM)
✅ Modular sensor/actuator classes with clean interfaces
✅ Comprehensive error logging (help debug hardware issues)

#### DON'T:
❌ Block main loop with synchronous I/O
❌ Import unused libraries (memory waste)
❌ Use global state without clear ownership
❌ Assume network always available
❌ Ignore sensor edge cases (disconnected, noise)

### Web App Code (Next.js)
**LIGHTWEIGHT & RESPONSIVE - This is a monitoring dashboard, not a SaaS product**

#### DO:
✅ Simple, clean UI components
✅ Real-time updates via MQTT subscriptions
✅ Efficient state management (React hooks)
✅ Clear error messages for connection issues

#### DON'T:
❌ Over-engineer with state management libraries
❌ Complex middleware/abstractions
❌ Unnecessary API layers (read Supabase directly)

---

## File Structure

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
├── web/                        # Next.js web application (Phase 2)
│   ├── app/
│   │   ├── page.tsx           # Main dashboard
│   │   ├── layout.tsx         # Root layout
│   │   └── api/
│   │       └── supabase/
│   │           └── route.ts   # Supabase query endpoints
│   ├── components/
│   │   ├── SensorCard.tsx     # Display sensor readings
│   │   ├── RFIDLog.tsx        # RFID scan history
│   │   ├── ControlPanel.tsx   # Actuator controls
│   │   └── MQTTProvider.tsx   # MQTT connection provider
│   ├── lib/
│   │   ├── mqtt.ts            # MQTT client setup
│   │   └── supabase.ts        # Supabase client
│   └── package.json
│
├── docs/                       # Project documentation
│   ├── architecture-decisions.md  # ADR log
│   ├── hardware-pinout.md     # ESP32 pin configuration
│   ├── mqtt-topics.md         # MQTT topic structure
│   └── database-schema.md     # Supabase table design
│
├── project-brief/
│   └── smart_home_requirements.md  # Teacher requirements
│
├── prd.md                      # This file
├── tasks.md                    # Development task breakdown
├── development-notes.md        # Session log
└── README.md                   # Setup instructions
```

**MQTT Topics**: See `planning/architecture.md`
**Database Schema**: See `planning/database-schema.sql`

---

## Development Flow (Embedded-First Approach)

### Phase 1: ESP32 Core (Current Focus)
1. Set up hardware connections and validate sensors
2. Implement individual sensor classes with test scripts
3. Build actuator control modules
4. Integrate WiFi + MQTT connectivity
5. Add Supabase HTTP client for data logging
6. Implement main event loop with state machine
7. Test complete automation scenarios

### Phase 2: Web Dashboard
1. Set up Next.js project with MQTT + Supabase clients
2. Build real-time sensor display components
3. Create RFID scan history with filtering
4. Implement control panel for actuators
5. Add charts for historical data
6. Test end-to-end: sensor → DB → web display

### Phase 3: Bonus Features (Optional)
1. Implement user authentication + roles
2. PIR arm/disarm functionality
3. Advanced analytics (avg temp per day)
4. Alarm system with web-based disarm

**API Endpoints**: See `planning/architecture.md`

---

## Environment Variables

### ESP32 (config.py)
```python
WIFI_SSID = "your_network"
WIFI_PASSWORD = "your_password"

MQTT_BROKER = "broker.hivemq.cloud"
MQTT_PORT = 8883  # SSL/TLS
MQTT_USER = "your_username"
MQTT_PASSWORD = "your_password"

SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_ANON_KEY = "your_anon_key"
```

### Next.js (.env.local)
```
NEXT_PUBLIC_MQTT_BROKER=wss://broker.hivemq.cloud:8884/mqtt
NEXT_PUBLIC_MQTT_USER=your_username
NEXT_PUBLIC_MQTT_PASSWORD=your_password

NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
```

---

## Success Criteria (Assessment Requirements)

### Functional Requirements
✅ All 5 standard house requirements working (LED, PIR, Steam, Gas, RFID)
✅ All 10 web app requirements implemented (dashboard, controls, history)
✅ All 5 database requirements met (30min logs, PIR/gas/RFID logging)
✅ Real-time MQTT communication between ESP32 and web app
✅ Direct Supabase integration for data persistence

### Technical Requirements
✅ MicroPython used for ESP32 programming
✅ JavaScript framework (Next.js) for web app
✅ Relational database (Supabase PostgreSQL) with ERD
✅ MQTT for house ↔ web communication
✅ Git version control with meaningful commits
✅ User stories tracked in GitHub Projects
✅ Wireframes/mockups created

### Quality Standards
- System runs reliably for 1+ hour without crashes
- Sensor readings accurate within ±5% (temperature, humidity)
- Web dashboard updates within 2 seconds of sensor event
- RFID scan response < 500ms
- All emergency responses trigger within 1 second (gas, steam)

---

## Out of Scope (Phase 1)

❌ User authentication (bonus feature - Phase 3)
❌ C# API layer (bonus requirement - Phase 3)
❌ Historical data charts (basic list only - Phase 2 enhancement)
❌ Mobile app (web-responsive is sufficient)
❌ Production deployment (localhost testing for Phase 1)
❌ PIR arming system (bonus feature - Phase 3)
❌ Multiple house zones (single room system)

---

## Future Enhancements (Post-Assessment)

**Phase 3 - Bonus Requirements:**
- User roles: Parent (full control) vs Child (view-only)
- PIR arm/disarm via button combo + web interface
- Alarm system with web-based disarm
- Card registration via button + RFID scan
- Average temperature per day analytics

**Production Deployment:**
- CI/CD pipeline (GitHub Actions)
- Deploy web app to Vercel/Netlify
- Secure MQTT with SSL/TLS certificates
- Environment-based configuration
- Monitoring and alerting (uptime tracking)

---

## Assessment Deliverables Checklist

### Code Deliverables
- [ ] Working ESP32 MicroPython codebase
- [ ] Next.js web application
- [ ] Git repository with commit history
- [ ] README with setup instructions

### Documentation
- [ ] ERD (database schema diagram)
- [ ] Wireframes/mockups for web app
- [ ] MQTT topic documentation
- [ ] Architecture decision records
- [ ] Hardware pinout diagram

### Project Management
- [ ] GitHub Projects board with user stories
- [ ] Tasks with start/completion dates
- [ ] Sprint planning (if using Agile approach)

### Learning Reflection
- [ ] Development process analysis
- [ ] Challenges overcome
- [ ] Skills acquired (technical + soft skills)
- [ ] What you'd do differently next time
