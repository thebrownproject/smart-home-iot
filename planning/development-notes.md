# Development Notes

A running diary of development decisions, important context, and session-to-session notes.

---

## Session 1 - October 7, 2025

### Project Planning & Architecture ✅

**What was completed:**
- Created planning documents: `prd.md`, `tasks.md`, `architecture.md`, `database-schema.sql`
- Defined system architecture with corrected data flows
- Established 3-phase development approach
- Created `/continue` slash command for session resumption

**Important Decisions Made:**

1. **Architecture Pattern (Corrected):**
   - ESP32 → Supabase (direct HTTP POST for persistence)
   - ESP32 → MQTT → Next.js (for real-time updates)
   - Next.js → C# API → Supabase (for historical data queries)
   - C# API is **read-only** query layer (not MQTT subscriber)

2. **C# API Requirement:**
   - Initially thought it was bonus (Phase 3)
   - **Corrected**: Required from start per teacher specs
   - Moved to Phase 2 alongside Next.js web app
   - Purpose: Query interface between web app and database

3. **ESP32 Communication:**
   - Uses both MQTT (real-time) and HTTP (persistence)
   - MQTT for: sensor broadcasts, receiving control commands
   - HTTP for: direct database writes to Supabase
   - Rationale: ESP32 owns its data, simpler than middleware

4. **File Organization:**
   - All planning docs in `planning/` folder
   - Database schema extracted to `database-schema.sql`
   - Architecture diagrams in dedicated `architecture.md`
   - PRD kept lean (~4 pages) with references to other docs

5. **Development Phases:**
   - Phase 1: ESP32 embedded system (sensors, MQTT, direct DB writes)
   - Phase 2: C# API (read endpoints, MVC pattern)
   - Phase 3: Next.js dashboard (frontend, MQTT client)
   - Phase 4: Bonus features (auth, user roles, PIR arm/disarm)

**Current Status:**
- Phase: Planning complete
- Next Task: T1.2 - Create Supabase project and database schema
- Hardware: Some sensor testing already done

**Git Status:**
- Branch: `001-comprehensive-smart-home`
- Planning docs created

**Next Steps:**
1. Set up Supabase project with schema from `database-schema.sql`
2. Create `embedded/config.py` with MQTT + Supabase credentials
3. Begin sensor module implementations (DHT11, PIR)

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
