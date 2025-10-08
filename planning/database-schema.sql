-- Smart Home IoT Database Schema
-- Supabase PostgreSQL

-- Sensor readings (temperature, humidity, etc.)
CREATE TABLE sensor_logs (
  id BIGSERIAL PRIMARY KEY,
  sensor_type VARCHAR(50) NOT NULL,  -- 'temperature', 'humidity', 'gas', 'steam'
  value DECIMAL(10,2),
  unit VARCHAR(10),                  -- 'C', '%', etc.
  timestamp TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_sensor_type_timestamp ON sensor_logs(sensor_type, timestamp DESC);

-- RFID access control
CREATE TABLE rfid_scans (
  id BIGSERIAL PRIMARY KEY,
  card_id VARCHAR(100) NOT NULL,
  access_result VARCHAR(20) NOT NULL,  -- 'granted', 'denied'
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  user_name VARCHAR(100)               -- NULL for unknown cards
);

CREATE INDEX idx_rfid_timestamp ON rfid_scans(timestamp DESC);
CREATE INDEX idx_rfid_result ON rfid_scans(access_result);

-- Motion detection events
CREATE TABLE motion_events (
  id BIGSERIAL PRIMARY KEY,
  detected BOOLEAN NOT NULL,
  timestamp TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_motion_timestamp ON motion_events(timestamp DESC);

-- Gas/flame alerts with duration tracking
CREATE TABLE gas_alerts (
  id BIGSERIAL PRIMARY KEY,
  sensor_value INTEGER NOT NULL,
  alert_start TIMESTAMPTZ DEFAULT NOW(),
  alert_end TIMESTAMPTZ,               -- NULL while alert active
  fan_activated BOOLEAN DEFAULT false
);

CREATE INDEX idx_gas_alert_start ON gas_alerts(alert_start DESC);

-- Bonus: User accounts for authentication
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  username VARCHAR(100) NOT NULL UNIQUE,
  email VARCHAR(255) NOT NULL UNIQUE,
  role VARCHAR(20) NOT NULL,           -- 'parent', 'child'
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Bonus: Authorized RFID cards
CREATE TABLE authorized_cards (
  id BIGSERIAL PRIMARY KEY,
  card_id VARCHAR(100) NOT NULL UNIQUE,
  user_id BIGINT REFERENCES users(id),
  card_name VARCHAR(100),              -- e.g., "Front Door Card"
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
