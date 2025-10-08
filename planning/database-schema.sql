-- Smart Home IoT Database Schema
-- Supabase PostgreSQL

-- Core entity: Physical devices (ESP32 microcontrollers)
CREATE TABLE devices (
  id BIGSERIAL PRIMARY KEY,
  device_type VARCHAR(50) NOT NULL,      -- 'esp32_main'
  device_name VARCHAR(100) NOT NULL,     -- 'Living Room Controller'
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- User accounts for authentication (Phase 4 bonus)
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  username VARCHAR(100) NOT NULL UNIQUE,
  email VARCHAR(255) NOT NULL UNIQUE,
  role VARCHAR(20) NOT NULL,             -- 'parent', 'child'
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Authorised RFID cards with user relationship (Phase 4 bonus)
CREATE TABLE authorised_cards (
  id BIGSERIAL PRIMARY KEY,
  card_id VARCHAR(100) NOT NULL UNIQUE,
  user_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Sensor readings (temperature, humidity, gas, steam)
CREATE TABLE sensor_logs (
  id BIGSERIAL PRIMARY KEY,
  device_id BIGINT REFERENCES devices(id) ON DELETE CASCADE,
  sensor_type VARCHAR(50) NOT NULL,      -- 'temperature', 'humidity', 'gas', 'steam'
  value DECIMAL(10,2),
  unit VARCHAR(10),                      -- 'C', '%', etc.
  timestamp TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_sensor_type_timestamp ON sensor_logs(sensor_type, timestamp DESC);
CREATE INDEX idx_sensor_device ON sensor_logs(device_id);

-- RFID access control scans
CREATE TABLE rfid_scans (
  id BIGSERIAL PRIMARY KEY,
  device_id BIGINT REFERENCES devices(id) ON DELETE CASCADE,
  card_id VARCHAR(100) NOT NULL,
  authorised_card_id BIGINT REFERENCES authorised_cards(id) ON DELETE SET NULL,
  access_result VARCHAR(20) NOT NULL,    -- 'granted', 'denied'
  timestamp TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_rfid_timestamp ON rfid_scans(timestamp DESC);
CREATE INDEX idx_rfid_result ON rfid_scans(access_result);
CREATE INDEX idx_rfid_card ON rfid_scans(authorised_card_id);

-- Motion detection events
CREATE TABLE motion_events (
  id BIGSERIAL PRIMARY KEY,
  device_id BIGINT REFERENCES devices(id) ON DELETE CASCADE,
  detected BOOLEAN NOT NULL,
  timestamp TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_motion_timestamp ON motion_events(timestamp DESC);
CREATE INDEX idx_motion_device ON motion_events(device_id);

-- Gas/flame alerts with duration tracking
CREATE TABLE gas_alerts (
  id BIGSERIAL PRIMARY KEY,
  device_id BIGINT REFERENCES devices(id) ON DELETE CASCADE,
  sensor_value INTEGER NOT NULL,
  alert_start TIMESTAMPTZ DEFAULT NOW(),
  alert_end TIMESTAMPTZ,                 -- NULL while alert active
  fan_activated BOOLEAN DEFAULT false
);

CREATE INDEX idx_gas_alert_start ON gas_alerts(alert_start DESC);
CREATE INDEX idx_gas_device ON gas_alerts(device_id);
