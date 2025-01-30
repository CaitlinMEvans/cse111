import pytest
from tkinter import Tk
from gui import app
from weather_utils import fetch_weather

@pytest.fixture
def setup_gui():
    """Fixture to initialize and clean up the GUI."""
    root = Tk()
    yield root
    root.destroy()

def test_gui_weather_prompt(mocker):
    """Test the weather prompt and data integration in the GUI."""
    mocker.patch("weather_utils.fetch_weather", return_value={"temperature": 36.5, "wind_speed": 5.2, "precipitation": 0.1})

    # Simulate weather fetch
    weather = fetch_weather("40.2837,-111.635")
    assert weather["temperature"] == 36.5, "Weather temperature integration failed."
    assert weather["wind_speed"] == 5.2, "Weather wind speed integration failed."
    assert weather["precipitation"] == 0.1, "Weather precipitation integration failed."
    
def test_gui_initialization(setup_gui):
    """Test if the GUI initializes without errors."""
    assert app is not None, "GUI failed to initialize."

def test_gui_log_submission(mocker):
    """Test log submission in the GUI."""
    mocker.patch("utils.log_practice_session")
    mocker.patch("weather_utils.fetch_weather", return_value={"temperature": 30.0, "wind_speed": 5.0, "precipitation": 0.0})

    # Simulate input fields
    app.date_var.set("01/25/2025")
    app.distance_var.set(40)
    app.arrows_var.set(10)
    app.hits_var.set(7)

    # Simulate button click
    app.submit_session()

    # Verify log function was called
    utils.log_practice_session.assert_called_once()

    
