using System.ComponentModel.DataAnnotations;

namespace api.contracts;

public class RfidScansRequest
{
    [Required]
    public Guid DeviceId { get; set; }
    [Required]
    [MaxLength(100)]
    public required string CardId { get; set; }
    public Guid? AuthorisedCardId { get; set; }
    [Required]
    [MaxLength(20)]
    [RegularExpression("^(granted|denied)$", ErrorMessage = "AccessResult must be 'granted' or 'denied'.")]
    public required string AccessResult { get; set; }
}
