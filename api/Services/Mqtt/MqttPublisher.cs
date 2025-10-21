using MQTTnet;

namespace api.services.mqtt;

/// <summary>
/// Helper service for publishing MQTT messages.
/// Injected into message handlers that need to send responses.
/// </summary>
public class MqttPublisher
{
    private readonly ILogger<MqttPublisher> _logger;
    private IMqttClient? _mqttClient;

    public MqttPublisher(ILogger<MqttPublisher> logger)
    {
        _logger = logger;
    }

    /// <summary>
    /// Internal method called by MqttBackgroundService to set the client instance.
    /// Not exposed via interface to prevent external misuse.
    /// </summary>
    internal void SetClient(IMqttClient client)
    {
        _mqttClient = client;
    }

    /// <summary>
    /// Publish a message to an MQTT topic.
    /// </summary>
    /// <param name="topic">The MQTT topic to publish to</param>
    /// <param name="payload">The message payload (usually JSON)</param>
    public async Task PublishAsync(string topic, string payload)
    {
        if (_mqttClient == null || !_mqttClient.IsConnected)
        {
            _logger.LogWarning("⚠️ Cannot publish to {Topic} - MQTT client not connected", topic);
            return;
        }

        var message = new MqttApplicationMessageBuilder()
            .WithTopic(topic)
            .WithPayload(payload)
            .WithQualityOfServiceLevel(MQTTnet.Protocol.MqttQualityOfServiceLevel.AtLeastOnce)
            .WithRetainFlag(false)
            .Build();

        await _mqttClient.PublishAsync(message);
        _logger.LogDebug("📤 Published to {Topic}: {Payload}", topic, payload);
    }
}
