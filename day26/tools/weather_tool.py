"""
Day 27 - Weather tool using Open-Meteo (free, no API key required).
"""

import requests
from langchain_core.tools import tool


def _geocode(city: str) -> tuple[float, float, str] | None:
    """Resolve a city name to latitude/longitude."""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    resp = requests.get(url, params={"name": city, "count": 1}, timeout=10)
    resp.raise_for_status()
    results = resp.json().get("results")
    if not results:
        return None
    r = results[0]
    label = f"{r['name']}, {r.get('country', '')}".strip(", ")
    return r["latitude"], r["longitude"], label


@tool
def weather(city: str) -> str:
    """Get the current weather for a city. Input should be a city name,
    e.g. 'Lahore' or 'New York'."""
    location = _geocode(city)
    if location is None:
        return f"Could not find a location matching '{city}'."

    lat, lon, label = location
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "timezone": "auto",
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json().get("current", {})

    temp = data.get("temperature_2m")
    humidity = data.get("relative_humidity_2m")
    wind = data.get("wind_speed_10m")
    code = data.get("weather_code")

    description = _weather_code_to_text(code)

    return (
        f"Current weather in {label}: {temp}°C, {description}, "
        f"humidity {humidity}%, wind {wind} km/h."
    )


def _weather_code_to_text(code: int) -> str:
    mapping = {
        0: "clear sky", 1: "mainly clear", 2: "partly cloudy", 3: "overcast",
        45: "fog", 48: "depositing rime fog",
        51: "light drizzle", 53: "moderate drizzle", 55: "dense drizzle",
        61: "slight rain", 63: "moderate rain", 65: "heavy rain",
        71: "slight snow", 73: "moderate snow", 75: "heavy snow",
        80: "rain showers", 81: "moderate rain showers", 82: "violent rain showers",
        95: "thunderstorm", 96: "thunderstorm with hail", 99: "severe thunderstorm with hail",
    }
    return mapping.get(code, "unknown conditions")


if __name__ == "__main__":
    print(weather.invoke("Lahore"))
    print(weather.invoke("Tokyo"))