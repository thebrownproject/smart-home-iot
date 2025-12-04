using Microsoft.AspNetCore.Mvc;
using Supabase;
using Supabase.Postgrest.Responses;
using api.models;
using api.contracts;

[ApiController]
[Route("[controller]")]
public class SensorLogController : ControllerBase
{
    private readonly ILogger<SensorLogController> _logger;

    public SensorLogController(ILogger<SensorLogController> logger)
    {
        _logger = logger;
    }

    [HttpPost]
    public async Task<IActionResult> OnPostAsync(
        [FromBody] SensorLogRequest? request,
        [FromServices] Client client)
    {
        // Validate request is not null
        if (request == null)
        {
            _logger.LogWarning("SensorLog POST received null request body");
            return BadRequest(new { error = "Request body is required" });
        }

        // Validate DeviceId is not empty
        if (request.DeviceId == Guid.Empty)
        {
            _logger.LogWarning("SensorLog POST received empty DeviceId");
            return BadRequest(new { error = "DeviceId is required" });
        }

        // Validate SensorType is valid
        var validSensorTypes = new[] { "temperature", "humidity", "gas", "motion" };
        if (!validSensorTypes.Contains(request.SensorType.ToLowerInvariant()))
        {
            _logger.LogWarning("SensorLog POST received invalid SensorType: {SensorType}", request.SensorType);
            return BadRequest(new { error = $"SensorType must be one of: {string.Join(", ", validSensorTypes)}" });
        }

        SensorLogModel sensorLog = new SensorLogModel(Guid.Empty, request);
        ModeledResponse<SensorLogModel> response = await client.From<SensorLogModel>().Insert(sensorLog);

        if (!response.Models.Any())
        {
            _logger.LogError("Failed to insert sensor log for device {DeviceId}", request.DeviceId);
            return StatusCode(500, new { error = "Failed to create sensor log" });
        }

        SensorLogModel newSensorLog = response.Models.First();
        _logger.LogInformation("Created sensor log {Id} for device {DeviceId}", newSensorLog.Id, request.DeviceId);
        return Ok(newSensorLog);
    }
}