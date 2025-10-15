-- Drop child tables first (FK dependencies)
DROP TABLE IF EXISTS rfid_scans;
DROP TABLE IF EXISTS sensor_logs;
DROP TABLE IF EXISTS gas_alerts;
DROP TABLE IF EXISTS motion_events;

-- Then parents/lookups
DROP TABLE IF EXISTS authorised_cards;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS devices;

-- enable UUID generation
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE devices (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  device_code INT UNIQUE NOT NULL,
  device_name VARCHAR(100) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Optional (Phase 4): users, without role
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  username VARCHAR(100) NOT NULL UNIQUE,
  email VARCHAR(255) NOT NULL UNIQUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE authorised_cards (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  card_id VARCHAR(100) NOT NULL UNIQUE,
  user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE sensor_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  device_id UUID REFERENCES devices(id) ON DELETE CASCADE,
  sensor_type VARCHAR(50) NOT NULL,      -- 'temperature','humidity','gas','steam','motion'
  value DECIMAL(10,2),
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  CONSTRAINT chk_sensor_type CHECK (sensor_type IN ('temperature','humidity','gas','steam','motion')),
  CONSTRAINT chk_motion_value CHECK (sensor_type <> 'motion' OR value IN (0,1))
);

CREATE INDEX idx_sensor_type_timestamp ON sensor_logs(sensor_type, timestamp DESC);
CREATE INDEX idx_sensor_device ON sensor_logs(device_id);
CREATE INDEX idx_sensor_motion_ts ON sensor_logs(timestamp DESC) WHERE sensor_type = 'motion';

CREATE TABLE rfid_scans (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  device_id UUID REFERENCES devices(id) ON DELETE CASCADE,
  card_id VARCHAR(100) NOT NULL,
  authorised_card_id UUID REFERENCES authorised_cards(id) ON DELETE SET NULL,
  access_result VARCHAR(20) NOT NULL,
  timestamp TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_rfid_timestamp ON rfid_scans(timestamp DESC);
CREATE INDEX idx_rfid_result ON rfid_scans(access_result);
CREATE INDEX idx_rfid_card ON rfid_scans(authorised_card_id);

CREATE TABLE gas_alerts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  device_id UUID REFERENCES devices(id) ON DELETE CASCADE,
  sensor_value INTEGER NOT NULL,
  alert_start TIMESTAMPTZ DEFAULT NOW(),
  alert_end TIMESTAMPTZ
);
CREATE INDEX idx_gas_alert_start ON gas_alerts(alert_start DESC);
CREATE INDEX idx_gas_device ON gas_alerts(device_id);