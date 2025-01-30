# test_weather_integration.py
import pytest
import requests
from unittest.mock import patch
from weather_utils import fetch_weather, view_current_weather
from unittest.mock import patch, MagicMock


# --- Test: Missing API Key ---
@patch("os.getenv", return_value=None)  # Mock missing API key
@patch("requests.get")  # Patch requests.get to ensure it doesn't interfere
def test_fetch_weather_missing_api_key(mock_get, mock_getenv):
    """Test fetch_weather when API key is missing."""
    # Mock the requests.get response to simulate no API call
    mock_get.return_value.raise_for_status = MagicMock()  # Ensure no actual call happens
    mock_get.return_value.json.return_value = {}  # Simulate an empty response

    # Call the function
    weather = fetch_weather("40.2837,-111.635")

    # Assert that the function returned None due to missing API key
    assert weather is None, "fetch_weather should return None when the API key is missing."
    
# --- Test: API Request Failure ---
@patch("requests.get")
def test_fetch_weather_api_failure(mock_get):
    """Test fetch_weather when the API request fails."""
    mock_get.side_effect = requests.exceptions.RequestException("Connection error")
    weather = fetch_weather("40.2837,-111.635")
    assert weather is None, "fetch_weather should return None on API request failure."

# --- Test: Unexpected JSON Response Structure ---
@patch("requests.get")
def test_fetch_weather_unexpected_json_structure(mock_get):
    """Test fetch_weather when the API response has an unexpected structure."""
    mock_get.return_value.json.return_value = {}  # Empty response
    mock_get.return_value.status_code = 200  # Simulate a successful API call

    weather = fetch_weather("40.2837,-111.635")
    assert weather is None, "fetch_weather should return None for unexpected JSON response structure."

# --- Test: HTTP Error ---
@patch("requests.get")
def test_fetch_weather_http_error(mock_get):
    """Test fetch_weather when the API responds with a non-200 status code."""
    mock_get.return_value.status_code = 404  # Simulate a 404 Not Found error
    mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError

    weather = fetch_weather("40.2837,-111.635")
    assert weather is None, "fetch_weather should return None for HTTP errors."

# --- Test: Fetch Weather with ZIP Code ---
@patch("requests.get")
def test_fetch_weather_with_zipcode(mock_get):
    """Test fetch_weather with a ZIP code instead of coordinates."""
    mock_get.return_value.json.return_value = {
        "current": {
            "temp_f": 60,
            "wind_mph": 10,
            "precip_mm": 2,
            "condition": {"text": "Rainy"}
        }
    }
    mock_get.return_value.status_code = 200

    weather = fetch_weather("84101")  # ZIP code for Salt Lake City, Utah
    assert weather["temperature"] == 60
    assert weather["wind_speed"] == 10
    assert weather["precipitation"] == 2
    assert weather["condition"] == "Rainy"

# --- Test: View Current Weather at Timpanogos ---
@patch("builtins.input", side_effect=["y"])  # Simulate "yes" for practicing at Timpanogos
@patch("weather_utils.fetch_weather")
def test_view_current_weather_at_timpanogos(mock_fetch_weather, mock_input):
    """Test view_current_weather for the default Timpanogos location."""
    mock_fetch_weather.return_value = {
        "temperature": 75,
        "wind_speed": 5,
        "precipitation": 0,
        "condition": "Clear",
        "forecast": "Sunny",
    }

    with patch("builtins.print") as mock_print:
        view_current_weather()
        mock_fetch_weather.assert_called_once_with("40.2837,-111.635")
        output = [call.args[0] for call in mock_print.call_args_list]
        assert "--- Current Weather for Timpanogos Archery Club ---" in output
        assert "Temperature: 75°F" in output
        assert "Wind Speed: 5 mph" in output
        assert "Precipitation: 0 mm" in output
        assert "Condition: Clear" in output
        assert "Forecast: Sunny" in output

# --- Test: Invalid ZIP Code ---
@patch("requests.get")
def test_fetch_weather_invalid_zip(mock_get):
    """Test fetch_weather with an invalid ZIP code."""
    mock_get.return_value.status_code = 400  # Simulate a bad request (invalid ZIP)
    mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError

    weather = fetch_weather("00000")  # Invalid ZIP code
    assert weather is None, "fetch_weather should return None for invalid ZIP codes."

# --- Test: Valid Fetch Weather ---
@patch("requests.get")
def test_fetch_weather(mock_get):
    """Test the fetch_weather function with mocked API response."""
    # Mocked API response
    mock_get.return_value.json.return_value = {
        "current": {
            "temp_f": 75,
            "wind_mph": 5,
            "precip_mm": 0,
            "condition": {"text": "Clear"}
        }
    }
    mock_get.return_value.status_code = 200  # Simulate a successful API call

    # Call the function with mocked data
    weather = fetch_weather("40.2837,-111.635")

    # Assertions to check if the parsed weather data is as expected
    assert weather["temperature"] == 75
    assert weather["wind_speed"] == 5
    assert weather["precipitation"] == 0
    assert weather["condition"] == "Clear"
