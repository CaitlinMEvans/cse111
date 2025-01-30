import pandas as pd
import csv
import json
from fpdf import FPDF
import numpy as np  # For handling numpy data types
from datetime import datetime
from weather_utils import fetch_weather
import logging
import os

# Define base directory and file path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "data", "session_logs.csv")

# Ensure the "data" directory exists
if not os.path.exists(os.path.join(BASE_DIR, "data")):
    os.makedirs(os.path.join(BASE_DIR, "data"))

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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
        # Handle date input
        if previous_date:
            reuse_date = input(f"Use the same date as the previous session ({previous_date})? (y/n): ").strip().lower()
            if reuse_date == 'y':
                date = previous_date
            else:
                date = prompt_date()
        else:
            date = prompt_date()

        previous_date = date

        try:
            # Collect session details
            distance = int(input("Enter the distance practiced (in yards): "))
            arrows = int(input("Enter the total number of arrows shot: "))
            hits = int(input("Enter the number of hits (arrows on target): "))

            if arrows <= 0 or hits < 0 or hits > arrows:
                print("Invalid input: Arrows must be positive, and hits must be between 0 and total arrows.")
                continue

            # Calculate accuracy and store session
            accuracy = (hits / arrows) * 100
            sessions.append([date, distance, arrows, hits, round(accuracy, 2)])
            print(f"Session recorded: {date}, {distance} yards, {arrows} arrows, {hits} hits, {round(accuracy, 2)}% accuracy")
        except ValueError:
            print("Invalid input: Please enter numeric values for distance, arrows, and hits.")
            continue

        another = input("Would you like to log another session? (y/n): ").strip().lower()
        if another != 'y':
            break

    # Fetch weather data once
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

    # Append sessions to CSV
    try:
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            for session in sessions:
                session.extend([weather['temperature'], weather['wind_speed'], weather['precipitation']])
                writer.writerow(session)
        print(f"All sessions logged successfully to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving the sessions: {e}")


# --- Feature: Generating a JSON Report ---
def generate_json_report(stats):
    """
    Generates a JSON report of the calculated statistics.
    """
    file_path = "data/progress_report.json"

    try:
        with open(file_path, "w") as file:
            json.dump(stats, file, indent=4)
        print(f"JSON report saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving the JSON report: {e}")


# --- Feature: Generating a PDF Report ---
def generate_pdf_report(stats):
    """
    Generates a PDF report of the calculated statistics.
    """
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

    # Save PDF
    try:
        pdf.output(file_path)
        print(f"PDF report saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving the PDF report: {e}")


# --- Feature: Distance-Based Recommendations ---
def recommend_distances(threshold=75, max_distance=100):
    try:
        data = pd.read_csv(file_path)
        data = data[data["distance"] <= max_distance]
        data["accuracy"] = pd.to_numeric(data["accuracy"], errors="coerce")
        avg_accuracy_by_distance = data.groupby("distance")["accuracy"].mean()

        print("\n--- Distance-Based Recommendations ---")
        for distance, avg_accuracy in avg_accuracy_by_distance.items():
            status = "Needs Improvement" if avg_accuracy < threshold else "Good Performance"
            print(f"Distance: {distance} yards | Avg Accuracy: {avg_accuracy:.2f}% | Status: {status}")

        problem_distances = avg_accuracy_by_distance[avg_accuracy_by_distance < threshold]
        if not problem_distances.empty:
            print("\nDistances to Focus On:")
            for distance, avg_accuracy in problem_distances.items():
                print(f"  {distance} yards: {avg_accuracy:.2f}%")
        else:
            print("\nGreat job! All distances are above the accuracy threshold.")

    except FileNotFoundError:
        print("No session log file found. Please log a session first.")
    except Exception as e:
        print(f"An error occurred: {e}")


# --- Feature: Calculating Statistics ---
def calculate_statistics():
    """
    Reads session data from the CSV file, calculates various statistics, and returns them as a dictionary.
    Includes weather data in accuracy trends and provides detailed analysis.
    """
    try:
        # File path setup
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, "data", "session_logs.csv")
        
        # Load and validate data
        data = pd.read_csv(file_path)
        if data.empty:
            raise ValueError("No practice sessions logged yet.")
        
        # Convert data types
        data["accuracy"] = pd.to_numeric(data["accuracy"], errors="coerce")
        data["temperature"] = pd.to_numeric(data["temperature"], errors="coerce")
        data["wind_speed"] = pd.to_numeric(data["wind_speed"], errors="coerce")
        data["precipitation"] = pd.to_numeric(data["precipitation"], errors="coerce")
        
        # Calculate statistics (same as previous implementation)
        total_arrows = data["arrows"].sum()
        total_hits = data["hits"].sum()
        overall_accuracy = (total_hits / total_arrows) * 100
        distance_counts = data["distance"].value_counts()
        most_practiced_distances = distance_counts[distance_counts == distance_counts.max()].index.tolist()
        accuracy_trends = (
            data.groupby("date")
            .agg({
                "accuracy": "mean",
                "temperature": "mean",
                "wind_speed": "mean",
                "precipitation": "mean",
            })
            .reset_index()
        )
        practice_frequency = data["distance"].value_counts().to_dict()
        accuracy_by_distance = {}
        for distance, group in data.groupby("distance"):
            group_sorted = group.sort_values(by="accuracy", ascending=False)
            most_recent_best = group_sorted.iloc[0]
            avg_by_year = group.groupby(group["date"].str[:4])["accuracy"].mean()
            accuracy_by_distance[distance] = {
                "most_recent_best": (most_recent_best["accuracy"], most_recent_best["date"]),
                "average_by_year": avg_by_year.to_dict(),
            }
        consistency_score = data["accuracy"].std()

        # Display statistics in the terminal
        print(f"Total arrows shot: {total_arrows}")
        print(f"Overall accuracy: {overall_accuracy:.2f}%")
        print(f"Most practiced distances: {', '.join(map(str, most_practiced_distances))}")
        print("\nAccuracy Trends by Date:")
        for _, row in accuracy_trends.iterrows():
            print(f"  {row['date']}: {row['accuracy']:.2f}% accuracy")
            print(f"    Weather - Temp: {row['temperature']:.1f}°F, Wind: {row['wind_speed']:.1f} mph, Precip: {row['precipitation']:.1f} mm")
        print("\nPractice Frequency by Distance:")
        for distance, count in practice_frequency.items():
            print(f"  {distance} yards: {count} sessions")
        print("\nAccuracy by Distance:")
        for distance, details in accuracy_by_distance.items():
            print(f"  {distance} yards:")
            print(f"    Most Recent Best: {details['most_recent_best'][0]:.2f}% on {details['most_recent_best'][1]}")
            for year, avg in details["average_by_year"].items():
                print(f"    Average for {year}: {avg:.2f}%")
        print(f"\nConsistency score (lower is better): {consistency_score:.2f}")

        # Prepare statistics dictionary
        stats = {
            "total_arrows": total_arrows,
            "overall_accuracy": overall_accuracy,
            "most_practiced_distances": most_practiced_distances,
            "accuracy_trends": accuracy_trends.to_dict("records"),
            "practice_frequency": practice_frequency,
            "accuracy_by_distance": accuracy_by_distance,
            "consistency_score": consistency_score,
        }

        # Export prompts
        export_json = input("\nWould you like to export the statistics to a JSON report? (y/n): ").strip().lower()
        if export_json == "y":
            generate_json_report(stats)
            print("Statistics exported as JSON.")

        export_pdf = input("Would you like to export the statistics to a PDF report? (y/n): ").strip().lower()
        if export_pdf == "y":
            generate_pdf_report(stats)
            print("Statistics exported as PDF.")

        return stats
    except FileNotFoundError:
        print("Session log file not found. Please log a session first.")
    except Exception as e:
        print(f"An error occurred while calculating statistics: {e}")