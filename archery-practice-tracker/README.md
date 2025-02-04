# Evans Archery Practice Tracker

The **Evans Archery Practice Tracker** is a Python-based tool to log, analyze, and visualize your archery practice data. It also includes weather integration for better performance tracking and features intuitive visualizations to help identify areas for improvement.

---

## Features

### 1. Logging Practice Sessions
- Record practice details such as:
  - Date of session
  - Distance practiced (in yards)
  - Total arrows shot
  - Hits (arrows on target)
  - Accuracy percentage (calculated automatically)
  - Weather data:
    - Temperature
    - Wind speed
    - Chance of precipitation
- Logs are saved to a CSV file for analysis.

### 2. Viewing Practice Statistics
- Aggregates and displays statistics, including:
  - Total arrows shot
  - Overall accuracy
  - Most practiced distances
  - Accuracy trends by date (including weather data)
  - Practice frequency by distance
  - Consistency score
- Export statistics as:
  - JSON file
  - PDF report

### 3. Distance-Based Recommendations
- Highlights distances where average accuracy falls below a threshold (default: 75%).
- Provides actionable insights to focus on problem areas.

### 4. Visualizations
- **Line Chart**: Accuracy trends over time.
- **Bar Chart**: Accuracy by distance.
- Export charts as PNG and PDF.

### 5. Weather Integration
- Fetches current weather data from the **Weather API**.
- Includes:
  - Temperature (Fahrenheit and Celsius)
  - Wind speed
  - Chance of precipitation
  - Detailed forecast
- Logs weather data for each practice session.

---

## Project Structure

```plaintext
archery-practice-tracker/
├── main.py              # Main program logic (menu, user interaction)
├── utils.py             # Shared helper functions (logging, statistics)
├── visualizations.py    # Visualization functions (line/bar charts)
├── weather_utils.py     # Weather-specific functions
├── tests/               # Directory for unit tests -- Moved to main directory. 
│   ├── test_utils.py
│   ├── test_visualizations.py
│   └── test_weather_utils.py
├── data/                # Directory for CSV logs and reports
├── exports/             # Directory for visualization exports
├── requirements.txt     # Python dependencies
├── README.md            # Documentation
```

## Setup Instructions
### 1. Install Dependencies
Ensure you have Python 3 installed. Run the following command to install required libraries:
pip install -r requirements.txt

The requirements.txt has dependencies list so that you have all the needed items to run the program. 

### 2. Set Up Environment Variables
Create a .env file in the project root to store your Weather API key and default location:
WEATHER_API_KEY=your_api_key_here
DEFAULT_LAT=40.2837
DEFAULT_LON=-111.635

### 3. Run the Program
Launch the program using:
python main.py

## Usage
### Main Menu
Upon running the program, you will see the following menu:
```plaintext
--- Archery Practice Tracker ---
1. Log a new practice session
2. View practice statistics
3. View current weather
4. View distance-based recommendations
5. Plot accuracy over time
6. Plot accuracy by distance
7. Quit
```
## Main Menu Breakdown
### 1. Log a New Practice Session
Enter the session date (MM/DD or MM/DD/YYYY format) or press Enter for today.
Enter distance practiced, total arrows shot, and hits.
The program calculates accuracy and logs weather data automatically.
### 2. View Practice Statistics
Displays aggregated statistics such as total arrows, accuracy, and practice frequency.
Option to export the data as JSON or PDF reports.
### 3. View Current Weather
Choose to use the default Timpanogos Archers Club location or enter a custom latitude and longitude.
Displays:
Temperature (Fahrenheit and Celsius)
Wind speed
Chance of precipitation
Detailed forecast
### 4. View Distance-Based Recommendations
Highlights distances where accuracy falls below the set threshold (default: 75%).
Suggests distances to focus on for improvement.
### 5 & 6 View Visualizations
Line Chart: Accuracy trends over time.
Bar Chart: Accuracy by distance.
Option to export charts as PNG and PDF.

### 7. Quit the program 
Goodbye message. 

## Example Output
### Practice Statistics Example
```plaintext
Total arrows shot: 120
Overall accuracy: 87.50%
Most practiced distance(s): 20, 50 yards

Accuracy trend by date:
  2025-01-20: 85.00%
  2025-01-21: 80.00%
  2025-01-22: 90.00%
  2025-01-23: 95.00%

Practice frequency by distance:
  20 yards: 3 sessions
  50 yards: 2 sessions
  30 yards: 1 session
```
### Distance-Based Recommendations Example
```plaintext
--- Distance-Based Recommendations ---
Distance: 20 yards | Avg Accuracy: 85.00% | Status: Good Performance
Distance: 50 yards | Avg Accuracy: 70.00% | Status: Needs Improvement

Distances to Focus On:
  50 yards: 70.00%
```

### Weather Example
```plaintext
Current Weather for 40.2837, -111.635:
- Temperature: 45°F (7°C)
- Wind: 5 mph
- Precipitation Chance: 10%
- Detailed Forecast: Clear skies with light winds.
```
### Visualizations Example:
Line Chart: Accuracy Trends Over Time
Bar Chart: Accuracy by Distance

## Testing
### Unit Tests
pytest -v

Tests cover:
Logging practice sessions
Generating statistics
Visualizations
File export functionality
