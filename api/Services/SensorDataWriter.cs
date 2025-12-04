using api.models;
using api.services.mqtt;
using Microsoft.Extensions.Logging;

namespace api.services;

/// <summary>
/// Background service that writes sensor data to database every 30 minutes.
/// Retrieves latest readings from SensorDataHandler and persists to Supabase.
/// </summary>
public class SensorDataWriter : IHostedService, IDisposable
{
    private readonly IServiceScopeFactory _scopeFactory;
    private readonly IConfiguration _configuration;
    private readonly SensorDataHandler _sensorDataHandler;
    private readonly ILogger<SensorDataWriter> _logger;
    private Timer? _timer;

    public SensorDataWriter(
        IServiceScopeFactory scopeFactory,
        IConfiguration configuration,
        SensorDataHandler sensorDataHandler,
        ILogger<SensorDataWriter> logger)
    {
        _scopeFactory = scopeFactory;
        _configuration = configuration;
        _sensorDataHandler = sensorDataHandler;
        _logger = logger;
    }

    public Task StartAsync(CancellationToken cancellationToken)
    {
        // TODO: Change back to 30 minutes for production (currently 1 min for testing)
        _timer = new Timer(
            WriteSensorDataToDatabase,
            null,
            TimeSpan.FromMinutes(1),  // First write after 1 minute
            TimeSpan.FromMinutes(1)   // Repeat every 1 minute
        );

        return Task.CompletedTask;
    }

    private async void WriteSensorDataToDatabase(object? state)
    {
        try
        {
            var (temperature, humidity) = _sensorDataHandler.GetLatestReadings();

            if (temperature == null && humidity == null)
            {
                return;  // No data to write
            }

            using var scope = _scopeFactory.CreateScope();
            var supabase = scope.ServiceProvider.GetRequiredService<Supabase.Client>();

            var deviceUuidString = _configuration.GetValue<string>("DeviceUuid");
            if (!Guid.TryParse(deviceUuidString, out var deviceId))
            {
                return;  // Invalid device ID
            }

            if (temperature != null && DateTimeOffset.TryParse(temperature.timestamp, out var tempTimestamp))
            {
                var tempLog = new SensorLogModel
                {
                    Id = Guid.NewGuid(),
                    DeviceId = deviceId,
                    SensorType = "temperature",
                    Value = (decimal)temperature.value,
                    Timestamp = tempTimestamp
                };
                await supabase.From<SensorLogModel>().Insert(tempLog);
            }

            if (humidity != null && DateTimeOffset.TryParse(humidity.timestamp, out var humTimestamp))
            {
                var humidityLog = new SensorLogModel
                {
                    Id = Guid.NewGuid(),
                    DeviceId = deviceId,
                    SensorType = "humidity",
                    Value = (decimal)humidity.value,
                    Timestamp = humTimestamp
                };
                await supabase.From<SensorLogModel>().Insert(humidityLog);
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error writing sensor data to database");
        }
    }

    public Task StopAsync(CancellationToken cancellationToken)
    {
        _timer?.Dispose();
        return Task.CompletedTask;
    }

    public void Dispose()
    {
        _timer?.Dispose();
    }
}
