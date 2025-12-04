using System.ComponentModel.DataAnnotations;
using System.ComponentModel;

namespace api.contracts;

public class AuthorisedCardsRequest
{
    [Required]
    [MaxLength(100)]
    public required string CardId { get; set; }

    // Nullable Guid to match database schema (user_id UUID)
    // DefaultValue(null) tells Swagger to show null as the example
    [DefaultValue(null)]
    public Guid? UserId { get; set; }

    // Defaults to true if not provided
    [DefaultValue(true)]
    public bool? IsActive { get; set; }
}