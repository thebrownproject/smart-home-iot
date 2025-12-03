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

        return Ok(response.Models);
    }
}