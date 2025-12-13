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
    private readonly ILogger<RfidScansController> _logger;

    public RfidScansController(ILogger<RfidScansController> logger)
    {
        _logger = logger;
    }

    [HttpPost]
    public async Task<IActionResult> OnPostAsync(
        [FromBody] RfidScansRequest? request,
        [FromServices] Client client
    )
    {
        // Validate request is not null
        if (request == null)
        {
            _logger.LogWarning("RfidScans POST received null request body");
            return BadRequest(new { error = "Request body is required" });
        }

        // Validate DeviceId is not empty
        if (request.DeviceId == Guid.Empty)
        {
            _logger.LogWarning("RfidScans POST received empty DeviceId");
            return BadRequest(new { error = "DeviceId is required" });
        }

        try
        {
            RfidScansModel rfidScan = new RfidScansModel(request);
            ModeledResponse<RfidScansModel> response = await client.From<RfidScansModel>().Insert(rfidScan);

            if (!response.Models.Any())
            {
                _logger.LogError("Failed to insert RFID scan for device {DeviceId}", request.DeviceId);
                return StatusCode(500, new { error = "Failed to create RFID scan record" });
            }

            RfidScansModel newRfidScan = response.Models.First();
            _logger.LogInformation("RFID scan {Id} created for device {DeviceId}, card {CardId}, result: {AccessResult}",
                newRfidScan.Id, request.DeviceId, request.CardId, request.AccessResult);
            return Ok(newRfidScan);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error creating RFID scan for device {DeviceId}, card {CardId}. This may be due to invalid DeviceId (must exist in devices table) or AuthorisedCardId (must exist in authorised_cards table if provided).",
                request.DeviceId, request.CardId);
            return StatusCode(500, new { error = "Failed to create RFID scan. Check that DeviceId exists in devices table.", details = ex.Message });
        }
    }

    [HttpGet]
    public async Task<IActionResult> GetScans(
        [FromServices] Client client,
        [FromQuery] string filter = "all",
        [FromQuery] int hours = 24
    )
    {
        DateTimeOffset cutoffTime = DateTimeOffset.UtcNow.AddHours(-hours);
        ModeledResponse<RfidScansModel> response;

        // Apply filter based on access_result
        if (filter == "success")
        {
            response = await client.From<RfidScansModel>()
                .Where(x => x.AccessResult == "granted" && x.Timestamp >= cutoffTime)
                .Order("timestamp", Supabase.Postgrest.Constants.Ordering.Descending)
                .Get();
        }
        else if (filter == "failed")
        {
            response = await client.From<RfidScansModel>()
                .Where(x => x.AccessResult == "denied" && x.Timestamp >= cutoffTime)
                .Order("timestamp", Supabase.Postgrest.Constants.Ordering.Descending)
                .Get();
        }
        else // "all"
        {
            response = await client.From<RfidScansModel>()
                .Where(x => x.Timestamp >= cutoffTime)
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