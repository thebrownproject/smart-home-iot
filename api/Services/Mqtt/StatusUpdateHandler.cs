namespace api.services.mqtt;

/// <summary>
/// Handles device status updates (door, window, fan, LED).
/// Pattern: devices/{deviceId}/status/{output}
///
/// Currently just logs status changes - could be extended to track device state in future.
/// </summary>
public class StatusUpdateHandler : IMqttMessageHandler
{
    public bool CanHandle(string topic)
    {
        return topic.Contains("/status/");
    }

    public async Task HandleAsync(string topic, string payload)
    {
        // For now, just acknowledge receipt
        // Future: Could track device state in memory or log to database
        await Task.CompletedTask;
    }
}
