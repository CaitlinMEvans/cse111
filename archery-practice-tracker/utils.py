import pandas as pd
import csv
from datetime import datetime
from weather_utils import fetch_weather
import logging
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
file_path = os.path.join(BASE_DIR, "data", "session_logs.csv")

if not os.path.exists(os.path.join(BASE_DIR, "data")):
    os.makedirs(os.path.join(BASE_DIR, "data"))


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
import pandas as pd

import pandas as pd
import json
from fpdf import FPDF

def calculate_statistics():
    """
    Reads session data from the CSV file, calculates various statistics, and displays them.
    Offers the option to export the results to JSON and PDF reports.
    """
    file_path = "data/session_logs.csv"

    try:
        data = pd.read_csv(file_path)
        if data.empty:
            print("No practice sessions logged yet.")
            return

        total_arrows = data["arrows"].sum()
        total_hits = data["hits"].sum()
        overall_accuracy = (total_hits / total_arrows) * 100

        distance_counts = data["distance"].value_counts()
        most_practiced_distances = distance_counts[distance_counts == distance_counts.max()].index.tolist()

        accuracy_trends = data.groupby("date")["accuracy"].mean()

        frequency_by_distance = data["distance"].value_counts()
        consistency_score = data["accuracy"].std()

        stats = {
            "total_arrows": total_arrows,
            "overall_accuracy": overall_accuracy,
            "most_practiced_distances": most_practiced_distances,
            "accuracy_trends": accuracy_trends.to_dict(),
            "practice_frequency": frequency_by_distance.to_dict(),
            "consistency_score": consistency_score,
        }

        # Display statistics
        print(f"Total arrows shot: {total_arrows}")
        print(f"Overall accuracy: {overall_accuracy:.2f}%")
        print(f"Most practiced distance(s): {', '.join(map(str, most_practiced_distances))} yards")
        print("\nAccuracy trend by date:")
        for date, accuracy in accuracy_trends.items():
            print(f"  {date}: {accuracy:.2f}%")
        print("\nPractice frequency by distance:")
        for distance, count in frequency_by_distance.items():
            print(f"  {distance} yards: {count} sessions")
        print(f"\nConsistency score (lower is better): {consistency_score:.2f}")

        # Export options
        export_json = input("\nWould you like to export the statistics to a JSON report? (y/n): ").strip().lower()
        if export_json == 'y':
            generate_json_report(stats)

        export_pdf = input("Would you like to export the statistics to a PDF report? (y/n): ").strip().lower()
        if export_pdf == 'y':
            generate_pdf_report(stats)

    except FileNotFoundError:
        print("No session log file found. Please log a session first.")
    except Exception as e:
        print(f"An error occurred: {e}")

# JSON Report Generation
def generate_json_report(stats):
    file_path = "data/progress_report.json"
    try:
        with open(file_path, "w") as file:
            json.dump(stats, file, indent=4)
        print(f"JSON report saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving the JSON report: {e}")

# PDF Report Generation
def generate_pdf_report(stats):
    file_path = "data/progress_report.pdf"
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Header
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt="Archery Practice Tracker Report", ln=True, align="C")
    pdf.ln(10)

    # Overall statistics
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 10, "Overall Statistics:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Total arrows shot: {stats['total_arrows']}", ln=True)
    pdf.cell(0, 10, f"Overall accuracy: {stats['overall_accuracy']:.2f}%", ln=True)
    pdf.cell(0, 10, f"Most practiced distances: {', '.join(map(str, stats['most_practiced_distances']))} yards", ln=True)
    pdf.ln(10)

    # Accuracy trends
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 10, "Accuracy Trends by Date:", ln=True)
    pdf.set_font("Arial", size=12)
    for date, accuracy in stats["accuracy_trends"].items():
        pdf.cell(0, 10, f"  {date}: {accuracy:.2f}%", ln=True)
    pdf.ln(10)

    # Practice frequency
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 10, "Practice Frequency by Distance:", ln=True)
    pdf.set_font("Arial", size=12)
    for distance, count in stats["practice_frequency"].items():
        pdf.cell(0, 10, f"  {distance} yards: {count} sessions", ln=True)
    pdf.ln(10)

    # Consistency score
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 10, f"Consistency score (lower is better): {stats['consistency_score']:.2f}", ln=True)

    # Save the PDF
    try:
        pdf.output(file_path)
        print(f"PDF report saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving the PDF report: {e}")
