using System.Text.Json;
using api.models;
using Microsoft.Extensions.Logging;

namespace api.services.mqtt;

/// <summary>
/// Handles RFID validation requests from ESP32 devices.
/// Pattern: devices/{deviceId}/rfid/check
/// </summary>
public class RfidValidationHandler : IMqttMessageHandler
{
    private readonly IServiceScopeFactory _scopeFactory;
    private readonly MqttPublisher _mqttPublisher;
    private readonly ILogger<RfidValidationHandler> _logger;
    private readonly IConfiguration _configuration;

    public RfidValidationHandler(
        IServiceScopeFactory scopeFactory,
        MqttPublisher mqttPublisher,
        ILogger<RfidValidationHandler> logger,
        IConfiguration configuration)
    {
        _scopeFactory = scopeFactory;
        _mqttPublisher = mqttPublisher;
        _logger = logger;
        _configuration = configuration;
    }

    public bool CanHandle(string topic)
    {
        return topic.Contains("/rfid/check");
    }

    public async Task HandleAsync(string topic, string payload)
    {
        // Validate topic format: devices/{deviceId}/rfid/check
        var topicParts = topic.Split('/');
        if (topicParts.Length < 4)
        {
            _logger.LogWarning("Invalid RFID topic format: {Topic}", topic);
            return;
        }
        var deviceId = topicParts[1];

        // Parse and validate JSON payload
        Dictionary<string, JsonElement>? data;
        try
        {
            data = JsonSerializer.Deserialize<Dictionary<string, JsonElement>>(payload);
        }
        catch (JsonException ex)
        {
            _logger.LogWarning(ex, "Failed to parse RFID payload: {Payload}", payload);
            return;
        }

        // Validate card_id exists in payload
        if (data == null || !data.TryGetValue("card_id", out var cardIdElement))
        {
            _logger.LogWarning("RFID payload missing card_id: {Payload}", payload);
            return;
        }

        var cardId = cardIdElement.GetString();
        if (string.IsNullOrWhiteSpace(cardId))
        {
            _logger.LogWarning("RFID card_id is empty or null");
            return;
        }

        // Validate card against database
        using var scope = _scopeFactory.CreateScope();
        var cardService = scope.ServiceProvider.GetRequiredService<CardLookupService>();
        var supabase = scope.ServiceProvider.GetRequiredService<Supabase.Client>();

        bool isValid = await cardService.IsCardValidAsync(cardId);

        // Publish validation response back to ESP32
        var response = new
        {
            access = isValid ? "granted" : "denied",
            card_id = cardId,
            timestamp = DateTimeOffset.UtcNow.ToString("O")
        };

        var responseJson = JsonSerializer.Serialize(response);
        var responseTopic = $"devices/{deviceId}/rfid/response";
        await _mqttPublisher.PublishAsync(responseTopic, responseJson);

        _logger.LogInformation("RFID validation for card {CardId}: {Result}", cardId, isValid ? "granted" : "denied");

        // Log scan to database
        try
        {
            // Parse device UUID from configuration
            var deviceUuidString = _configuration.GetValue<string>("DeviceUuid");
            if (!Guid.TryParse(deviceUuidString, out var deviceUuid))
            {
                _logger.LogWarning("Invalid DeviceUuid configuration for RFID scan logging");
                return;
            }

            var rfidScan = new RfidScansModel
            {
                Id = Guid.NewGuid(),
                DeviceId = deviceUuid,
                CardId = cardId,
                AccessResult = isValid ? "granted" : "denied",
                AuthorisedCardId = isValid ? (await cardService.GetByCardIdAsync(cardId))?.Id : null,
                Timestamp = DateTimeOffset.UtcNow
            };
            await supabase.From<RfidScansModel>().Insert(rfidScan);
            _logger.LogInformation("RFID scan logged to database for card {CardId}", cardId);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to log RFID scan to database for card {CardId}", cardId);
        }
    }
}
