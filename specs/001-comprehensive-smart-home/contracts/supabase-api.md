# Supabase API Contract: Smart Home Database Integration

**Branch**: `001-comprehensive-smart-home` | **Date**: 2025-09-17
**Database**: Supabase PostgreSQL with REST API

## API Base Configuration

### Connection Parameters
```python
SUPABASE_CONFIG = {
    "url": "https://your-project.supabase.co",
    "anon_key": "[ENV_VARIABLE]",  # Public anon key
    "service_key": "[ENV_VARIABLE]",  # Service role key for ESP32
    "timeout": 10,
    "retry_attempts": 3
}
```

### Authentication
- ESP32 uses service role key for write operations
- Public dashboard uses anon key with RLS policies
- API requests include Authorization header: `Bearer {key}`

## REST API Endpoints

### Environmental Readings

#### POST /rest/v1/environmental_readings
**Purpose**: Insert new sensor reading
**Authentication**: Service role key required
**Content-Type**: application/json

**Request Body**:
```json
{
  "sensor_type": "temperature",
  "value": 24.5,
  "unit": "celsius",
  "location": "indoor",
  "device_id": "ESP32_ABC123",
  "status": "normal"
}
```

**Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2025-09-17T10:30:00.123456Z",
  "sensor_type": "temperature",
  "value": 24.5,
  "unit": "celsius",
  "location": "indoor",
  "device_id": "ESP32_ABC123",
  "status": "normal"
}
```

**Error Response** (400 Bad Request):
```json
{
  "code": "22P02",
  "details": "invalid input syntax for type numeric",
  "hint": null,
  "message": "value must be a valid number"
}
```

#### GET /rest/v1/environmental_readings
**Purpose**: Retrieve sensor readings with filtering
**Authentication**: Anon key (with RLS)
**Query Parameters**:
- `device_id=eq.ESP32_ABC123`: Filter by device
- `sensor_type=eq.temperature`: Filter by sensor type
- `timestamp=gte.2025-09-17T00:00:00Z`: Filter by date range
- `order=timestamp.desc`: Sort by timestamp descending
- `limit=100`: Limit number of results

**Response** (200 OK):
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2025-09-17T10:30:00.123456Z",
    "sensor_type": "temperature",
    "value": 24.5,
    "unit": "celsius",
    "location": "indoor",
    "device_id": "ESP32_ABC123",
    "status": "normal"
  }
]
```

### Access Records

#### POST /rest/v1/access_records
**Purpose**: Log RFID access attempt
**Authentication**: Service role key required

**Request Body**:
```json
{
  "card_uid": "A1B2C3D4",
  "access_granted": true,
  "door_action": "unlock",
  "user_name": "John Doe",
  "device_id": "ESP32_ABC123",
  "location": "main_door"
}
```

**Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "timestamp": "2025-09-17T10:30:00.123456Z",
  "card_uid": "A1B2C3D4",
  "access_granted": true,
  "door_action": "unlock",
  "user_name": "John Doe",
  "device_id": "ESP32_ABC123",
  "location": "main_door"
}
```

#### GET /rest/v1/authorized_users
**Purpose**: Retrieve authorized RFID cards for validation
**Authentication**: Service role key required

**Query Parameters**:
- `active=eq.true`: Only active users
- `select=card_uid,user_name`: Select specific columns

**Response** (200 OK):
```json
[
  {
    "card_uid": "A1B2C3D4",
    "user_name": "John Doe"
  },
  {
    "card_uid": "E5F6G7H8",
    "user_name": "Jane Smith"
  }
]
```

### Security Events

#### POST /rest/v1/security_events
**Purpose**: Log security events (motion, PIR, manual overrides)
**Authentication**: Service role key required

**Request Body**:
```json
{
  "event_type": "motion",
  "severity": "info",
  "triggered_by": "motion_sensor_pin14",
  "response_actions": ["led_on", "fan_start"],
  "device_id": "ESP32_ABC123",
  "location": "living_room"
}
```

### Emergency Events

#### POST /rest/v1/emergency_events
**Purpose**: Log emergency events (gas detection, system failures)
**Authentication**: Service role key required

**Request Body**:
```json
{
  "emergency_type": "gas_detected",
  "severity_level": 5,
  "triggered_by": "gas_sensor_pin23",
  "response_sequence": ["open_doors", "open_windows", "activate_fan", "sound_alarm"],
  "device_id": "ESP32_ABC123"
}
```

#### PATCH /rest/v1/emergency_events
**Purpose**: Update emergency event (e.g., mark as resolved)
**Authentication**: Service role key required

**Query Parameters**: `id=eq.{emergency_id}`

**Request Body**:
```json
{
  "resolved_at": "2025-09-17T10:35:00.123456Z",
  "manual_disable": true
}
```

### System State Management

#### POST /rest/v1/system_state
**Purpose**: Insert/update current system state (upsert operation)
**Authentication**: Service role key required

**Request Body**:
```json
{
  "device_id": "ESP32_ABC123",
  "pir_enabled": true,
  "gas_alarm_active": false,
  "manual_overrides": {
    "gas_alarm": false,
    "pir_system": false
  },
  "device_status": {
    "temperature_sensor": "online",
    "motion_sensor": "online",
    "rfid_reader": "online",
    "gas_sensor": "online",
    "oled_display": "online"
  },
  "network_status": "connected",
  "last_heartbeat": "2025-09-17T10:30:00.123456Z"
}
```

## Row Level Security (RLS) Policies

### Environmental Readings
```sql
-- Read access for all authenticated users
CREATE POLICY "Allow read access to environmental readings" ON environmental_readings
FOR SELECT USING (true);

-- Write access only for service role
CREATE POLICY "Allow insert for service role" ON environmental_readings
FOR INSERT WITH CHECK (auth.role() = 'service_role');
```

### Access Records
```sql
-- Read access for authenticated users
CREATE POLICY "Allow read access to access records" ON access_records
FOR SELECT USING (auth.role() IS NOT NULL);

-- Write access only for service role
CREATE POLICY "Allow insert for service role" ON access_records
FOR INSERT WITH CHECK (auth.role() = 'service_role');
```

### Security Events
```sql
-- Read access for authenticated users
CREATE POLICY "Allow read access to security events" ON security_events
FOR SELECT USING (auth.role() IS NOT NULL);

-- Write/update access only for service role
CREATE POLICY "Allow insert for service role" ON security_events
FOR INSERT WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "Allow update for service role" ON security_events
FOR UPDATE USING (auth.role() = 'service_role');
```

## Batch Operations

### Bulk Insert Environmental Readings
**Endpoint**: POST /rest/v1/environmental_readings
**Content-Type**: application/json

**Request Body** (Array):
```json
[
  {
    "sensor_type": "temperature",
    "value": 24.5,
    "unit": "celsius",
    "device_id": "ESP32_ABC123"
  },
  {
    "sensor_type": "humidity",
    "value": 65.0,
    "unit": "percent",
    "device_id": "ESP32_ABC123"
  }
]
```

### Data Synchronization
ESP32 implements batch sync for network recovery:

```python
def sync_cached_data():
    """Sync locally cached data to Supabase during network recovery"""
    for table_name, cached_records in local_cache.items():
        if cached_records:
            response = supabase.table(table_name).insert(cached_records).execute()
            if response.status_code == 201:
                clear_local_cache(table_name)
            else:
                log_sync_error(table_name, response.error)
```

## Error Handling

### HTTP Status Codes
- **200 OK**: Successful GET request
- **201 Created**: Successful POST request
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Missing or invalid API key
- **403 Forbidden**: RLS policy violation
- **409 Conflict**: Unique constraint violation
- **422 Unprocessable Entity**: Validation error
- **500 Internal Server Error**: Database error

### Common Error Responses

#### Validation Error (422):
```json
{
  "code": "23514",
  "details": "Failing row contains (gas, -10, ppm, ...)",
  "hint": null,
  "message": "new row for relation \"environmental_readings\" violates check constraint"
}
```

#### Authentication Error (401):
```json
{
  "code": "PGRST301",
  "details": null,
  "hint": null,
  "message": "JWT expired"
}
```

### Retry Logic
```python
def api_call_with_retry(endpoint, data, max_retries=3):
    """API call with exponential backoff retry"""
    for attempt in range(max_retries):
        try:
            response = make_api_call(endpoint, data)
            if response.status_code < 500:
                return response
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(2 ** attempt)  # Exponential backoff
```

## Real-time Subscriptions

### WebSocket Connection (for dashboards)
```javascript
const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)

// Subscribe to environmental readings
const subscription = supabase
  .channel('environmental_readings')
  .on('postgres_changes',
    { event: 'INSERT', schema: 'public', table: 'environmental_readings' },
    (payload) => {
      console.log('New reading:', payload.new)
      updateDashboard(payload.new)
    }
  )
  .subscribe()
```

### Emergency Alert Subscriptions
```javascript
// Subscribe to emergency events for real-time alerts
const emergencySubscription = supabase
  .channel('emergency_events')
  .on('postgres_changes',
    { event: 'INSERT', schema: 'public', table: 'emergency_events' },
    (payload) => {
      if (payload.new.severity_level >= 4) {
        triggerEmergencyNotification(payload.new)
      }
    }
  )
  .subscribe()
```

## Performance Optimization

### Indexes
All critical indexes defined in data-model.md for optimal query performance.

### Connection Pooling
ESP32 reuses HTTP connections where possible:
```python
import urequests
session = urequests.Session()
session.headers.update({'Authorization': f'Bearer {service_key}'})
```

### Caching Strategy
- ESP32 caches authorized users list (updated hourly)
- Recent readings cached locally for dashboard queries
- Emergency events never cached (real-time priority)