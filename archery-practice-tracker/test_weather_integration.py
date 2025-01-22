# test_weather_integration.py
import unittest
from weather_utils import fetch_weather

class TestWeatherIntegration(unittest.TestCase):

    def test_fetch_weather_valid(self):
        weather = fetch_weather("40.2837", "-111.635")
        self.assertIsNotNone(weather)
        self.assertIn("temperature", weather)
        self.assertIn("wind_speed", weather)
        self.assertIn("precipitation", weather)

    def test_fetch_weather_invalid(self):
        weather = fetch_weather("invalid", "coordinates")
        self.assertIsNone(weather)