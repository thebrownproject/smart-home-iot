using Supabase;
using Supabase.Postgrest.Responses;
using api.models;

namespace api.services;

/// <summary>
/// Service for looking up RFID cards in the database.
/// Shared by both HTTP controllers and MQTT background services.
/// </summary>
public class CardLookupService
{
    private readonly Client _supabase;

    // Dependency Injection - Supabase client injected by ASP.NET Core
    public CardLookupService(Client supabase)
    {
        _supabase = supabase;
    }

    /// <summary>
    /// Look up a card by its RFID card_id (e.g., "abc123")
    /// </summary>
    /// <param name="cardId">The RFID card identifier</param>
    /// <returns>Card model if found, null otherwise</returns>
    public async Task<AuthorisedCardsModel?> GetByCardIdAsync(string cardId)
    {
        ModeledResponse<AuthorisedCardsModel> response = await _supabase
            .From<AuthorisedCardsModel>()
            .Where(x => x.CardId == cardId)
            .Get();

        return response.Models.FirstOrDefault();
    }

    /// <summary>
    /// Look up a card by its internal database ID (UUID)
    /// </summary>
    /// <param name="id">The database UUID</param>
    /// <returns>Card model if found, null otherwise</returns>
    public async Task<AuthorisedCardsModel?> GetByIdAsync(Guid id)
    {
        ModeledResponse<AuthorisedCardsModel> response = await _supabase
            .From<AuthorisedCardsModel>()
            .Where(x => x.Id == id)
            .Get();

        return response.Models.FirstOrDefault();
    }

    /// <summary>
    /// Check if a card is valid for access control.
    /// A card is valid if it exists AND is_active = true.
    /// </summary>
    /// <param name="cardId">The RFID card identifier</param>
    /// <returns>True if card is valid for access, false otherwise</returns>
    public async Task<bool> IsCardValidAsync(string cardId)
    {
        var card = await GetByCardIdAsync(cardId);
        return card != null && card.IsActive == true;
    }
}
