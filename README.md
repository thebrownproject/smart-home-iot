# Zap Smart Home

![Status](https://img.shields.io/badge/status-production-green)
![Python](https://img.shields.io/badge/MicroPython-2B2728?logo=micropython&logoColor=white)
![C#](https://img.shields.io/badge/C%23-239120?logo=csharp&logoColor=white)
![.NET](https://img.shields.io/badge/.NET-512BD4?logo=dotnet&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?logo=nextdotjs&logoColor=white)
![MQTT](https://img.shields.io/badge/MQTT-660066?logo=mqtt&logoColor=white)

> Distributed IoT system connecting ESP32 microcontroller with multiple sensors and web dashboard via RESTful API and MQTT

🔗 **Live Demo:** [zap-smart-home.vercel.app](https://zap-smart-home.vercel.app/)

---

## Overview

A comprehensive IoT smart home automation system built for Cert IV capstone project, demonstrating distributed system architecture with ESP32 microcontroller, cloud messaging, and full-stack web development. The system monitors environmental conditions (temperature, humidity), manages security through RFID access control and motion detection, responds to emergencies (gas/steam detection), and provides real-time web monitoring with remote control capabilities. Extensive project planning preceded implementation, including PRD creation, system architecture design, MQTT topic structure definition, database schema modeling, and phased task breakdown.

---

## Tech Stack

**Embedded System:** ESP32 · MicroPython · KS5009 Smart Home Kit <br>
**Sensors:** DHT11 (temperature/humidity) · PIR (motion) · Gas/Flame · Steam/Moisture · RFID (RC522) <br>
**Outputs:** RGB LED (SK6812) · Servo Motors · Fan · Buzzer · OLED Display (SSD1306) <br>
**Backend:** ASP.NET Core 9.0 · C# 12 · RESTful API · Swagger/OpenAPI <br>
**Frontend:** Next.js 15 · TypeScript · TailwindCSS (planned) <br>
**Infrastructure:** MQTT (HiveMQ) · Supabase (PostgreSQL) · WiFi

---

## Features

- Environmental monitoring with DHT11 sensor displaying temperature and humidity on OLED display
- Object-oriented MicroPython architecture with handler classes for sensors, outputs, and communication
- RFID access control system with two-stage validation flow through C# middleware
- Motion detection with PIR sensor triggering visual indicators and database logging
- Emergency response system for gas and steam detection with automatic fan activation and window control
- MQTT-based distributed communication architecture with publish/subscribe patterns
- C# RESTful API middleware acting as single database gateway for security and business logic
- Real-time data streaming to web dashboard via MQTT subscriptions
- Remote control interface for door, window, and fan operation from web application
- State machine implementation for event prioritization (gas alert > steam > motion > idle)
- Asthma alert system monitoring temperature and humidity thresholds

---

## Architecture & Tech Decisions

**Built using distributed IoT architecture with three-tier communication pattern:**

**Communication Flow:**
- ESP32 publishes sensor data to HiveMQ MQTT broker
- C# middleware subscribes to device messages for validation and database persistence
- Next.js web app queries C# API for historical data and subscribes to MQTT for direct ESP32 status updates

**ESP32 Communication Strategy:**
- MQTT-only communication to avoid memory leaks from MicroPython's urequests library
- Persistent connection with automatic reconnection logic
- Publishes status updates (door/window state, temperature, humidity) to MQTT topics
- Web app subscribes to these status topics for real-time updates

**Direct ESP32-to-Web Communication:**
- ESP32 publishes current temperature/humidity to MQTT topics
- ESP32 publishes door/window status updates to MQTT topics
- Web app subscribes to these MQTT topics and updates React state
- Historical data accessed via C# API queries to database

**C# Middleware Gateway:**
- Single database gateway to centralise Supabase credentials and business logic
- Provides RESTful endpoints for historical queries
- Handles all database writes via MQTT subscriptions
- Implements business logic and data validation

**RFID Validation Pattern:**
- Request/response pattern via MQTT topics
- ESP32 publishes card UID to `devices/{id}/rfid/check`
- C# queries authorized cards table in database
- C# publishes validation result back to `devices/{id}/rfid/response`
- ESP32 receives response and controls door access

**MicroPython Architecture:**
- Object-oriented structure with handler classes
- Separate handlers for environmental monitoring, security, and outputs
- Clean separation of concerns for testability
- Lazy-loading pattern for memory efficiency (100KB RAM constraint)

**Event Priority State Machine:**
- Gas alert (highest priority) - activates fan, RGB solid red
- Steam alert - closes window, RGB flashes blue
- Motion alert - visual indicator, RGB orange
- Normal operation - standard monitoring cycle
- Critical alerts override lower-priority events

---

## Deployment & CI/CD

**Production infrastructure deployed with automated CI/CD pipelines for both API and web applications:**

**API Deployment (DigitalOcean VPS):**
- Hosted on DigitalOcean droplet with Docker containerization
- Automatic deployment via GitHub Actions when `/api` folder is updated
- Dynamic DNS resolution through DuckDNS (`zap-smart-home.duckdns.org`)
- Container runs on port 8080, exposed on host port 5000
- Environment variables managed through GitHub Secrets
- Health monitoring with container status checks and log streaming

**Web Deployment (Vercel):**
- Automatic deployment to [zap-smart-home.vercel.app](https://zap-smart-home.vercel.app/)
- Triggers on every push to `web/` folder
- Environment variables configured through Vercel dashboard
- Global CDN for fast worldwide access

**CI/CD Pipeline:**
- GitHub Actions workflow deploys API to DigitalOcean VPS on push to main branch
- Uses SSH/SCP actions to copy files and execute remote deployment scripts
- Docker Compose handles container orchestration with health checks
- Web app auto-deploys through Vercel's GitHub integration
- Both pipelines maintain zero-downtime deployments with rolling updates

---

## Project Planning

**Comprehensive planning documentation created before implementation:**

**Product Requirements Document (PRD):**
- Defined 9 user stories with detailed functional requirements
- Established tech stack for embedded, API, and web layers
- Documented code philosophy emphasizing robust embedded patterns
- Created success criteria aligned with assessment rubric

**System Architecture:**
- Designed full data flow diagram showing ESP32 → MQTT → C# → Supabase → Next.js
- Documented 5 message flow patterns (sensor persistence, real-time updates, historical queries, RFID validation, remote control)
- Specified MQTT topic structure with wildcard subscriptions for scalability
- Defined REST API endpoints for Sensors, RFID, Motion, Gas, and Status controllers

**Database Schema:**
- Modelled 7 PostgreSQL tables (sensor_logs, rfid_scans, motion_events, gas_alerts, device_status, authorized_cards, users)
- Designed relationships and constraints for data integrity
- Planned indexes for timestamp-based queries

**Task Breakdown:**
- Created phased development roadmap (Phase 1: Embedded, Phase 2: API, Phase 3: Web, Phase 4: Bonus)
- Defined granular tasks with dependencies and completion tracking
- Established milestones for each development phase

**File Structure:**
- Pre-planned directory organization for esp32/, api/, and web/ components
- Designed module separation for sensors, outputs, handlers, and communication layers

---

## Learnings & Challenges

**Key Learnings:**
- Architecting distributed IoT systems with MQTT publish/subscribe messaging patterns
- Object-oriented programming in MicroPython with handler classes for embedded system organization
- Designing RESTful API middleware with ASP.NET Core for IoT device communication
- Creating comprehensive project documentation (PRD, architecture diagrams, ERDs) before implementation
- Managing constrained hardware resources on ESP32 with non-blocking patterns and memory-conscious code

**Challenges Overcome:**
- Avoiding MicroPython urequests memory leaks by implementing MQTT-only communication strategy
- Designing secure RFID validation flow where ESP32 has no database credentials
- Implementing event priority state machine to handle competing sensor inputs
- Balancing real-time responsiveness with 30-minute database logging intervals
- Planning MQTT topic structure for single-device prototype with multi-device scalability

