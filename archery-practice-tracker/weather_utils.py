import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# WeatherAPI Key from .env
WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY")
BASE_URL = "http://api.weatherapi.com/v1/current.json"

def fetch_weather(query):
    """
    Fetch current weather data using WeatherAPI.
    :param query: A string representing a location (latitude/longitude or ZIP code).
    """
    if not WEATHERAPI_KEY:
        print("Error: WeatherAPI key is missing. Please add it to the .env file.")
        return None

    try:
        params = {
            "key": WEATHERAPI_KEY,
            "q": query,
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # Parse and return relevant data
        return {
            "temperature": data["current"].get("temp_f", "N/A"),
            "wind_speed": data["current"].get("wind_mph", "N/A"),
            "precipitation": data["current"].get("precip_mm", 0),
            "condition": data["current"]["condition"].get("text", "N/A"),
            "forecast": data["current"]["condition"].get("text", "No forecast available"),
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    except KeyError as e:
        print(f"Error parsing weather data: Missing key {e}")
        return None

def view_current_weather():
    """
    Asks if the user is at the Timpanogos Archery Club and fetches weather data accordingly.
    """
    # Default coordinates for Timpanogos Archery Club
    default_location = "40.2837,-111.635"

    # Ask the user if they are at the Timpanogos Archery Club
    at_timpanogos = input("Are you practicing at the Timpanogos Archery Club? (y/n): ").strip().lower()

    # Fetch weather data based on the user's answer
    if at_timpanogos == "y":
        weather = fetch_weather(default_location)
        location = "Timpanogos Archery Club"
    else:
        zipcode = input("Enter your ZIP code: ").strip()
        weather = fetch_weather(zipcode)
        location = f"ZIP Code: {zipcode}"

    # Display weather data
    if weather:
        print(f"--- Current Weather for {location} ---")
        print(f"Temperature: {weather['temperature']}°F")
        print(f"Wind Speed: {weather['wind_speed']} mph")
        print(f"Precipitation: {weather['precipitation']} mm")
        print(f"Condition: {weather['condition']}")
        print(f"Forecast: {weather.get('forecast', 'No forecast available')}")
    else:
        print("Unable to fetch weather data. Please try again later.")
