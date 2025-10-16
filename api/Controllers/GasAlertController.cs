using Microsoft.AspNetCore.Mvc;
using Supabase;
using Supabase.Postgrest.Responses;
using api.models;
using api.contracts;

[ApiController]
[Route("[controller]")]

public class GasAlertController : ControllerBase
{
    [HttpPost]
    public async Task<IActionResult> OnPostAsync(
        [FromBody] GasAlertsRequest request,
        [FromServices] Client client
    )
    {
        GasAlertsModel gasAlert = new GasAlertsModel();
        ModeledResponse<GasAlertsModel> response = await client.From<GasAlertsModel>().Insert(gasAlert);
        GasAlertsModel newGasAlert = response.Models.First();
        return Ok(newGasAlert);
    }
}