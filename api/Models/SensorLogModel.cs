using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;
using api.contracts;

namespace api.models;

[Table("sensor_logs")]
public class SensorLogModel : BaseModel
{
    public SensorLogModel()
    {
        Id = 0;
        DeviceId = 0;
        SensorType = string.Empty;
        Value = 0;
        Timestamp = DateTime.UtcNow;
    }

    public SensorLogModel(long id, SensorLogRequest request)
    {
        Id = id;
        DeviceId = request.DeviceId;
        SensorType = request.SensorType;
        Value = (decimal)request.Value;
        Timestamp = DateTime.UtcNow;
    }

    [PrimaryKey("id")]
    public int Id { get; set; }

    [Column("device_id")]
    public long DeviceId { get; set; }

    [Column("sensor_type")]
    public string SensorType { get; set; }

    [Column("value")]
    public decimal Value { get; set; }

    [Column("timestamp")]
    public DateTime Timestamp { get; set; }
}