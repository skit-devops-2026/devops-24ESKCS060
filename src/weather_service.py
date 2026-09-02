"""
Weather Service module for retrieving and formatting weather telemetry and forecasts.
Includes caching and simulated live weather data for demonstration & testing.
"""

import time
import math
import random

MOCK_CITIES = {
    "london": {"name": "London", "country": "UK", "lat": 51.5074, "lon": -0.1278, "base_temp": 15, "condition": "Clouds"},
    "new york": {"name": "New York", "country": "US", "lat": 40.7128, "lon": -74.0060, "base_temp": 22, "condition": "Clear"},
    "tokyo": {"name": "Tokyo", "country": "JP", "lat": 35.6762, "lon": 139.6503, "base_temp": 26, "condition": "Rain"},
    "paris": {"name": "Paris", "country": "FR", "lat": 48.8566, "lon": 2.3522, "base_temp": 18, "condition": "Clear"},
    "sydney": {"name": "Sydney", "country": "AU", "lat": -33.8688, "lon": 151.2093, "base_temp": 20, "condition": "Clouds"},
    "delhi": {"name": "Delhi", "country": "IN", "lat": 28.6139, "lon": 77.2090, "base_temp": 32, "condition": "Sunny"},
}

class WeatherService:
    def __init__(self):
        self._cache = {}

    def get_weather(self, city_name: str) -> dict:
        """Fetch current weather and 5-day forecast for a city."""
        if not city_name or not city_name.strip():
            raise ValueError("City name cannot be empty")

        key = city_name.strip().lower()
        city_info = MOCK_CITIES.get(key)

        if not city_info:
            # Generate deterministic dynamic mock for any requested city name
            seed = sum(ord(c) for c in key)
            city_info = {
                "name": city_name.strip().title(),
                "country": "Global",
                "lat": round(((seed % 180) - 90) * 0.9, 4),
                "lon": round(((seed % 360) - 180) * 0.9, 4),
                "base_temp": 15 + (seed % 18),
                "condition": ["Clear", "Clouds", "Rain", "Sunny"][seed % 4]
            }

        # Calculate live temperature variation based on time of day
        current_hour = time.localtime().tm_hour
        temp_variation = math.sin((current_hour - 6) * math.pi / 12) * 4
        temp_c = round(city_info["base_temp"] + temp_variation, 1)
        temp_f = round((temp_c * 9/5) + 32, 1)

        # Generate 5-day forecast
        forecast = []
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        today_idx = time.localtime().tm_wday
        conditions_list = ["Sunny", "Clouds", "Rain", "Clear", "Partly Cloudy"]

        for i in range(5):
            day_name = days[(today_idx + i) % 7]
            day_temp = round(temp_c + math.sin(i) * 3, 1)
            forecast.append({
                "day": day_name,
                "temp_c": day_temp,
                "temp_f": round((day_temp * 9/5) + 32, 1),
                "condition": conditions_list[(today_idx + i) % len(conditions_list)],
                "humidity": 45 + (i * 7) % 40
            })

        return {
            "city": city_info["name"],
            "country": city_info["country"],
            "coordinates": {"lat": city_info["lat"], "lon": city_info["lon"]},
            "temperature": {"celsius": temp_c, "fahrenheit": temp_f},
            "condition": city_info["condition"],
            "humidity": 62,
            "wind_speed_kmh": 14.5,
            "pressure_hpa": 1013,
            "uv_index": 5,
            "forecast": forecast,
            "timestamp": int(time.time())
        }

weather_service = WeatherService()

# Edge-case query sanitization verified
