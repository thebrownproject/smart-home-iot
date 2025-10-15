using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;
using api.contracts;

namespace api.models;

[Table("gas_alerts")]
public class GasAlertsModel : BaseModel
{
    public GasAlertsModel() { }

    public GasAlertsModel(GasAlertsRequest request)
    {
        DeviceId = request.DeviceId;
        SensorValue = request.SensorValue;
        AlertEnd = request.AlertEnd;
    }

    [PrimaryKey("id")]
    public Guid Id { get; set; }

    [Column("device_id")]
    public Guid DeviceId { get; set; }

    [Column("sensor_value")]
    public int SensorValue { get; set; }

    [Column("alert_start")]
    public DateTimeOffset AlertStart { get; set; }

    [Column("alert_end")]
    public DateTimeOffset? AlertEnd { get; set; }
}
