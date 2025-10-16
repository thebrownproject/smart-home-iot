using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;
using api.contracts;

namespace api.models;

[Table("authorised_cards")]
public class AuthorisedCardsModel : BaseModel
{
    public AuthorisedCardsModel() { }

    public AuthorisedCardsModel(AuthorisedCardsRequest request)
    {
        CardId = request.CardId;
        UserId = request.UserId;
        IsActive = request.IsActive;
    }

    [PrimaryKey("id")]
    public Guid Id { get; set; }

    [Column("card_id")]
    public string CardId { get; set; } = string.Empty;

    [Column("user_id")]
    public Guid? UserId { get; set; }

    [Column("is_active")]
    public bool? IsActive { get; set; }

    [Column("created_at")]
    public DateTimeOffset CreatedAt { get; set; }
}