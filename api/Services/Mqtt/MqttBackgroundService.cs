using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using MQTTnet;
using System.Text;

namespace api.services.mqtt;

/// <summary>
/// MQTT Background Service - Manages connection to MQTT broker and routes messages to handlers.
/// Runs continuously in the background, independent of HTTP requests.
/// </summary>
public class MqttBackgroundService : IHostedService, IDisposable
{
    private readonly IConfiguration _configuration;
    private readonly IEnumerable<IMqttMessageHandler> _handlers;
    private readonly MqttPublisher _mqttPublisher;
    private readonly ILogger<MqttBackgroundService> _logger;
    private IMqttClient? _mqttClient;
    private Timer? _reconnectTimer;

    public MqttBackgroundService(
        IConfiguration configuration,
        IEnumerable<IMqttMessageHandler> handlers,
        MqttPublisher mqttPublisher,
        ILogger<MqttBackgroundService> logger)
    {
        _configuration = configuration;
        _handlers = handlers;
        _mqttPublisher = mqttPublisher;
        _logger = logger;
    }

    public async Task StartAsync(CancellationToken cancellationToken)
    {
        var factory = new MqttClientFactory();
        _mqttClient = factory.CreateMqttClient();

        _mqttClient.ApplicationMessageReceivedAsync += OnMessageReceivedAsync;
        _mqttClient.DisconnectedAsync += OnDisconnectedAsync;

        await ConnectAsync();
    }

    private async Task ConnectAsync()
    {
        var broker = _configuration.GetValue<string>("MqttBroker");
        var port = _configuration.GetValue<int>("MqttPort");
        var username = _configuration.GetValue<string>("MqttUser");
        var password = _configuration.GetValue<string>("MqttPassword");

        var options = new MqttClientOptionsBuilder()
            .WithTcpServer(broker, port)
            .WithCredentials(username, password)
            .WithClientId($"SmartHomeAPI_{Guid.NewGuid()}")
            .WithCleanSession()
            .WithTlsOptions(o =>
            {
                o.UseTls();
                // Accept all server certificates (required for HiveMQ Cloud)
                o.WithCertificateValidationHandler(_ => true);
            })
            .Build();

        await _mqttClient!.ConnectAsync(options);
        _logger.LogInformation("✅ Connected to MQTT broker: {Broker}:{Port}", broker, port);

        // Give the publisher access to the client
        _mqttPublisher.SetClient(_mqttClient);

        // Subscribe to all topics
        var subscribeOptions = new MqttClientSubscribeOptionsBuilder()
            .WithTopicFilter("devices/+/data")
            .WithTopicFilter("devices/+/rfid/check")
            .WithTopicFilter("devices/+/status/#")
            .Build();

        await _mqttClient.SubscribeAsync(subscribeOptions);
        _logger.LogInformation("📬 Subscribed to MQTT topics: devices/+/data, devices/+/rfid/check, devices/+/status/#");
    }

    private async Task OnMessageReceivedAsync(MqttApplicationMessageReceivedEventArgs e)
    {
        try
        {
            var topic = e.ApplicationMessage.Topic;
            var payload = Encoding.UTF8.GetString(e.ApplicationMessage.Payload);

            _logger.LogInformation("📨 MQTT Message Received - Topic: {Topic}, Payload: {Payload}", topic, payload);

            // Route message to ALL handlers that can process it
            var matchingHandlers = _handlers.Where(h => h.CanHandle(topic)).ToList();

            if (matchingHandlers.Count > 0)
            {
                foreach (var handler in matchingHandlers)
                {
                    _logger.LogInformation("🔄 Routing to handler: {HandlerType}", handler.GetType().Name);
                    await handler.HandleAsync(topic, payload);
                }
            }
            else
            {
                _logger.LogWarning("⚠️ No handler found for topic: {Topic}", topic);
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error processing MQTT message on topic {Topic}", e.ApplicationMessage.Topic);
        }
    }

    private Task OnDisconnectedAsync(MqttClientDisconnectedEventArgs e)
    {
        _reconnectTimer?.Dispose();
        _reconnectTimer = new Timer(async _ =>
        {
            try
            {
                await ConnectAsync();
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, "MQTT reconnection attempt failed, will retry in 5 seconds");
            }
        }, null, TimeSpan.FromSeconds(5), Timeout.InfiniteTimeSpan);

        return Task.CompletedTask;
    }

    public async Task StopAsync(CancellationToken cancellationToken)
    {
        if (_mqttClient != null && _mqttClient.IsConnected)
        {
            await _mqttClient.DisconnectAsync();
        }
    }

    public void Dispose()
    {
        _reconnectTimer?.Dispose();
        _mqttClient?.Dispose();
    }
}
