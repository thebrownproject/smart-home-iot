using Microsoft.AspNetCore.Mvc;
using Supabase;
using Supabase.Postgrest.Responses;
using api.models;
using api.contracts;

[ApiController]
[Route("[controller]")]

public class SensorLogController : ControllerBase
{
    [HttpPost]
    public async Task<IActionResult> OnPostAsync(
        [FromBody] SensorLogRequest request,
        [FromServices] Client client
    )
    {
        SensorLogModel sensorLog = new SensorLogModel(Guid.Empty, request);
        ModeledResponse<SensorLogModel> response = await client.From<SensorLogModel>().Insert(sensorLog);
        SensorLogModel newSensorLog = response.Models.First();
        return Ok(newSensorLog);
    }
}