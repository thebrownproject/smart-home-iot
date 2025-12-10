using Microsoft.AspNetCore.Mvc;
using Supabase;
using Supabase.Postgrest.Responses;
using api.models;
using api.contracts;

namespace api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class RfidScansController : ControllerBase
{
    [HttpPost]
    public async Task<IActionResult> OnPostAsync(
        [FromBody] RfidScansRequest request,
        [FromServices] Client client
    )
    {
        RfidScansModel rfidScan = new RfidScansModel(request);
        ModeledResponse<RfidScansModel> response = await client.From<RfidScansModel>().Insert(rfidScan);
        RfidScansModel newRfidScan = response.Models.First();
        return Ok(newRfidScan);
    }

    [HttpGet]
    public async Task<IActionResult> GetScans(
        [FromServices] Client client,
        [FromQuery] string filter = "all"
    )
    {
        ModeledResponse<RfidScansModel> response;

        // Apply filter based on access_result
        if (filter == "success")
        {
            response = await client.From<RfidScansModel>()
                .Where(x => x.AccessResult == "granted")
                .Order("timestamp", Supabase.Postgrest.Constants.Ordering.Descending)
                .Get();
        }
        else if (filter == "failed")
        {
            response = await client.From<RfidScansModel>()
                .Where(x => x.AccessResult == "denied")
                .Order("timestamp", Supabase.Postgrest.Constants.Ordering.Descending)
                .Get();
        }
        else // "all"
        {
            response = await client.From<RfidScansModel>()
                .Order("timestamp", Supabase.Postgrest.Constants.Ordering.Descending)
                .Get();
        }

        // Get authorised cards to lookup usernames
        var cardsResponse = await client.From<AuthorisedCardsModel>().Get();
        var cardLookup = cardsResponse.Models.ToDictionary(c => c.Id, c => c.Username);

        // Build response with username from authorised_cards
        var result = response.Models.Select(scan => new
        {
            scan.Id,
            scan.DeviceId,
            scan.CardId,
            scan.AuthorisedCardId,
            scan.AccessResult,
            scan.Timestamp,
            Username = scan.AuthorisedCardId.HasValue && cardLookup.ContainsKey(scan.AuthorisedCardId.Value)
                ? cardLookup[scan.AuthorisedCardId.Value]
                : null
        });

        return Ok(result);
    }
}