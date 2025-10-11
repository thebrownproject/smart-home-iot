# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Context

ESP32-based smart home automation system for Cert IV assessment. Four-layer IoT architecture:

- **HOUSE layer**: ESP32 MicroPython (sensors/outputs)
- **API layer**: C# ASP.NET Core 9.0 (REST endpoints, business logic)
- **WEB layer**: Next.js dashboard (monitoring/control)
- **DATABASE layer**: Supabase PostgreSQL (persistence)

Communication: ESP32 → Supabase (HTTPS) for persistence, ESP32 ↔ HiveMQ MQTT ↔ Next.js for real-time updates, Next.js → C# API → Supabase for queries.

## Available MCP Tools

**Context7** - Fetch up-to-date library documentation before writing code:
- Use `mcp__context7__resolve-library-id` to find libraries
- Use `mcp__context7__get-library-docs` to fetch specific documentation
- Always fetch docs BEFORE implementing features (see `/continue` workflow)

**Supabase** - Interact with Supabase database:
- Query schema and verify table structure
- Test database connections
- Run SQL queries for validation

## Branch Strategy

- `main` - Clean, stable baseline (all merged work)
- `phase-1-embedded-core` - ESP32 implementation (sensors, outputs, MQTT, Supabase)
- `phase-2-api-layer` - C# ASP.NET Core API (future)
- `phase-3-web-dashboard` - Next.js frontend (future)

**Legacy branches** (merged, can be deleted):
- `planning` - Initial documentation (merged to main)
- `001-comprehensive-smart-home` - Early implementation (merged to main)

## Key Documentation

**Read on every session** (in order):

1. `planning/prd.md` - Functional requirements with layer tags (HOUSE/WEB/DATABASE/API)
2. `planning/tasks.md` - Current milestone and next pending task

**Reference as needed** (context-dependent):

- `planning/architecture.md` - Data flow patterns, MQTT topics, API endpoints, design decisions
- `planning/file-structure.md` - Directory layout and file purposes
- `planning/environment-setup.md` - Credential configuration for ESP32, C# API, Next.js
- `planning/database-schema.sql` - PostgreSQL table definitions
- `project-brief/smart_home_requirements.md` - Teacher's original requirements (already captured in PRD)

## Layer Tag System

Every functional requirement in the PRD is tagged:

- `(HOUSE)` - Implement in ESP32 MicroPython
- `(API)` - Implement in C# ASP.NET Core (Phase 2)
- `(WEB)` - Implement in Next.js (Phase 3)
- `(DATABASE)` - Database schema/logging

Example: `FR2.1 (HOUSE): PIR sensor detects motion`

**Always check the layer tag before implementing**.

**MQTT Topics**: See `planning/architecture.md` for complete topic structure and message formats

## ESP32 Development (MicroPython)

**System Architecture (3-Layer Boot Pattern with Modular Handlers)**:

- `main.py` - Entry point (15 lines): Creates SystemInit → calls init() → creates SmartHomeApp → calls run()
- `system_init.py` - Hardware abstraction layer: Initializes all sensors, outputs, comms modules; handles boot sequence (WiFi, time sync, display messages)
- `app.py` - Event loop orchestrator: SmartHomeApp class imports and calls handler functions in main loop
- `handlers/` - Modular automation logic: One file per feature (lighting, motion, steam, gas, rfid, environment)

**Pattern**: main.py is minimal orchestration, system_init handles hardware initialization, app.py orchestrates the event loop, and handlers/ contain the automation rules. Each handler lazy-loads dependencies (sensors/outputs) inside the function, uses them, then deletes and runs garbage collection for memory efficiency.

**Handler Structure Example**:
```python
# handlers/motion.py
def handle_motion_detection(system, mqtt):
    """Check PIR sensor and respond to motion events"""
    from sensors.pir import PIRSensor
    from outputs.rgb import RGB
    # ... lazy load, use, delete pattern
```

**Deploy to hardware**:

1. Connect ESP32 via USB
2. VS Code → MicroPico extension
3. `MicroPico: Connect` then `MicroPico: Upload project to Pico`

**Reference code**: `Docs/Python/microPython Code/pj*_*.py` - Example implementations for each sensor/output

**Critical constraints**:

- ESP32 has ~100KB RAM - avoid importing unused libraries
- Use non-blocking patterns (no `time.sleep()` in main loop)
- Validate sensor readings (e.g., DHT11 range: -20 to 60°C)
- Handle network failures gracefully (MQTT/WiFi can disconnect)

**YAGNI Principle - "You Aren't Gonna Need It"**:

- Only implement features when **explicitly required** by the current task
- Don't add "nice to have" configuration, helper functions, or abstractions until actually needed
- Keep code simple and focused - this is a student project, not production software
- If in doubt, ask before adding extra functionality beyond the task requirements
- Example: Don't add debug flags, device IDs, or timing intervals until the code that uses them exists

## Data Flow Patterns

**Persistence**: ESP32 → POST Supabase → sensor_logs table

**Real-time**: ESP32 → MQTT publish → Next.js subscribes → UI update

**Control**: Next.js → MQTT publish → ESP32 subscribes → Output executes

**Historical**: Next.js → GET C# API → Query Supabase → Display charts/logs

## Hardware Pin Reference

- OLED Display: I2C (SDA:21, SCL:22, addr:0x3C)
- RFID Reader: I2C (SDA:21, SCL:22, addr:0x28)
- DHT11: Data pin 17
- PIR Motion: Signal pin 14
- Gas Sensor: Signal pin 23
- LED: Pin 12
- Door Servo: PWM pin 13

I2C bus is shared between OLED and RFID (different addresses).

## Commit Message Format

```bash
git commit -m "$(cat <<'EOF'
Implement DHT11 sensor class with error handling

- Add read() method with validation
- Return last good value on sensor errors
- Log errors to serial for debugging

Implements FR6.1 (HOUSE): DHT11 sensor reads temp/humidity

)"
```

Structure: Subject line, bullet points, FR reference, attribution footer.

## Workflow Commands

- **Start session**: Run `/continue` - Loads context, shows next task, handles implementation workflow
- **End session**: Run `/wrap-up` - Updates tasks.md, commits with FR references, adds session notes

Detailed workflow steps are in `/continue` command. Always use these commands for consistency.

**Database Schema**: `planning/database-schema.sql` - Tables: `devices`, `sensor_logs`, `rfid_scans`, `motion_events`, `gas_alerts`, `users`, `authorised_cards`

**Key Architectural Decision**: ESP32 writes directly to Supabase (not through C# API). C# API is read-only for querying historical data.

## Development Phases

**Phase 1: Embedded Core** - ESP32 sensors/outputs, MQTT pub/sub, Supabase direct logging, main event loop
**Phase 2: C# API** - ASP.NET Core 9.0 with Models/Controllers/Contracts, Supabase queries, Swagger docs
**Phase 3: Web Dashboard** - Next.js with MQTT subscriptions (real-time) and C# API calls (historical data)
**Phase 4: Bonus Features** - JWT authentication, user roles (Parent/Child), PIR arm/disarm, analytics

**Detailed phase breakdown**: See `planning/architecture.md`
