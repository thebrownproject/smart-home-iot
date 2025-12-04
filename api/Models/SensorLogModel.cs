using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;
using api.contracts;

namespace api.models;

[Table("sensor_logs")]
public class SensorLogModel : BaseModel
{
    public SensorLogModel()
    {
        SensorType = string.Empty;
        Value = 0m;
    }

    public SensorLogModel(Guid id, SensorLogRequest request)
    {
        Id = id;
        DeviceId = request.DeviceId;
        SensorType = request.SensorType;
        Value = request.Value;
    }

    [PrimaryKey("id")]
    public Guid Id { get; set; }

    [Column("device_id")]
    public Guid DeviceId { get; set; }

    [Column("sensor_type")]
    public string SensorType { get; set; }

    [Column("value")]
    public decimal Value { get; set; }

    [Column("timestamp")]
    public DateTimeOffset Timestamp { get; set; }
}