# Environment Setup Guide

This document covers environment variable configuration for all system layers.

---

## ESP32 (MicroPython)

**File**: `embedded/config.py`

**⚠️ Important**: This file contains secrets and is gitignored. Create it locally on your machine.

```python
# WiFi Configuration
WIFI_SSID = "your_network"
WIFI_PASSWORD = "your_password"

# MQTT Broker (HiveMQ Cloud)
MQTT_BROKER = "broker.hivemq.cloud"
MQTT_PORT = 8883  # SSL/TLS
MQTT_USER = "your_username"
MQTT_PASSWORD = "your_password"

# Supabase (Direct HTTP)
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_ANON_KEY = "your_anon_key"
```

**How to get credentials**:

1. **WiFi**: Your local network SSID and password
2. **HiveMQ**: Create free account at [console.hivemq.cloud](https://console.hivemq.cloud)
   - Create cluster → Access Management → Add credentials
3. **Supabase**: Project settings → API → Project URL and `anon` public key

**Deployment**:
- Upload `config.py` to ESP32 via MicroPico extension
- File stays on device, not in git repository

---

## C# API (ASP.NET Core)

### Base Configuration

**File**: `api/SmartHomeApi/appsettings.json` (committed to git, no secrets)

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*",
  "SupabaseUrl": "https://placeholder.supabase.co",
  "SupabaseApiKey": "placeholder_key",
  "UseSwagger": true,
  "Cors": {
    "AllowedOrigins": ["http://localhost:3000"]
  }
}
```

### Development Overrides

**File**: `api/SmartHomeApi/appsettings.Development.json` (gitignored)

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Debug"
    }
  },
  "SupabaseUrl": "https://your-project.supabase.co",
  "SupabaseApiKey": "your_anon_key"
}
```

**⚠️ Security**: Real credentials go in `appsettings.Development.json`, not the base file.

**Alternative: User Secrets** (Recommended for production)

```bash
cd api/SmartHomeApi
dotnet user-secrets init
dotnet user-secrets set "SupabaseUrl" "https://your-project.supabase.co"
dotnet user-secrets set "SupabaseApiKey" "your_anon_key"
```

**Accessing in code** (`Program.cs`):

```csharp
var supabaseUrl = builder.Configuration["SupabaseUrl"];
var supabaseKey = builder.Configuration["SupabaseApiKey"];
```

---

## Web App (Next.js)

**File**: `web/.env.local` (gitignored)

```bash
# C# API Backend
NEXT_PUBLIC_API_URL=http://localhost:5000

# MQTT Broker (HiveMQ Cloud)
NEXT_PUBLIC_MQTT_BROKER=wss://broker.hivemq.cloud:8884/mqtt
NEXT_PUBLIC_MQTT_USER=your_username
NEXT_PUBLIC_MQTT_PASSWORD=your_password
```

**Production** (when deploying to Vercel/Netlify):

```bash
# C# API Backend
NEXT_PUBLIC_API_URL=https://api.yourproject.com

# MQTT stays the same (HiveMQ Cloud endpoint)
NEXT_PUBLIC_MQTT_BROKER=wss://broker.hivemq.cloud:8884/mqtt
NEXT_PUBLIC_MQTT_USER=your_username
NEXT_PUBLIC_MQTT_PASSWORD=your_password
```

**⚠️ Security Note**: `NEXT_PUBLIC_*` variables are exposed to the browser. This is acceptable for:
- Public API URLs
- MQTT broker URLs (using SSL/TLS)
- MQTT credentials with limited permissions

For sensitive data (API keys, database secrets), use server-side environment variables (no `NEXT_PUBLIC_` prefix).

**Accessing in code**:

```typescript
// Client-side component
const apiUrl = process.env.NEXT_PUBLIC_API_URL;
const mqttBroker = process.env.NEXT_PUBLIC_MQTT_BROKER;
```

---

## Environment Variable Checklist

### ESP32 Setup
- [ ] Create `embedded/config.py` locally
- [ ] Add WiFi credentials
- [ ] Add HiveMQ MQTT credentials
- [ ] Add Supabase URL and anon key
- [ ] Upload to ESP32 (do not commit to git)

### C# API Setup
- [ ] Create `api/SmartHomeApi/appsettings.Development.json`
- [ ] Add Supabase URL and anon key
- [ ] Verify `.gitignore` excludes `appsettings.Development.json`
- [ ] Test with `dotnet run` (should connect to Supabase)

### Next.js Setup
- [ ] Create `web/.env.local`
- [ ] Add `NEXT_PUBLIC_API_URL` (http://localhost:5000 for dev)
- [ ] Add `NEXT_PUBLIC_MQTT_*` credentials
- [ ] Verify `.gitignore` excludes `.env.local`
- [ ] Test with `npm run dev`

---

## Security Best Practices

### ✅ Do:
- Use `.gitignore` for all credential files
- Use environment-specific configs (`Development.json`, `.env.local`)
- Rotate credentials if accidentally committed
- Use read-only database keys where possible (Supabase anon key is safe for public use with RLS)

### ❌ Don't:
- Commit credentials to git (even in private repos)
- Share `.env` files via Slack/email
- Use production credentials in development
- Hard-code credentials in source files

---

## Credential Sources

| Service | Where to Get Credentials |
|---------|--------------------------|
| **HiveMQ Cloud** | [console.hivemq.cloud](https://console.hivemq.cloud) → Access Management |
| **Supabase** | Project Settings → API → URL + `anon` key |
| **WiFi** | Your local network SSID/password |

---

## Troubleshooting

### ESP32 can't connect to WiFi
- Check SSID/password spelling (case-sensitive)
- Verify ESP32 supports 2.4GHz WiFi (not 5GHz)
- Check serial output: `print("WiFi connected:", network.isconnected())`

### C# API can't connect to Supabase
- Verify URL format: `https://your-project.supabase.co` (no trailing slash)
- Check anon key is correct (starts with `eyJ...`)
- Test with Postman: `GET https://your-project.supabase.co/rest/v1/sensor_logs`

### Next.js can't reach C# API
- Verify C# API is running: `curl http://localhost:5000/api/sensors/current`
- Check CORS settings in `appsettings.json` (must include `http://localhost:3000`)
- Clear browser cache/hard refresh

### MQTT connection fails
- Verify port: 8883 (SSL/TLS) not 1883 (plain)
- Check HiveMQ cluster is running (free tier hibernates after inactivity)
- Test with MQTT client (MQTT Explorer, mqttx)

---

## Quick Start

**First-time setup** (run once):

```bash
# 1. Create ESP32 config
cat > embedded/config.py << EOF
WIFI_SSID = "your_network"
WIFI_PASSWORD = "your_password"
MQTT_BROKER = "broker.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "your_username"
MQTT_PASSWORD = "your_password"
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_ANON_KEY = "your_anon_key"
EOF

# 2. Create C# API dev config
cat > api/SmartHomeApi/appsettings.Development.json << EOF
{
  "SupabaseUrl": "https://your-project.supabase.co",
  "SupabaseApiKey": "your_anon_key"
}
EOF

# 3. Create Next.js env
cat > web/.env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:5000
NEXT_PUBLIC_MQTT_BROKER=wss://broker.hivemq.cloud:8884/mqtt
NEXT_PUBLIC_MQTT_USER=your_username
NEXT_PUBLIC_MQTT_PASSWORD=your_password
EOF
```

**Verify** (all should be gitignored):

```bash
git status
# Should NOT show:
# - embedded/config.py
# - api/SmartHomeApi/appsettings.Development.json
# - web/.env.local
```

---

## Related Documentation

- **File structure**: `planning/file-structure.md`
- **Architecture**: `planning/architecture.md` (MQTT topics, data flow)
- **Database setup**: `planning/database-schema.sql`
