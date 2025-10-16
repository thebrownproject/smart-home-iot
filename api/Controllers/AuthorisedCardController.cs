using Microsoft.AspNetCore.Mvc;
using Supabase;
using Supabase.Postgrest.Responses;
using api.models;
using api.contracts;
using api.services;

[ApiController]
[Route("[controller]")]

public class AuthorisedCardController : ControllerBase
{
    private readonly CardLookupService _cardService;

    // Constructor injection - ASP.NET Core DI container provides the service
    public AuthorisedCardController(CardLookupService cardService)
    {
        _cardService = cardService;
    }

    [HttpPost]
    public async Task<IActionResult> OnPostAsync(
        [FromBody] AuthorisedCardsRequest request,
        [FromServices] Client client
    )
    {
        AuthorisedCardsModel authorisedCard = new AuthorisedCardsModel(request);
        ModeledResponse<AuthorisedCardsModel> response = await client.From<AuthorisedCardsModel>().Insert(authorisedCard);
        AuthorisedCardsModel newAuthorisedCard = response.Models.First();
        return Ok(newAuthorisedCard);
    }

    // GET by internal database ID (UUID)
    [HttpGet("{id:guid}")]
    public async Task<IActionResult> GetByIdAsync(Guid id)
    {
        AuthorisedCardsModel? authorisedCard = await _cardService.GetByIdAsync(id);
        if (authorisedCard is null) return NotFound();
        return Ok(authorisedCard);
    }

    // GET by RFID card_id (string) - used for RFID validation
    [HttpGet("card/{cardId}")]
    public async Task<IActionResult> GetByCardIdAsync(string cardId)
    {
        AuthorisedCardsModel? authorisedCard = await _cardService.GetByCardIdAsync(cardId);
        if (authorisedCard is null) return NotFound(new { message = "Card not found" });

        // Return card info and validation status
        return Ok(new
        {
            cardId = authorisedCard.CardId,
            isActive = authorisedCard.IsActive,
            isValid = authorisedCard.IsActive == true, // Only valid if active
            userId = authorisedCard.UserId
        });
    }
}
