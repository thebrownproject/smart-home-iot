using System.Text.Json;
using Microsoft.Extensions.Logging;
using api.models;

namespace api.services.mqtt;

/// <summary>
/// Handles sensor data from ESP32 devices (temperature, humidity, and motion).
/// Pattern: devices/{deviceId}/data
///
/// Temperature/Humidity: Stores latest readings in memory for the SensorDataWriter to write to database every 30 minutes.
/// Motion: Writes immediately to database as events occur.
/// </summary>
public class SensorDataHandler : IMqttMessageHandler
{
    private readonly object _lockObject = new object();
    private readonly ILogger<SensorDataHandler> _logger;
    private readonly IServiceScopeFactory _scopeFactory;
    private readonly IConfiguration _configuration;
    private SensorDataMessage? _latestTemperature;
    private SensorDataMessage? _latestHumidity;

    // DHT11 sensor valid ranges
    private const double MinTemperature = -20.0;
    private const double MaxTemperature = 60.0;
    private const double MinHumidity = 0.0;
    private const double MaxHumidity = 100.0;

    public SensorDataHandler(
        ILogger<SensorDataHandler> logger,
        IServiceScopeFactory scopeFactory,
        IConfiguration configuration)
    {
        _logger = logger;
        _scopeFactory = scopeFactory;
        _configuration = configuration;
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

        // Handle motion events - write immediately to database
        if (data.sensor_type == "motion")
        {
            return WriteMotionEventAsync(data);
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

    /// <summary>
    /// Writes motion detection event immediately to database
    /// </summary>
    private async Task WriteMotionEventAsync(SensorDataMessage motionData)
    {
        try
        {
            // Parse device UUID from configuration
            var deviceUuidString = _configuration.GetValue<string>("DeviceUuid");
            if (!Guid.TryParse(deviceUuidString, out var deviceId))
            {
                _logger.LogWarning("Invalid DeviceUuid configuration for motion event");
                return;
            }

            // Parse timestamp
            if (!DateTimeOffset.TryParse(motionData.timestamp, out var timestamp))
            {
                _logger.LogWarning("Invalid timestamp in motion data: {Timestamp}", motionData.timestamp);
                return;
            }

            // Only write motion detection events (detected=true)
            bool isMotionDetected = motionData.detected ?? false;

            if (!isMotionDetected)
            {
                return; // Don't log "no motion" events
            }

            // Write to database
            using var scope = _scopeFactory.CreateScope();
            var supabase = scope.ServiceProvider.GetRequiredService<Supabase.Client>();

            var motionLog = new SensorLogModel
            {
                Id = Guid.NewGuid(),
                DeviceId = deviceId,
                SensorType = "motion",
                Value = 1, // Motion detected = 1
                Timestamp = timestamp
            };

            await supabase.From<SensorLogModel>().Insert(motionLog);
            _logger.LogInformation("Motion event written to database at {Timestamp}", timestamp);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error writing motion event to database");
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
    public bool? detected { get; set; }  // For motion/gas sensors
    public string unit { get; set; } = string.Empty;
    public string timestamp { get; set; } = string.Empty;
}