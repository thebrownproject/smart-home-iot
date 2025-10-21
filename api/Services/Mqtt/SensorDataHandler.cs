using System.Text.Json;

namespace api.services.mqtt;

/// <summary>
/// Handles sensor data from ESP32 devices (temperature and humidity).
/// Pattern: devices/{deviceId}/data
///
/// Stores latest readings in memory for the SensorDataWriter to write to database every 30 minutes.
/// </summary>
public class SensorDataHandler : IMqttMessageHandler
{
    private readonly object _lockObject = new object();
    private SensorDataMessage? _latestTemperature;
    private SensorDataMessage? _latestHumidity;

    public bool CanHandle(string topic)
    {
        return topic.Contains("/data");
    }

    public Task HandleAsync(string topic, string payload)
    {
        var data = JsonSerializer.Deserialize<SensorDataMessage>(payload);
        if (data == null) return Task.CompletedTask;

        lock (_lockObject)
        {
            if (data.sensor_type == "temperature")
                _latestTemperature = data;
            else if (data.sensor_type == "humidity")
                _latestHumidity = data;
        }

        return Task.CompletedTask;
    }

    public (SensorDataMessage? temperature, SensorDataMessage? humidity) GetLatestReadings()
    {
        lock (_lockObject)
        {
            return (_latestTemperature, _latestHumidity);
        }
    }
}

/// <summary>
/// Represents sensor data received from ESP32 via MQTT
/// </summary>
public class SensorDataMessage
{
    public string sensor_type { get; set; } = string.Empty;
    public double value { get; set; }
    public string unit { get; set; } = string.Empty;
    public string timestamp { get; set; } = string.Empty;
}