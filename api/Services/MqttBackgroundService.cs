using Microsoft.Extensions.Hosting;
using MQTTnet;
using System.Text;
using System.Text.Json;

namespace api.services;

/// <summary>
/// MQTT Background Service - The middleware bridge between ESP32 and Supabase.
/// Runs continuously in the background, independent of HTTP requests.
///
/// Architecture:
/// ESP32 → MQTT Publish → This Service Receives → Process → Write to Supabase
/// ESP32 ← MQTT Publish ← This Service Sends   ← Validation/Response
/// </summary>
public class MqttBackgroundService : IHostedService, IDisposable
{
    private readonly ILogger<MqttBackgroundService> _logger;
    private readonly IConfiguration _configuration;
    private readonly IServiceScopeFactory _scopeFactory;
    private IMqttClient? _mqttClient;
    private Timer? _reconnectTimer;

    // Constructor - injected by ASP.NET Core DI
    public MqttBackgroundService(
        ILogger<MqttBackgroundService> logger,
        IConfiguration configuration,
        IServiceScopeFactory scopeFactory)
    {
        _logger = logger;
        _configuration = configuration;
        _scopeFactory = scopeFactory; // Used to create scoped services in background thread
    }

    /// <summary>
    /// Called when the application starts.
    /// Sets up and connects the MQTT client.
    /// </summary>
    public async Task StartAsync(CancellationToken cancellationToken)
    {
        _logger.LogInformation("🚀 MQTT Background Service is starting...");

        try
        {
            // Create MQTT client instance
            var factory = new MqttClientFactory();
            _mqttClient = factory.CreateMqttClient();

            // Set up event handlers BEFORE connecting
            _mqttClient.ApplicationMessageReceivedAsync += OnMessageReceivedAsync;
            _mqttClient.DisconnectedAsync += OnDisconnectedAsync;
            _mqttClient.ConnectedAsync += OnConnectedAsync;

            // Connect to HiveMQ broker
            await ConnectAsync();

            _logger.LogInformation("✅ MQTT Background Service started successfully");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "❌ Failed to start MQTT Background Service");
            throw;
        }
    }

    /// <summary>
    /// Connects to the MQTT broker using credentials from appsettings.json
    /// </summary>
    private async Task ConnectAsync()
    {
        // Read MQTT configuration from appsettings.json
        var broker = _configuration.GetValue<string>("MqttBroker");
        var port = _configuration.GetValue<int>("MqttPort");
        var username = _configuration.GetValue<string>("MqttUser");
        var password = _configuration.GetValue<string>("MqttPassword");

        _logger.LogInformation($"📡 Connecting to MQTT broker: {broker}:{port}");

        // Build MQTT client options
        var optionsBuilder = new MqttClientOptionsBuilder()
            .WithTcpServer(broker, port)
            .WithCredentials(username, password)
            .WithClientId($"SmartHomeAPI_{Guid.NewGuid()}")
            .WithCleanSession();

        // Enable TLS for port 8883 with certificate validation
        // Note: For production, use proper certificate validation
        optionsBuilder.WithTlsOptions(o =>
        {
            o.UseTls();
            o.WithCertificateValidationHandler(_ => true); // Accept all certificates (dev only)
        });

        var options = optionsBuilder.Build();

        // Connect to broker
        var result = await _mqttClient!.ConnectAsync(options);

        if (result.ResultCode == MqttClientConnectResultCode.Success)
        {
            _logger.LogInformation("✅ Connected to MQTT broker successfully");
            await SubscribeToTopicsAsync();
        }
        else
        {
            _logger.LogError($"❌ Failed to connect to MQTT broker: {result.ResultCode}");
            throw new Exception($"MQTT connection failed: {result.ResultCode}");
        }
    }

    /// <summary>
    /// Subscribe to all required MQTT topics from ESP32 devices
    /// </summary>
    private async Task SubscribeToTopicsAsync()
    {
        _logger.LogInformation("📬 Subscribing to MQTT topics...");

        // Subscribe to multiple topics
        var subscribeOptions = new MqttClientSubscribeOptionsBuilder()
            .WithTopicFilter("devices/+/data")  // Sensor data from all devices
            .WithTopicFilter("devices/+/rfid/check")  // RFID validation requests
            .WithTopicFilter("devices/+/status/#")  // Device status updates
            .Build();

        await _mqttClient!.SubscribeAsync(subscribeOptions);
        _logger.LogInformation("✅ Subscribed to 3 topic patterns");
    }

    /// <summary>
    /// Called when an MQTT message is received from ESP32.
    /// This is the main message routing logic.
    /// </summary>
    private async Task OnMessageReceivedAsync(MqttApplicationMessageReceivedEventArgs e)
    {
        try
        {
            var topic = e.ApplicationMessage.Topic;
            var payload = Encoding.UTF8.GetString(e.ApplicationMessage.Payload);

            _logger.LogInformation($"📨 Received MQTT message on topic: {topic}");
            _logger.LogDebug($"Payload: {payload}");

            // Route message to appropriate handler based on topic
            if (topic.Contains("/rfid/check"))
            {
                await HandleRfidCheckAsync(topic, payload);
            }
            else if (topic.Contains("/data"))
            {
                await HandleSensorDataAsync(topic, payload);
            }
            else if (topic.Contains("/status/"))
            {
                await HandleStatusUpdateAsync(topic, payload);
            }
            else
            {
                _logger.LogWarning($"⚠️ Unknown topic pattern: {topic}");
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "❌ Error processing MQTT message");
        }
    }

    /// <summary>
    /// Handle RFID validation requests from ESP32.
    /// Pattern: devices/{deviceId}/rfid/check
    /// </summary>
    private async Task HandleRfidCheckAsync(string topic, string payload)
    {
        _logger.LogInformation("🔐 Processing RFID validation request");

        // Extract device ID from topic (e.g., "devices/esp32_main/rfid/check" → "esp32_main")
        var deviceId = topic.Split('/')[1];

        // Parse JSON payload
        var data = JsonSerializer.Deserialize<Dictionary<string, JsonElement>>(payload);
        var cardId = data?["card_id"].GetString();

        if (string.IsNullOrEmpty(cardId))
        {
            _logger.LogWarning("⚠️ RFID check request missing card_id");
            return;
        }

        // Create a scope to get scoped services (CardLookupService)
        using var scope = _scopeFactory.CreateScope();
        var cardService = scope.ServiceProvider.GetRequiredService<CardLookupService>();

        // Validate card using the service layer
        var isValid = await cardService.IsCardValidAsync(cardId);

        _logger.LogInformation($"🔐 Card {cardId} validation result: {isValid}");

        // Publish validation response back to ESP32
        // Format matches ESP32 expectations: {"access": "granted"/"denied", "card_id": "...", "timestamp": "..."}
        var response = new
        {
            access = isValid ? "granted" : "denied",
            card_id = cardId,
            timestamp = DateTimeOffset.UtcNow.ToString("O")
        };

        var responseJson = JsonSerializer.Serialize(response);
        var responseTopic = $"devices/{deviceId}/rfid/response";

        await PublishAsync(responseTopic, responseJson);
        _logger.LogInformation($"📤 Published RFID validation response to {responseTopic}");

        // TODO: Log RFID scan to database (rfid_scans table)
    }

    /// <summary>
    /// Handle sensor data from ESP32.
    /// Pattern: devices/{deviceId}/data
    /// </summary>
    private Task HandleSensorDataAsync(string topic, string payload)
    {
        _logger.LogInformation("📊 Processing sensor data");

        // TODO: Parse sensor data and write to database (sensor_logs table)
        // This will be implemented in T2.6 - SensorDataWriter service

        return Task.CompletedTask;
    }

    /// <summary>
    /// Handle device status updates (fan, door, window, LED).
    /// Pattern: devices/{deviceId}/status/{output}
    /// </summary>
    private Task HandleStatusUpdateAsync(string topic, string payload)
    {
        _logger.LogInformation($"📡 Processing status update: {topic}");

        // TODO: Log status changes if needed

        return Task.CompletedTask;
    }

    /// <summary>
    /// Publish a message to an MQTT topic.
    /// Used to send responses back to ESP32.
    /// </summary>
    private async Task PublishAsync(string topic, string payload)
    {
        if (_mqttClient == null || !_mqttClient.IsConnected)
        {
            _logger.LogWarning("⚠️ Cannot publish - MQTT client not connected");
            return;
        }

        var message = new MqttApplicationMessageBuilder()
            .WithTopic(topic)
            .WithPayload(payload)
            .WithQualityOfServiceLevel(MQTTnet.Protocol.MqttQualityOfServiceLevel.AtLeastOnce)
            .WithRetainFlag(false)
            .Build();

        await _mqttClient.PublishAsync(message);
    }

    /// <summary>
    /// Called when MQTT client successfully connects
    /// </summary>
    private Task OnConnectedAsync(MqttClientConnectedEventArgs e)
    {
        _logger.LogInformation("✅ MQTT client connected");
        return Task.CompletedTask;
    }

    /// <summary>
    /// Called when MQTT client disconnects.
    /// Attempts automatic reconnection.
    /// </summary>
    private Task OnDisconnectedAsync(MqttClientDisconnectedEventArgs e)
    {
        _logger.LogWarning($"⚠️ MQTT client disconnected: {e.Reason}");

        // Schedule reconnection attempt after 5 seconds
        _reconnectTimer = new Timer(async _ =>
        {
            try
            {
                _logger.LogInformation("🔄 Attempting to reconnect to MQTT broker...");
                await ConnectAsync();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "❌ Reconnection attempt failed");
            }
        }, null, TimeSpan.FromSeconds(5), Timeout.InfiniteTimeSpan);

        return Task.CompletedTask;
    }

    /// <summary>
    /// Called when the application stops.
    /// Gracefully disconnect from MQTT broker.
    /// </summary>
    public async Task StopAsync(CancellationToken cancellationToken)
    {
        _logger.LogInformation("🛑 MQTT Background Service is stopping...");

        if (_mqttClient != null && _mqttClient.IsConnected)
        {
            await _mqttClient.DisconnectAsync();
        }

        _logger.LogInformation("✅ MQTT Background Service stopped");
    }

    /// <summary>
    /// Clean up resources
    /// </summary>
    public void Dispose()
    {
        _reconnectTimer?.Dispose();
        _mqttClient?.Dispose();
    }
}
