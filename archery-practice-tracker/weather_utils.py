import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# WeatherAPI Key from .env
WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY")
BASE_URL = "http://api.weatherapi.com/v1/current.json"

def fetch_weather(latitude, longitude):
    """
    Fetch current weather data using WeatherAPI.
    """
    if not WEATHERAPI_KEY:
        print("Error: WeatherAPI key is missing. Please add it to the .env file.")
        return None

    try:
        params = {
            "key": WEATHERAPI_KEY,
            "q": f"{latitude},{longitude}",
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # Parse and return relevant data
        return {
            "temperature": data["current"]["temp_f"],
            "wind_speed": data["current"]["wind_mph"],
            "precipitation": data["current"].get("precip_mm", 0),
            "condition": data["current"]["condition"]["text"],
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def view_current_weather():
    """
    Displays the current weather for the user.
    """
    location = input("Enter the location (e.g., Provo, UT): ").strip()

    # Fetch weather data
    weather = fetch_weather("40.2837", "-111.635") if location.lower() == "provo, ut" else fetch_weather(location)
    if weather:
        print(f"Current Weather for {location}:")
        print(f"- Temperature: {weather['temperature']}°F")
        print(f"- Wind Speed: {weather['wind_speed']} mph")
        print(f"- Precipitation: {weather['precipitation']} mm")
        print(f"- Condition: {weather['condition']}")
    else:
        print("Unable to fetch weather data. Please try again later.")