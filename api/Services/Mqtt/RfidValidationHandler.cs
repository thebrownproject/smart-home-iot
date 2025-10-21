using System.Text.Json;
using api.models;

namespace api.services.mqtt;

/// <summary>
/// Handles RFID validation requests from ESP32 devices.
/// Pattern: devices/{deviceId}/rfid/check
/// </summary>
public class RfidValidationHandler : IMqttMessageHandler
{
    private readonly IServiceScopeFactory _scopeFactory;
    private readonly MqttPublisher _mqttPublisher;

    public RfidValidationHandler(
        IServiceScopeFactory scopeFactory,
        MqttPublisher mqttPublisher)
    {
        _scopeFactory = scopeFactory;
        _mqttPublisher = mqttPublisher;
    }

    public bool CanHandle(string topic)
    {
        return topic.Contains("/rfid/check");
    }

    public async Task HandleAsync(string topic, string payload)
    {
        // Extract device ID from topic (e.g., "devices/esp32_main/rfid/check" → "esp32_main")
        var deviceId = topic.Split('/')[1];

        // Parse JSON payload
        var data = JsonSerializer.Deserialize<Dictionary<string, JsonElement>>(payload);
        var cardId = data?["card_id"].GetString();

        // Validate card against database
        using var scope = _scopeFactory.CreateScope();
        var cardService = scope.ServiceProvider.GetRequiredService<CardLookupService>();
        var supabase = scope.ServiceProvider.GetRequiredService<Supabase.Client>();

        bool isValid = await cardService.IsCardValidAsync(cardId!);

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

        // Log scan to database
        var rfidScan = new RfidScansModel
        {
            Id = Guid.NewGuid(),
            CardId = cardId!,
            AccessResult = isValid ? "granted" : "denied",
            AuthorisedCardId = isValid ? (await cardService.GetByCardIdAsync(cardId!))?.Id : null,
            Timestamp = DateTimeOffset.UtcNow
        };
        await supabase.From<RfidScansModel>().Insert(rfidScan);
    }
}
