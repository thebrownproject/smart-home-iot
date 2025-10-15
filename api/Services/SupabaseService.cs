using Supabase;

namespace SmartHomeApi.Services;

public class SupabaseService
{
    private readonly Supabase.Client _client;

    public SupabaseService(IConfiguration configuration)
    {
        var url = configuration["SupabaseUrl"]
            ?? throw new ArgumentNullException("SupabaseUrl not found in configuration");
        var key = configuration["SupabaseApiKey"]
            ?? throw new ArgumentNullException("SupabaseApiKey not found in configuration");

        var options = new SupabaseOptions
        {
            AutoConnectRealtime = false // We're using MQTT for realtime, not Supabase Realtime
        };

        _client = new Supabase.Client(url, key, options);
    }

    public Supabase.Client GetClient()
    {
        return _client;
    }

    // Query sensor_logs table
    public async Task<List<T>> QuerySensorLogs<T>(int hoursBack = 24) where T : class, new()
    {
        var cutoffTime = DateTime.UtcNow.AddHours(-hoursBack);
        var response = await _client
            .From<T>()
            .Where(x => x.GetType().GetProperty("timestamp")!.GetValue(x)! >= cutoffTime)
            .Get();

        return response.Models;
    }

    // Insert sensor log
    public async Task<T> InsertSensorLog<T>(T logEntry) where T : class, new()
    {
        var response = await _client
            .From<T>()
            .Insert(logEntry);

        return response.Models.First();
    }

    // Query motion events
    public async Task<List<T>> QueryMotionEvents<T>(int hoursBack = 1) where T : class, new()
    {
        var cutoffTime = DateTime.UtcNow.AddHours(-hoursBack);
        var response = await _client
            .From<T>()
            .Where(x => x.GetType().GetProperty("detected_at")!.GetValue(x)! >= cutoffTime)
            .Get();

        return response.Models;
    }

    // Insert motion event
    public async Task<T> InsertMotionEvent<T>(T motionEvent) where T : class, new()
    {
        var response = await _client
            .From<T>()
            .Insert(motionEvent);

        return response.Models.First();
    }

    // Query gas alerts
    public async Task<List<T>> QueryGasAlerts<T>() where T : class, new()
    {
        var response = await _client
            .From<T>()
            .Order("started_at", Postgrest.Constants.Ordering.Descending)
            .Limit(50)
            .Get();

        return response.Models;
    }

    // Insert gas alert
    public async Task<T> InsertGasAlert<T>(T gasAlert) where T : class, new()
    {
        var response = await _client
            .From<T>()
            .Insert(gasAlert);

        return response.Models.First();
    }

    // Query RFID scans with optional filter
    public async Task<List<T>> QueryRfidScans<T>(string? filter = null) where T : class, new()
    {
        var query = _client
            .From<T>()
            .Order("scanned_at", Postgrest.Constants.Ordering.Descending)
            .Limit(50);

        if (filter == "success")
        {
            query = query.Where(x => (bool)x.GetType().GetProperty("access_granted")!.GetValue(x)! == true);
        }
        else if (filter == "failed")
        {
            query = query.Where(x => (bool)x.GetType().GetProperty("access_granted")!.GetValue(x)! == false);
        }

        var response = await query.Get();
        return response.Models;
    }

    // Insert RFID scan
    public async Task<T> InsertRfidScan<T>(T rfidScan) where T : class, new()
    {
        var response = await _client
            .From<T>()
            .Insert(rfidScan);

        return response.Models.First();
    }

    // Validate RFID card (check if card is authorized)
    public async Task<T?> ValidateRfidCard<T>(string cardId) where T : class, new()
    {
        var response = await _client
            .From<T>()
            .Where(x => x.GetType().GetProperty("card_id")!.GetValue(x)!.ToString() == cardId)
            .Where(x => (bool)x.GetType().GetProperty("is_active")!.GetValue(x)! == true)
            .Single();

        return response;
    }
}
