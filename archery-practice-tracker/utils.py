import pandas as pd
import csv
from datetime import datetime
from weather_utils import fetch_weather
import logging

# Debug logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- Helper: Parse Date ---
def parse_date(user_input):
    try:
        if '/' in user_input and len(user_input.split('/')) == 3:  # MM/DD/YYYY
            parsed_date = datetime.strptime(user_input, '%m/%d/%Y')
        elif '/' in user_input and len(user_input.split('/')) == 2:  # MM/DD
            current_year = datetime.today().year
            parsed_date = datetime.strptime(f"{user_input}/{current_year}", '%m/%d/%Y')
        else:
            raise ValueError("Invalid date format. Please use MM/DD/YYYY or MM/DD.")
        return parsed_date.strftime('%Y-%m-%d')  # Standard YYYY-MM-DD format
    except ValueError as e:
        print(e)
        return None

# --- Helper: Prompt for Date ---
def prompt_date():
    while True:
        user_date = input("Enter the date (MM/DD or MM/DD/YYYY) or press Enter for today: ").strip()
        if not user_date:
            return datetime.today().strftime('%Y-%m-%d')
        date = parse_date(user_date)
        if date:
            return date

# --- Feature: Logging Practice Sessions ---
def log_practice_session():
    """
    Allows users to log one or more practice sessions.
    Fetches weather data once at the end and appends it to all sessions logged.
    """
    sessions = []  # Temporary storage for sessions logged in this round
    previous_date = None

    while True:
        # Handle date input with reuse option
        if previous_date:
            reuse_date = input(f"Use the same date as the previous session ({previous_date})? (y/n): ").strip().lower()
            if reuse_date == 'y':
                date = previous_date
            else:
                date = prompt_date()
        else:
            date = prompt_date()

        # Save the date for reuse
        previous_date = date

        try:
            # Collect session details
            distance = int(input("Enter the distance practiced (in yards): "))
            arrows = int(input("Enter the total number of arrows shot: "))
            hits = int(input("Enter the number of hits (arrows on target): "))

            if arrows <= 0 or hits < 0 or hits > arrows:
                print("Invalid input: Arrows must be positive, and hits must be between 0 and total arrows.")
                continue

            # Calculate accuracy
            accuracy = (hits / arrows) * 100

            # Add session data to temporary storage
            sessions.append([date, distance, arrows, hits, round(accuracy, 2)])
            print(f"Session recorded: {date}, {distance} yards, {arrows} arrows, {hits} hits, {round(accuracy, 2)}% accuracy")
        except ValueError:
            print("Invalid input: Please enter numeric values for distance, arrows, and hits.")
            continue

        # Option to log another session
        another = input("Would you like to log another session? (y/n): ").strip().lower()
        if another != 'y':
            break

    # Fetch weather data once for all sessions
    use_default_location = input("Are you practicing at the Timpanogos Archery Club? (y/n): ").strip().lower()
    if use_default_location == 'y':
        weather = fetch_weather("40.2837", "-111.635")  # Default club coordinates
    else:
        latitude = input("Enter latitude (e.g., 40.2837): ").strip()
        longitude = input("Enter longitude (e.g., -111.635): ").strip()
        weather = fetch_weather(latitude, longitude)

    if not weather:
        print("Unable to fetch weather data. Proceeding without weather information.")
        weather = {"temperature": "N/A", "wind_speed": "N/A", "precipitation": "N/A"}

    # Append sessions to CSV with weather data
    file_path = "data/session_logs.csv"
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        for session in sessions:
            session.extend([weather['temperature'], weather['wind_speed'], weather['precipitation']])
            writer.writerow(session)

    print("\nAll sessions logged successfully.")
    print(f"Weather: {weather['temperature']}°F, Wind: {weather['wind_speed']} mph, Precipitation: {weather['precipitation']}%")
    print("Returning to the main menu...")

# --- Feature: Calculating Statistics ---
def calculate_statistics():
    file_path = "data/session_logs.csv"

    try:
        data = pd.read_csv(file_path)
        if data.empty:
            print("No practice sessions logged yet.")
            return

        total_arrows = data["arrows"].sum()
        total_hits = data["hits"].sum()
        overall_accuracy = (total_hits / total_arrows) * 100

        most_practiced_distances = data["distance"].value_counts().idxmax()

        print(f"Total arrows shot: {total_arrows}")
        print(f"Overall accuracy: {overall_accuracy:.2f}%")
        print(f"Most practiced distance: {most_practiced_distances} yards")

    except FileNotFoundError:
        print("No session log file found. Please log a session first.")
    except Exception as e:
        print(f"An error occurred: {e}")