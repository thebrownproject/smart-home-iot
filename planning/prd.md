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

**As a user, I want to control outputs from the web app**

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
- **Outputs**: LED, RGB (SK6812), Servo motors, Fan, Buzzer
- **Display**: OLED (SSD1306) via I2C
- **Connectivity**: WiFi (ESP32 built-in), MQTT client

### API Layer (Phase 2)

- **Framework**: ASP.NET Core 9.0 Web API
- **Language**: C# 12
- **Architecture**: MVC pattern with Controllers, Models, Contracts
- **Database Client**: Supabase C# client (`Supabase` NuGet package)
- **Dependency Injection**: Scoped Supabase client registration
- **Documentation**: Swagger/OpenAPI
- **Validation**: Data Annotations + custom attributes
- **Hosting**: localhost:5000 (Phase 2), Azure/Railway (Phase 4)

### Cloud Services

- **MQTT Broker**: HiveMQ Cloud (free tier, SSL/TLS support)
- **Database**: Supabase PostgreSQL (cloud-hosted)
- **Communication Pattern**:
  - ESP32 → Supabase (direct HTTPS for data persistence)
  - ESP32 → HiveMQ → Web App (MQTT for real-time updates)
  - Web App → C# API → Supabase (queries and historical data)

### Web Application (Phase 3)

- **Frontend**: Next.js 15 (App Router) + TypeScript
- **Styling**: Tailwind CSS
- **MQTT Client**: `mqtt` npm package (subscribes to sensor topics)
- **API Client**: `axios` or native `fetch` (calls C# API endpoints)

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

- **Non-blocking patterns**: Avoid `sleep()` in main loop; handle sensor failures gracefully with timeouts
- **Memory-conscious**: ESP32 has ~100KB RAM—import only needed libraries, use efficient data structures
- **Network resilience**: Retry logic for MQTT/WiFi; never assume network availability
- **Error handling**: Log failures to serial for debugging; return last good sensor values on read errors

### Web App Code (Next.js)

**LIGHTWEIGHT & RESPONSIVE - This is a monitoring dashboard, not a SaaS product**

- **Simplicity first**: Clean UI components, React hooks for state (no complex state libraries)
- **Real-time focus**: MQTT subscriptions for live updates; C# API for historical queries
- **Clear errors**: Surface connection issues to user (MQTT disconnected, API timeout)

---

**File Structure**: See `planning/file-structure.md` for complete directory organization

**MQTT Topics**: See `planning/architecture.md`
**Database Schema**: See `planning/database-schema.sql`
**Environment Setup**: See `planning/environment-setup.md`

---

**Development Phases**: See `planning/architecture.md` for implementation workflow

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

❌ User authentication (bonus feature - Phase 4)
❌ Historical data charts (basic list only - Phase 3 enhancement)
❌ Mobile app (web-responsive is sufficient)
❌ Production deployment (localhost testing initially)
❌ PIR arming system (bonus feature - Phase 4)
❌ Multiple house zones (single room system)

---

## Future Enhancements (Post-Assessment)

**Phase 4 - Bonus Requirements:**

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
