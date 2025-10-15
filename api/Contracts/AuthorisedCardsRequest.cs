using System.ComponentModel.DataAnnotations;

namespace api.contracts;

public class AuthorisedCardsRequest
{
    [Required]
    [MaxLength(100)]
    public string CardId { get; set; }
    public Guid? UserId { get; set; }
    public bool? IsActive { get; set; }
}