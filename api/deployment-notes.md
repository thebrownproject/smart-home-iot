# Deployment Notes

This file exists to help trigger the GitHub Actions workflow when needed.

## Last Deployment
- Date: 2025-12-11
- Fix: Corrected appsettings.Production.json structure
- Configuration: SupabaseUrl and SupabaseApiKey are now at root level
- MQTT: Updated from nested HiveMQ to flat MqttBroker/MqttUser structure
- Status: Fixed MQTT configuration causing null broker error