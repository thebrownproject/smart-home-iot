# Multi-stage build for .NET 9.0 API
FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS base
WORKDIR /app
EXPOSE 8080
EXPOSE 443

FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src
# Copy csproj and restore as distinct layers
COPY ["SmartHomeApi.csproj", "."]
RUN dotnet restore "SmartHomeApi.csproj"
# Copy everything else and build
COPY . .
WORKDIR "/src/."
RUN dotnet build "SmartHomeApi.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "SmartHomeApi.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app
USER appuser
ENTRYPOINT ["dotnet", "SmartHomeApi.dll"]