# Development Notes

A running diary of development decisions, important context, and session-to-session notes.

---

## Session 1 - October 7, 2025

### Project Planning & Architecture ✅

**What was completed:**
- Created planning documents: `prd.md`, `tasks.md`, `architecture.md`, `database-schema.sql`
- Defined system architecture with corrected data flows
- Established 4-phase development approach
- Created `/continue` slash command for session resumption

**Important Decisions Made:**

1. **Architecture Pattern - 4-Layer System:**
   - **HOUSE Layer**: ESP32 with MicroPython (sensors/actuators)
   - **DATABASE Layer**: Supabase PostgreSQL (persistence)
   - **API Layer**: C# ASP.NET Core 9.0 (read endpoints, MVC pattern)
   - **WEB Layer**: Next.js dashboard (frontend, MQTT client)
   - **MQTT Broker**: HiveMQ Cloud (real-time message routing)

2. **Data Flow Patterns:**
   - **Persistence**: ESP32 → Supabase (direct HTTPS POST for data logging)
   - **Real-time updates**: ESP32 → HiveMQ MQTT → Next.js (sensor broadcasts)
   - **Historical queries**: Next.js → C# API → Supabase (GET endpoints)
   - **Control commands**: Next.js → HiveMQ MQTT → ESP32 (actuator control)
   - **Key decision**: ESP32 writes directly to Supabase (not through C# API)

3. **C# API Requirement:**
   - Initially thought it was bonus (Phase 4)
   - **Corrected**: Required from start per teacher specs
   - Phase 2: C# API Layer (separate from Phase 3 Web)
   - Purpose: Read-only query interface between web app and database
   - Pattern: MVC with Controllers, Models, Contracts + Dependency Injection

4. **ESP32 Communication:**
   - Uses both MQTT (real-time) and HTTPS (persistence)
   - **MQTT Publishes**: Sensor data to `home/*` topics (temperature, humidity, motion, gas, etc.)
   - **MQTT Subscribes**: Control commands from `home/control/*` topics (door, window, fan)
   - **HTTPS POST**: Direct writes to Supabase tables (sensor_logs, rfid_scans, etc.)
   - Rationale: ESP32 owns its data, simpler than middleware

5. **File Organization:**
   - All planning docs in `planning/` folder
   - Database schema extracted to `database-schema.sql`
   - Architecture diagrams in dedicated `architecture.md`
   - PRD kept lean (~4 pages) with references to other docs

6. **Development Phases:**
   - Phase 1: ESP32 embedded system (sensors, MQTT, direct DB writes)
   - Phase 2: C# API (read endpoints, MVC pattern, Supabase client)
   - Phase 3: Next.js dashboard (frontend, MQTT client, API calls)
   - Phase 4: Bonus features (auth, user roles, PIR arm/disarm)

**Current Status:**
- Phase: Planning complete
- Next Task: T1.2 - Create Supabase project and database schema
- Hardware: Some sensor testing already done

**Git Status:**
- Branch: `planning` (documentation branch)
- Planning docs created and organized

**Next Steps:**
1. Set up Supabase project with schema from `database-schema.sql`
2. Create `embedded/config.py` with WiFi, MQTT, and Supabase credentials
3. Begin sensor module implementations (DHT11, PIR)

---

---

## Session 2 - October 7, 2025

### GitHub Project Setup & Planning Document Alignment ✅

**What was completed:**
- Created GitHub Project board: "smart-home-project"
- Created 9 GitHub issues (US1-US9) with task checkboxes for all functional requirements
- All issues added to project backlog column
- Reviewed and aligned planning documents (PRD, tasks.md, architecture.md)
- Fixed alignment issues in tasks.md

**Important Decisions Made:**

1. **Issue Granularity:**
   - Each User Story = 1 GitHub Issue (9 total)
   - Functional Requirements = Checkboxes within issue body
   - Rationale: Provides progress tracking without board clutter (GitHub shows checkbox completion %)
   - Alternative considered: Each FR as separate issue (rejected - too granular for solo project)

2. **Branching Strategy (Updated October 8, 2025):**
   - `main` - Clean baseline, all planning and cleanup merged
   - `phase-1-embedded-core` - ESP32 implementation (current development)
   - `phase-2-api-layer` - C# API (future)
   - `phase-3-web-dashboard` - Next.js frontend (future)
   - Rationale: Phase-based branches align with development milestones and tech stacks
   - Legacy branches (`planning`, `001-comprehensive-smart-home`) merged and can be deleted

3. **Issue Closure Workflow:**
   - Use commit message keywords: `Closes #N`, `Fixes #N`, `Resolves #N`
   - Issues auto-close when commits merge to `main` branch
   - Move issues across project board manually during development (Backlog → In Progress → Done)
   - Reference issues in commits: `Implements #N` for work-in-progress

4. **Document Alignment Fixes:**
   - Updated tasks.md: ASP.NET Core 8 → 9.0 (matches PRD requirement)
   - Updated tasks.md: Npgsql → Supabase NuGet package (matches architecture pattern)
   - Fixed Phase 4 milestone numbering: 3.3, 3.4 → 4.2, 4.3 (consistency)
   - Fixed Phase 4 task numbering: T3.5-T3.10 → T4.2-T4.7 (no conflicts)

**GitHub Issues Created:**
- Issue #2: US1 - Time-Based Lighting (3 FRs, Phase 1, HOUSE)
- Issue #3: US2 - Motion Detection & Response (3 FRs, Phase 1, HOUSE + DATABASE)
- Issue #4: US3 - Steam Detection & Window Control (3 FRs, Phase 1, HOUSE)
- Issue #5: US4 - Gas Detection & Emergency Response (4 FRs, Phase 1, HOUSE + DATABASE)
- Issue #6: US5 - RFID Access Control (5 FRs, Phase 1, HOUSE + DATABASE)
- Issue #7: US6 - Environmental Monitoring (4 FRs, Phase 1, HOUSE + WEB + DATABASE)
- Issue #8: US7 - Asthma Alert System (3 FRs, Phase 1, HOUSE + WEB)
- Issue #9: US8 - Real-Time System Monitoring (5 FRs, Phase 3, WEB)
- Issue #10: US9 - Remote Control (4 FRs, Phase 3, WEB + HOUSE)

**Current Status:**
- Phase: Planning complete, ready for Phase 1 implementation
- GitHub Project: Set up with 9 issues in Backlog
- Documentation: All planning docs aligned and consistent
- Next Task: T1.2 - Create Supabase project and database schema

**Git Status:**
- Branch: `planning` (current session)
- Planning docs updated and aligned
- Ready to switch to `001-comprehensive-smart-home` for implementation

**Next Steps:**
1. Switch to `001-comprehensive-smart-home` branch
2. Create Supabase project with schema from `database-schema.sql`
3. Set up MQTT credentials (HiveMQ Cloud)
4. Create `embedded/config.py` with WiFi, MQTT, and Supabase credentials
5. Begin sensor module implementations (T1.5-T1.9)
6. Move GitHub issue #7 (US6: Environmental Monitoring) to "In Progress" when starting DHT11 work

---

## Session 3 - October 8, 2025

### Repository Cleanup & Phase 1 Preparation ✅

**What was completed:**
- Reorganized repository structure to match architecture.md
- Created ESP32 deployment workflow with `/deploy` slash command
- Updated branch strategy to phase-based development

**Important Decisions Made:**

1. **Repository Structure Cleanup:**
   - Moved `src/` → `embedded/` to match file-structure.md
   - Moved `tests/hardware/` → `embedded/tests/` (layer-based testing)
   - Organized `Docs/` into subdirectories: reference-code/, libraries/, manuals/, tools/
   - Removed obsolete directories: `.specify/`, `specs/001-comprehensive-smart-home/`
   - Rationale: Clean structure before starting Phase 1, matches planned architecture

2. **Dependencies & Requirements:**
   - Updated `requirements.txt` to reflect actual desktop Python tools
   - `mpremote==1.26.1`, `pyserial==3.5`, `platformdirs==4.4.0`
   - Clarified: Desktop Python (venv) vs MicroPython (ESP32 libraries in Docs/)

3. **ESP32 Deployment Workflow:**
   - Created `deploy.py` script at root level
   - Uses `mpremote` to upload `embedded/*` to ESP32
   - Added `/deploy` slash command for easy deployment from Claude
   - Device target: `/dev/tty.usbserial-10`

4. **Branch Strategy Update:**
   - **New approach**: Phase-based branches (`phase-1-embedded-core`, etc.)
   - **Old approach**: Single implementation branch (`001-comprehensive-smart-home`)
   - Rationale: Clear separation between phases, aligns with project milestones
   - Merged legacy branches to `main` for clean baseline

**Documentation Updates:**
- `file-structure.md`: Added `embedded/tests/`, `Docs/` structure, deployment workflow
- `requirements.txt`: Accurate desktop Python dependencies
- `CLAUDE.md`: Updated branch strategy
- `development-notes.md`: Documented new branching approach

**Git Operations:**
- Committed: "Reorganize repository structure for Phase 1 development"
- Committed: "Add ESP32 deployment workflow"
- Pushed both commits to `main` branch
- **Current branch**: `main` (ready to create `phase-1-embedded-core`)

**Current Status:**
- Phase: Ready for Phase 1 implementation
- Next Task: T1.2 - Create Supabase project and database schema
- Repository: Clean, organized, documented

**Next Steps:**
1. Create `phase-1-embedded-core` branch from `main`
2. Run `/continue` to start Phase 1 workflow
3. Set up Supabase project with `database-schema.sql`
4. Create `embedded/config.py` with credentials
5. Begin sensor module implementations

---

## Session Template (for future sessions)

### Session X - [Date]

**Phase:** [Phase Name]

**What was completed:**
- Task list

**Important Decisions Made:**
- Decision 1
- Decision 2

**Blockers/Issues:**
- Any problems encountered

**Current Branch:** [branch name]

**Next Steps:** [What to tackle next]
