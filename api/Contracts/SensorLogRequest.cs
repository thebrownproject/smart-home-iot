using System.ComponentModel.DataAnnotations;

namespace api.contracts;

public class SensorLogRequest
{
    [Required]
    public Guid DeviceId { get; set; }
    [Required]
    [MaxLength(50)]
    public required string SensorType { get; set; }
    [Required]
    public decimal Value { get; set; }
}