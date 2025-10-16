using Microsoft.AspNetCore.Mvc;
using Supabase;
using Supabase.Postgrest.Responses;
using api.models;
using api.contracts;

[ApiController]
[Route("[controller]")]

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
}