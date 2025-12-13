using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;
using api.contracts;

namespace api.models;

[Table("rfid_scans")]
public class RfidScansModel : BaseModel
{
    public RfidScansModel()
    {
        CardId = string.Empty;
        AccessResult = string.Empty;
    }

    public RfidScansModel(RfidScansRequest request)
    {
        Id = Guid.NewGuid();
        DeviceId = request.DeviceId;
        CardId = request.CardId;
        AuthorisedCardId = request.AuthorisedCardId;
        Username = request.Username;
        AccessResult = request.AccessResult;
        Timestamp = DateTimeOffset.UtcNow;
    }

    [PrimaryKey("id")]
    public Guid Id { get; set; }

    [Column("device_id")]
    public Guid DeviceId { get; set; }

    [Column("card_id")]
    public string CardId { get; set; }

    [Column("authorised_card_id")]
    public Guid? AuthorisedCardId { get; set; }

    [Column("access_result")]
    public string AccessResult { get; set; }

    [Column("timestamp")]
    public DateTimeOffset Timestamp { get; set; }

    [Column("username")]
    public string? Username { get; set; }
}