// Using statements
using Newtonsoft.Json;
using Supabase;

// Namespace
namespace Supabase_Minimal_API;

// Program class
internal static class Program
{
    // Application entry point
    private static void Main(string[] args)
    {
        // Creates the foundation for the application
        WebApplicationBuilder builder = WebApplication.CreateBuilder(args);

        // Configures the builder with the necessary services
        bool useSwagger = builder.Configuration.GetValue<bool>("UseSwagger");

        // Configures the web app builder
        ConfigureWebAppBuilder(builder, useSwagger);

        // Builds the application
        WebApplication app = BuildWebApp(builder, useSwagger);

        // Runs the application
        app.Run();
    }

    // Configures the web app builder with the necessary services
    private static void ConfigureWebAppBuilder(WebApplicationBuilder builder, bool useSwagger)
    {
        // Add controllers and configure JSON serialization
        builder.Services.AddControllers().AddNewtonsoftJson(options =>
        {
            // Why? Ignores reference loops in JSON serialization
            options.SerializerSettings.ReferenceLoopHandling = ReferenceLoopHandling.Ignore;
        });

        // Configures the Supabase client
        ConfigureSupabase(builder.Services, builder.Configuration);

        // Register service layer (business logic)
        // Why Scoped? Services are created once per HTTP request (or MQTT message handling)
        builder.Services.AddScoped<api.services.CardLookupService>();

        // Register MQTT background service
        // Why HostedService? Runs in background when app starts, independent of HTTP requests
        builder.Services.AddHostedService<api.services.MqttBackgroundService>();

        // Configures the Swagger UI
        if (useSwagger)
        {
            builder.Services.AddEndpointsApiExplorer();
            builder.Services.AddSwaggerGen();

            builder.Services.AddSwaggerGen(options =>
            {
                options.SwaggerDoc("v1", new Microsoft.OpenApi.Models.OpenApiInfo
                {
                    Title = "Smart Home API",
                    Version = "v1",
                    Description = "ASP.NET Core API for Smart Home automation system - handles MQTT middleware, RFID validation, and sensor data persistence"
                });
            });
        }
    }

    // Configures the Supabase client
    private static void ConfigureSupabase(IServiceCollection services, IConfiguration config)
    {
        // Gets the Supabase URL and API key from the configuration
        string? url = config.GetValue<string>("SupabaseUrl");
        string? supabasekey = config.GetValue<string>("SupabaseApiKey");

        // Throws an exception if the Supabase URL or API key is missing
        if (string.IsNullOrWhiteSpace(url) ||
            string.IsNullOrWhiteSpace(supabasekey))
        {
            throw new Exception("Missing Supabase config in appsettings.json");
        }

        // Adds the Supabase client to the DI container as a singleton
        // Why singleton? The Supabase client maintains connection state and should be reused
        services.AddSingleton(_ =>
        {
            // Creates a new Supabase client with options
            SupabaseOptions options = new SupabaseOptions
            {
                AutoRefreshToken = true,
                // Disable realtime - we only need REST API (Postgrest) for database operations
                // Realtime would be for live subscriptions, which we handle via MQTT instead
                AutoConnectRealtime = false
            };

            // Create and initialize the Supabase client synchronously
            // Note: InitializeAsync() must be called before using the client
            Client client = new Client(url, supabasekey, options);
            client.InitializeAsync().GetAwaiter().GetResult();

            return client;
        });
    }

    // Builds the web application
    private static WebApplication BuildWebApp(WebApplicationBuilder builder, bool useSwagger)
    {
        // Builds the web application
        WebApplication app = builder.Build();

        // Configures the web application
        if (useSwagger)
        {
            // Enables Swagger
            app.UseSwagger();
            app.UseSwaggerUI(options =>
            {
                options.SwaggerEndpoint("/swagger/v1/swagger.json", "Smart Home API v1");
            });
        }

        // Redirects to HTTPS
        app.UseHttpsRedirection();

        // Uses the controllers
        app.UseAuthorization();

        // Uses the controllers
        app.MapControllers();

        // Returns the web application
        return app;
    }
}
