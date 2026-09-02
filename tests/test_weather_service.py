"""
Unit tests for WeatherService business logic.
"""

import unittest
from src.weather_service import weather_service

class TestWeatherService(unittest.TestCase):

    def test_get_weather_known_city(self):
        result = weather_service.get_weather("London")
        self.assertEqual(result["city"], "London")
        self.assertEqual(result["country"], "UK")
        self.assertIn("celsius", result["temperature"])
        self.assertIn("fahrenheit", result["temperature"])
        self.assertEqual(len(result["forecast"]), 5)

    def test_get_weather_unknown_city(self):
        result = weather_service.get_weather("Atlantis")
        self.assertEqual(result["city"], "Atlantis")
        self.assertIn("forecast", result)
        self.assertEqual(len(result["forecast"]), 5)

    def test_get_weather_empty_city_raises_error(self):
        with self.assertRaises(ValueError):
            weather_service.get_weather("")

        with self.assertRaises(ValueError):
            weather_service.get_weather("   ")

if __name__ == "__main__":
    unittest.main()
