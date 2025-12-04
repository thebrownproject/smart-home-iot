using System.Text.Json;
using Microsoft.Extensions.Logging;

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
    private readonly ILogger<SensorDataHandler> _logger;
    private SensorDataMessage? _latestTemperature;
    private SensorDataMessage? _latestHumidity;

    // DHT11 sensor valid ranges
    private const double MinTemperature = -20.0;
    private const double MaxTemperature = 60.0;
    private const double MinHumidity = 0.0;
    private const double MaxHumidity = 100.0;

    public SensorDataHandler(ILogger<SensorDataHandler> logger)
    {
        _logger = logger;
    }

    public bool CanHandle(string topic)
    {
        return topic.Contains("/data");
    }

    public Task HandleAsync(string topic, string payload)
    {
        // Parse JSON with error handling
        SensorDataMessage? data;
        try
        {
            data = JsonSerializer.Deserialize<SensorDataMessage>(payload);
        }
        catch (JsonException ex)
        {
            _logger.LogWarning(ex, "Failed to parse sensor data payload: {Payload}", payload);
            return Task.CompletedTask;
        }

        if (data == null)
        {
            _logger.LogWarning("Sensor data deserialized to null: {Payload}", payload);
            return Task.CompletedTask;
        }

        // Validate sensor_type
        if (string.IsNullOrWhiteSpace(data.sensor_type))
        {
            _logger.LogWarning("Sensor data missing sensor_type: {Payload}", payload);
            return Task.CompletedTask;
        }

        // Validate sensor value is within DHT11 operating ranges
        if (data.sensor_type == "temperature" && (data.value < MinTemperature || data.value > MaxTemperature))
        {
            _logger.LogWarning("Temperature value {Value} out of range [{Min}-{Max}]",
                data.value, MinTemperature, MaxTemperature);
            return Task.CompletedTask;
        }

        if (data.sensor_type == "humidity" && (data.value < MinHumidity || data.value > MaxHumidity))
        {
            _logger.LogWarning("Humidity value {Value} out of range [{Min}-{Max}]",
                data.value, MinHumidity, MaxHumidity);
            return Task.CompletedTask;
        }

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