using System.ComponentModel.DataAnnotations;

namespace api.contracts;

public class GasAlertsRequest
{
    [Required]
    public Guid DeviceId { get; set; }
    [Required]
    public int SensorValue { get; set; }
    public DateTimeOffset? AlertStart { get; set; }
    public DateTimeOffset? AlertEnd { get; set; }
}