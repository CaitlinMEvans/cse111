# Evans Archery Practice Tracker

The **Evans Archery Practice Tracker** is a Python-based tool to log, analyze, and visualize your archery practice data. It also includes weather integration for better performance tracking.

## Features

### 1. Logging Practice Sessions
- Record practice details such as:
  - Date of session
  - Distance practiced (in yards)
  - Total arrows shot
  - Hits (arrows on target)
  - Accuracy percentage (calculated automatically)
- Logs are saved to a CSV file for analysis.

### 2. Viewing Practice Statistics
- Aggregates and displays statistics, including:
  - Total arrows shot
  - Overall accuracy
  - Most practiced distances
  - Accuracy trends by date
  - Practice frequency by distance
  - Consistency score
- Export statistics as:
  - JSON file
  - PDF report

### 3. Weather Integration
- Fetches current weather data from the **National Weather Service (NWS)** API.
- Includes:
  - Temperature (Fahrenheit and Celsius)
  - Wind speed
  - Chance of precipitation
  - Detailed forecast
- Option to log weather data for additional insights.

## Project Structure
```plaintext
archery-practice-tracker/
├── main.py              # Main program logic (menu, user interaction)
├── utils.py             # Shared helper functions (logging, statistics)
├── weather_utils.py     # Weather-specific functions
├── data/                # Directory for CSV logs and reports
├── requirements.txt     # Python dependencies
├── README.md            # Documentation
```

## Setup Instructions

### 1. Install Dependencies
Ensure you have Python 3 installed. Run the following command to install required libraries:
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
Create a `.env` file in the project root to store the default location for weather data:
```
DEFAULT_LAT=40.2837
DEFAULT_LON=-111.635
```

### 3. Run the Program
Launch the program using:
```bash
python main.py
```

## Usage

### Main Menu
Upon running the program, you will see the following menu:
```plaintext
--- Archery Practice Tracker ---
1. Log a new practice session
2. View practice statistics
3. View current weather
4. Quit
```

### 1. Log a New Practice Session
- Enter the session date (MM/DD or MM/DD/YYYY format) or press Enter for today.
- Enter distance practiced, total arrows shot, and hits.
- The program calculates accuracy and saves the session.

### 2. View Practice Statistics
- Displays statistics such as total arrows, accuracy, and practice frequency.
- Option to export the data as JSON or PDF reports.

### 3. View Current Weather
- Choose to use the default Timpanogos Archers Club location or enter a custom latitude and longitude.
- Displays:
  - Temperature (Fahrenheit and Celsius)
  - Wind speed
  - Chance of precipitation
  - Detailed forecast

## Weather Integration
<!-- The program uses the **National Weather Service (NWS)** API for weather data. -->
The program uses the **Weather API** API for weather data.

### Fetching Weather
- Default location: Timpanogos Archers Club (Kyhv Peak Rd, Provo, UT 84604).
- User can enter custom coordinates if practicing elsewhere.

### Logged Weather Data
- Temperature
- Wind speed
- Precipitation chance
- Detailed forecast

## Example Output

### Practice Statistics Example
```plaintext
Total arrows shot: 93
Overall accuracy: 86.02%
Most practiced distance(s): 20, 50, 40 yards

Accuracy trend by date:
  2025-01-01: 83.33%
  2025-01-02: 75.00%
  2025-01-18: 100.00%
  2025-01-19: 93.70%

Practice frequency by distance:
  20 yards: 2 sessions
  50 yards: 2 sessions
  40 yards: 2 sessions
```

### Weather Example
```plaintext
Current Weather for 40.2837, -111.635:
- Temperature: 50°F (10°C)
- Wind: 10 mph
- Precipitation Chance: 20%
- Detailed Forecast: Partly cloudy with a chance of rain.
```

## Contributing
Feel free to contribute to this project by submitting issues or pull requests.

<!-- ## License
This project is licensed under the MIT License. -->