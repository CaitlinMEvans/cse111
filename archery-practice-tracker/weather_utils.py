import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY")
BASE_URL = "http://api.weatherapi.com/v1/current.json"

def fetch_weather(lat, lon):
    if not WEATHERAPI_KEY:
        print("Error: WeatherAPI key is missing. Please add it to the .env file.")
        return None

    try:
        params = {
            "key": WEATHERAPI_KEY,
            "q": f"{lat},{lon}",
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        return {
            "temperature": data["current"]["temp_f"],
            "wind_speed": data["current"]["wind_mph"],
            "precipitation": data["current"].get("precip_mm", 0)
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None