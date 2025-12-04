using Microsoft.AspNetCore.Mvc;
using Supabase;
using Supabase.Postgrest.Responses;
using api.models;
using api.contracts;

[ApiController]
[Route("[controller]")]
public class GasAlertController : ControllerBase
{
    private readonly ILogger<GasAlertController> _logger;

    public GasAlertController(ILogger<GasAlertController> logger)
    {
        _logger = logger;
    }

    [HttpPost]
    public async Task<IActionResult> OnPostAsync(
        [FromBody] GasAlertsRequest? request,
        [FromServices] Client client)
    {
        // Validate request is not null
        if (request == null)
        {
            _logger.LogWarning("GasAlert POST received null request body");
            return BadRequest(new { error = "Request body is required" });
        }

        // Validate DeviceId is not empty
        if (request.DeviceId == Guid.Empty)
        {
            _logger.LogWarning("GasAlert POST received empty DeviceId");
            return BadRequest(new { error = "DeviceId is required" });
        }

        // Validate SensorValue is within reasonable range (0-1023 for analog sensor)
        if (request.SensorValue < 0 || request.SensorValue > 1023)
        {
            _logger.LogWarning("GasAlert POST received invalid SensorValue: {SensorValue}", request.SensorValue);
            return BadRequest(new { error = "SensorValue must be between 0 and 1023" });
        }

        // Use the constructor that accepts the request (fixes bug: was creating empty model)
        GasAlertsModel gasAlert = new GasAlertsModel(request);
        ModeledResponse<GasAlertsModel> response = await client.From<GasAlertsModel>().Insert(gasAlert);

        if (!response.Models.Any())
        {
            _logger.LogError("Failed to insert gas alert for device {DeviceId}", request.DeviceId);
            return StatusCode(500, new { error = "Failed to create gas alert" });
        }

        GasAlertsModel newGasAlert = response.Models.First();
        _logger.LogWarning("Gas alert {Id} created for device {DeviceId} with value {SensorValue}",
            newGasAlert.Id, request.DeviceId, request.SensorValue);
        return Ok(newGasAlert);
    }
}