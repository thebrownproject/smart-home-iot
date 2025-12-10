using System.Text.Json;
using Microsoft.Extensions.Logging;
using api.models;

namespace api.services.mqtt;

/// <summary>
/// Handles gas detection events from ESP32 devices.
/// Pattern: devices/{deviceId}/data (sensor_type='gas')
///
/// Gas detected: Creates new alert with alert_start=NOW(), alert_end=NULL
/// Gas cleared: Updates most recent alert SET alert_end=NOW()
/// </summary>
public class GasAlertHandler : IMqttMessageHandler
{
    private readonly ILogger<GasAlertHandler> _logger;
    private readonly IServiceScopeFactory _scopeFactory;
    private readonly IConfiguration _configuration;

    public GasAlertHandler(
        ILogger<GasAlertHandler> logger,
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

    public async Task HandleAsync(string topic, string payload)
    {
        // Parse JSON with error handling
        SensorDataMessage? data;
        try
        {
            data = JsonSerializer.Deserialize<SensorDataMessage>(payload);
        }
        catch (JsonException ex)
        {
            _logger.LogWarning(ex, "Failed to parse gas sensor data payload: {Payload}", payload);
            return;
        }

        if (data == null || data.sensor_type != "gas")
        {
            return; // Not a gas sensor message
        }

        // Validate detected field exists
        if (!data.detected.HasValue)
        {
            _logger.LogWarning("Gas sensor data missing 'detected' field: {Payload}", payload);
            return;
        }

        // Parse device UUID
        var deviceUuidString = _configuration.GetValue<string>("DeviceUuid");
        if (!Guid.TryParse(deviceUuidString, out var deviceId))
        {
            _logger.LogWarning("Invalid DeviceUuid configuration for gas alert");
            return;
        }

        // Parse timestamp
        if (!DateTimeOffset.TryParse(data.timestamp, out var timestamp))
        {
            _logger.LogWarning("Invalid timestamp in gas data: {Timestamp}", data.timestamp);
            return;
        }

        using var scope = _scopeFactory.CreateScope();
        var supabase = scope.ServiceProvider.GetRequiredService<Supabase.Client>();

        if (data.detected.Value)
        {
            // Gas detected - create new alert
            await CreateGasAlertAsync(supabase, deviceId, (int)data.value, timestamp);
        }
        else
        {
            // Gas cleared - close existing alert
            await CloseGasAlertAsync(supabase, deviceId, timestamp);
        }
    }

    /// <summary>
    /// Creates a new gas alert with alert_end = NULL (active alert)
    /// </summary>
    private async Task CreateGasAlertAsync(Supabase.Client supabase, Guid deviceId, int sensorValue, DateTimeOffset timestamp)
    {
        try
        {
            var gasAlert = new GasAlertsModel
            {
                Id = Guid.NewGuid(),
                DeviceId = deviceId,
                SensorValue = sensorValue,
                AlertStart = timestamp,
                AlertEnd = null  // Active alert
            };

            await supabase.From<GasAlertsModel>().Insert(gasAlert);
            _logger.LogWarning("🔥 Gas alert STARTED - Device: {DeviceId}, Value: {SensorValue}, Time: {Timestamp}",
                deviceId, sensorValue, timestamp);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error creating gas alert");
        }
    }

    /// <summary>
    /// Closes the most recent active gas alert by setting alert_end = NOW()
    /// </summary>
    private async Task CloseGasAlertAsync(Supabase.Client supabase, Guid deviceId, DateTimeOffset timestamp)
    {
        try
        {
            // Find most recent active alert (alert_end IS NULL)
            var activeAlerts = await supabase
                .From<GasAlertsModel>()
                .Where(x => x.DeviceId == deviceId && x.AlertEnd == null)
                .Order("alert_start", Supabase.Postgrest.Constants.Ordering.Descending)
                .Limit(1)
                .Get();

            var activeAlert = activeAlerts.Models.FirstOrDefault();

            if (activeAlert == null)
            {
                _logger.LogWarning("No active gas alert found to close for device {DeviceId}", deviceId);
                return;
            }

            // Update alert_end
            activeAlert.AlertEnd = timestamp;
            await supabase.From<GasAlertsModel>().Update(activeAlert);

            _logger.LogInformation("✅ Gas alert CLEARED - Device: {DeviceId}, Duration: {Duration}",
                deviceId, timestamp - activeAlert.AlertStart);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error closing gas alert");
        }
    }
}
