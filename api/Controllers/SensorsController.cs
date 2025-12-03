using Microsoft.AspNetCore.Mvc;
using Supabase;
using Supabase.Postgrest.Responses;
using api.models;

namespace api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class SensorsController : ControllerBase
{
    [HttpGet("motion")]
    public async Task<IActionResult> GetMotion(
        [FromServices] Client client,
        [FromQuery] int hours = 1
    )
    {
        DateTimeOffset cutoffTime = DateTimeOffset.UtcNow.AddHours(-hours);

        ModeledResponse<SensorLogModel> response = await client
            .From<SensorLogModel>()
            .Where(x => x.SensorType == "motion" && x.Timestamp >= cutoffTime)
            .Order("timestamp", Supabase.Postgrest.Constants.Ordering.Descending)
            .Get();

        return Ok(response.Models);
    }

    [HttpGet("gas")]
    public async Task<IActionResult> GetGas(
        [FromServices] Client client,
        [FromQuery] int hours = 24
    )
    {
        DateTimeOffset cutoffTime = DateTimeOffset.UtcNow.AddHours(-hours);

        ModeledResponse<GasAlertsModel> response = await client
            .From<GasAlertsModel>()
            .Where(x => x.AlertStart >= cutoffTime)
            .Order("alert_start", Supabase.Postgrest.Constants.Ordering.Descending)
            .Get();

        return Ok(response.Models);
    }
}
