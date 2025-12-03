using Microsoft.AspNetCore.Mvc;
using Supabase;
using Supabase.Postgrest.Responses;
using api.models;

[ApiController]
[Route("[controller]")]

public class SensorController : ControllerBase
{
    [HttpGet("temperature")]
    public async Task<IActionResult> OnGetAsync(
        Guid id, [FromServices] Client client)
    {
        ModeledResponse<SensorLogModel> response = await client
            .From<SensorLogModel>()
            .Where(i => i.DeviceId == id)
            .Get();
        SensorLogModel? sensorLog = response.Models.FirstOrDefault();
        if (sensorLog is null) return NotFound();
        return Ok(response.Models);
    }
}
