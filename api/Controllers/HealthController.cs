using Microsoft.AspNetCore.Mvc;

namespace Supabase_Minimal_API.Controllers;

/// <summary>
/// Health check endpoint for Docker monitoring
/// </summary>
[ApiController]
[Route("health")]
public class HealthController : ControllerBase
{
    /// <summary>
    /// Simple health check - returns 200 OK if service is running
    /// </summary>
    [HttpGet]
    public IActionResult Get()
    {
        return Ok(new {
            status = "healthy",
            timestamp = DateTime.UtcNow,
            service = "Smart Home API"
        });
    }
}