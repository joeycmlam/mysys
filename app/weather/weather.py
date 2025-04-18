from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("weather")

# API Configuration
NWS_API = "https://api.weather.gov"
USER_AGENT = "MyWeatherMCP/1.0 (your@email.com)"

async def fetch_weather_data(url: str) -> dict | None:
    """Fetch data from NWS API with error handling"""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"API Error: {str(e)}")
            return None

@mcp.tool()
async def get_weather_alerts(state: str) -> str:
    """Get active weather alerts for a US state
    Args:
        state: 2-letter state code (e.g. CA, NY)
    """
    url = f"{NWS_API}/alerts/active/area/{state}"
    data = await fetch_weather_data(url)
    
    if not data or "features" not in data:
        return "No active alerts found"
    
    alerts = []
    for alert in data["features"]:
        props = alert["properties"]
        alerts.append(
            f"{props['event']} - {props['areaDesc']}\n"
            f"Severity: {props['severity']}\n"
            f"{props['description']}"
        )
    return "\n\n".join(alerts[:5])  # Return top 5 alerts

@mcp.tool() 
async def get_weather_forecast(lat: float, lon: float) -> str:
    """Get detailed weather forecast for coordinates
    Args:
        lat: Latitude (-90 to 90)
        lon: Longitude (-180 to 180)
    """
    points_url = f"{NWS_API}/points/{lat},{lon}"
    points_data = await fetch_weather_data(points_url)
    
    if not points_data:
        return "Location not found"
    
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await fetch_weather_data(forecast_url)
    
    if not forecast_data:
        return "Forecast unavailable"
    
    periods = forecast_data["properties"]["periods"][:3]  # Next 3 periods
    forecast = []
    for period in periods:
        forecast.append(
            f"{period['name']}:\n"
            f"Temp: {period['temperature']}°{period['temperatureUnit']}\n"
            f"Wind: {period['windSpeed']} {period['windDirection']}\n"
            f"{period['detailedForecast']}"
        )
    return "\n\n".join(forecast)

if __name__ == "__main__":
    mcp.run()
