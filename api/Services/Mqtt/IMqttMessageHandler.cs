namespace api.services.mqtt;

/// <summary>
/// Interface for MQTT message handlers.
/// Each handler is responsible for processing a specific type of MQTT message.
/// This pattern follows the Single Responsibility Principle and Strategy Pattern.
/// </summary>
public interface IMqttMessageHandler
{
    /// <summary>
    /// Determines if this handler can process the given MQTT topic.
    /// </summary>
    /// <param name="topic">The MQTT topic (e.g., "devices/esp32_main/rfid/check")</param>
    /// <returns>True if this handler should process messages on this topic</returns>
    bool CanHandle(string topic);

    /// <summary>
    /// Process an MQTT message asynchronously.
    /// </summary>
    /// <param name="topic">The MQTT topic the message was received on</param>
    /// <param name="payload">The message payload (JSON string)</param>
    /// <returns>Task representing the async operation</returns>
    Task HandleAsync(string topic, string payload);
}
