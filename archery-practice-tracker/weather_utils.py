import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# WeatherAPI Key from .env
WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY")
BASE_URL = "http://api.weatherapi.com/v1/current.json"

def fetch_weather_api(location="Provo, UT"):
    """
    Fetch current weather data using WeatherAPI.
    :param location: The location for which to fetch weather (default is Provo, UT).
    :return: A dictionary containing weather data or None if an error occurs.
    """
    if not WEATHERAPI_KEY:
        print("Error: WeatherAPI key is missing. Please add it to the .env file.")
        return None

    try:
        params = {
            "key": WEATHERAPI_KEY,
            "q": location,
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()

        # Parse and return relevant data
        return {
            "location": data["location"]["name"] + ", " + data["location"]["region"],
            "temperature_f": data["current"]["temp_f"],
            "temperature_c": data["current"]["temp_c"],
            "wind_speed_mph": data["current"]["wind_mph"],
            "humidity": data["current"]["humidity"],
            "precipitation_chance": data["current"].get("precip_mm", 0),
            "condition": data["current"]["condition"]["text"],
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None


def view_current_weather():
    """
    Displays the current weather based on user input location or default (Provo, UT).
    """
    use_default = input("Are you practicing at the Timpanogos Archery Club? (y/n): ").strip().lower()
    location = "Provo, UT" if use_default == 'y' else input("Enter city or ZIP code: ").strip()

    weather = fetch_weather_api(location)
    if weather:
        print(f"\nCurrent Weather for {weather['location']}:")
        print(f"- Temperature: {weather['temperature_f']}°F ({weather['temperature_c']}°C)")
        print(f"- Wind Speed: {weather['wind_speed_mph']} mph")
        print(f"- Humidity: {weather['humidity']}%")
        print(f"- Precipitation Chance: {weather['precipitation_chance']} mm")
        print(f"- Condition: {weather['condition']}")
    else:
        print("Unable to fetch weather data. Please try again later.")

# Optional: Convert temperature (if needed)
def convert_to_celsius(fahrenheit):
    return round((fahrenheit - 32) * 5 / 9, 2)