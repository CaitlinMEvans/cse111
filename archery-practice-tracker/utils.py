import pandas as pd
import csv
import json
import numpy as np
from fpdf import FPDF
import os
from datetime import datetime
from weather_utils import fetch_weather
import logging

# Define base directory and file path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "data", "session_logs.csv")

# Ensure the "data" directory exists
if not os.path.exists(os.path.join(BASE_DIR, "data")):
    os.makedirs(os.path.join(BASE_DIR, "data"))

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# --- Helper: Parse Date ---
def parse_date(user_input):
    try:
        if "/" in user_input and len(user_input.split("/")) == 3:  # MM/DD/YYYY
            parsed_date = datetime.strptime(user_input, "%m/%d/%Y")
        elif "/" in user_input and len(user_input.split("/")) == 2:  # MM/DD
            current_year = datetime.today().year
            parsed_date = datetime.strptime(f"{user_input}/{current_year}", "%m/%d/%Y")
        else:
            raise ValueError("Invalid date format. Please use MM/DD/YYYY or MM/DD.")
        return parsed_date.strftime("%Y-%m-%d")  # Standard YYYY-MM-DD format
    except ValueError as e:
        print(e)
        return None


# --- Helper: Prompt for Date ---
def prompt_date():
    while True:
        user_date = input("Enter the date (MM/DD or MM/DD/YYYY) or press Enter for today: ").strip()
        if not user_date:
            return datetime.today().strftime("%Y-%m-%d")
        date = parse_date(user_date)
        if date:
            return date


# --- Feature: Logging Practice Sessions ---
def log_practice_session(date, distance, arrows, hits, accuracy, temperature, wind_speed, precipitation):
    """
    Logs a practice session with all details, including weather data, into the CSV file.
    """
    try:
        # Ensure the file exists and has a header
        if not os.path.exists(file_path):
            with open(file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["date", "distance", "arrows", "hits", "accuracy", "temperature", "wind_speed", "precipitation"])

        # Log the session data
        with open(file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([date, distance, arrows, hits, accuracy, temperature, wind_speed, precipitation])

        logging.info(f"Session logged: {date}, {distance} yards, {arrows} arrows, {hits} hits, "
                     f"{accuracy:.2f}% accuracy, {temperature}°F, {wind_speed} mph, {precipitation} mm")
    except Exception as e:
        logging.error(f"Failed to log session: {e}")
        raise RuntimeError(f"An error occurred while logging the session: {e}")


# --- Feature: Logging Practice Session from Terminal ---
def log_practice_session_terminal():
    """
    Logs a practice session via terminal input, calculates weather data, and adds details automatically.
    """
    try:
        # Prompt for date and use the current date if none is provided
        date_input = input("Enter the date (MM/DD/YYYY) or press Enter for today: ").strip()
        if not date_input:
            date = datetime.today().strftime('%Y-%m-%d')  # Default to today's date
        else:
            try:
                date = datetime.strptime(date_input, '%m/%d/%Y').strftime('%Y-%m-%d')
            except ValueError:
                raise ValueError("Invalid date format. Please use MM/DD/YYYY.")

        # Prompt for other details
        distance = int(input("Enter the distance (yards): ").strip())
        arrows = int(input("Enter the total arrows shot: ").strip())
        hits = int(input("Enter the hits on target: ").strip())

        if hits > arrows:
            raise ValueError("Hits cannot exceed total arrows shot.")

        # Prompt for location and fetch weather data
        use_default_location = input("At Timpanogos Archery Club? (y/n): ").strip().lower() == "y"
        location = "40.2837,-111.635" if use_default_location else input("Enter ZIP code: ").strip()
        weather = fetch_weather(location) or {"temperature": "N/A", "wind_speed": "N/A", "precipitation": "N/A"}

        # Calculate accuracy and log the session
        accuracy = (hits / arrows) * 100
        log_practice_session(date, distance, arrows, hits, accuracy, weather["temperature"], weather["wind_speed"], weather["precipitation"])

        print(f"Session logged successfully: {date}, {distance} yards, {arrows} arrows, {hits} hits.")
    except Exception as e:
        print(f"Error logging session: {e}")


# --- Feature: Calculating Statistics ---
def calculate_statistics(gui_mode=False):
    """
    Reads session data from the CSV file, calculates various statistics, and returns them as a dictionary.
    """
    try:
        data = pd.read_csv(file_path)
        if data.empty:
            raise ValueError("No practice sessions logged yet.")

        # Ensure numeric columns are converted correctly
        data["accuracy"] = pd.to_numeric(data["accuracy"], errors="coerce")
        data["temperature"] = pd.to_numeric(data["temperature"], errors="coerce")
        data["wind_speed"] = pd.to_numeric(data["wind_speed"], errors="coerce")
        data["precipitation"] = pd.to_numeric(data["precipitation"], errors="coerce")

        # Calculate core statistics
        total_arrows = data["arrows"].sum()
        total_hits = data["hits"].sum()
        overall_accuracy = (total_hits / total_arrows) * 100
        distance_counts = data["distance"].value_counts()
        most_practiced_distances = distance_counts[distance_counts == distance_counts.max()].index.tolist()

        # Group data for trends and consistency calculations
        accuracy_trends = data.groupby("date").agg({
            "accuracy": "mean",
            "temperature": "mean",
            "wind_speed": "mean",
            "precipitation": "mean"
        }).reset_index()

        # Calculate practice frequency and accuracy by distance
        practice_frequency = data["distance"].value_counts().to_dict()

        accuracy_by_distance = {}
        for distance, group in data.groupby("distance"):
            group_sorted = group.sort_values(by="accuracy", ascending=False)
            most_recent_best = group_sorted.iloc[0]
            avg_by_year = group.groupby(group["date"].str[:4])["accuracy"].mean()
            accuracy_by_distance[distance] = {
                "most_recent_best": (most_recent_best["accuracy"], most_recent_best["date"]),
                "average_by_year": avg_by_year.to_dict()
            }

        # Calculate consistency score (standard deviation of accuracy)
        consistency_score = data["accuracy"].std()

        # Prepare statistics dictionary
        stats = {
            "total_arrows": total_arrows,
            "overall_accuracy": overall_accuracy,
            "most_practiced_distances": most_practiced_distances,
            "accuracy_trends": accuracy_trends.to_dict("records"),
            "practice_frequency": practice_frequency,
            "accuracy_by_distance": accuracy_by_distance,
            "consistency_score": consistency_score
        }

        return stats
    except FileNotFoundError:
        print("Session log file not found. Please log a session first.")
    except Exception as e:
        print(f"An error occurred while calculating statistics: {e}")

def export_terminal(stats):
    """
    Handles exporting statistics to JSON or PDF for terminal users.
    :param stats: The statistics dictionary to export.
    """
    try:
        # Prompt to export statistics to JSON
        export_json = input("\nWould you like to export the statistics to a JSON report? (y/n): ").strip().lower()
        if export_json == "y":
            generate_json_report(stats)
            print("Statistics exported as JSON.")

        # Prompt to export statistics to PDF
        export_pdf = input("Would you like to export the statistics to a PDF report? (y/n): ").strip().lower()
        if export_pdf == "y":
            generate_pdf_report(stats)
            print("Statistics exported as PDF.")
    except Exception as e:
        print(f"An error occurred during export: {e}")


def view_statistics():
    """Fetch and display practice statistics with export options."""
    try:
        stats = calculate_statistics()

        print("\n--- Practice Statistics ---")
        print(f"Total arrows shot: {stats['total_arrows']}")
        print(f"Overall accuracy: {stats['overall_accuracy']:.2f}%")
        print(f"Most practiced distances: {', '.join(map(str, stats['most_practiced_distances']))}")

        print("\nAccuracy Trends by Date:")
        for trend in stats['accuracy_trends']:
            print(f"  {trend['date']}: {trend['accuracy']:.2f}% accuracy")
            print(f"    Weather - Temp: {trend['temperature']:.1f}°F, Wind: {trend['wind_speed']:.1f} mph, Precip: {trend['precipitation']:.1f} mm")

        print("\nPractice Frequency by Distance:")
        for distance, count in stats['practice_frequency'].items():
            print(f"  {distance} yards: {count} sessions")

        print("\nAccuracy by Distance:")
        for distance, details in stats['accuracy_by_distance'].items():
            print(f"  {distance} yards:")
            print(f"    Most Recent Best: {details['most_recent_best'][0]:.2f}% on {details['most_recent_best'][1]}")
            for year, avg in details['average_by_year'].items():
                print(f"    Average for {year}: {avg:.2f}%")

        print(f"\nConsistency score (lower is better): {stats['consistency_score']:.2f}")

        # Prompt to export statistics
        export_json = input("\nWould you like to export the statistics to a JSON report? (y/n): ").strip().lower()
        if export_json == "y":
            generate_json_report(stats)
            print("Statistics exported as JSON.")

        export_pdf = input("Would you like to export the statistics to a PDF report? (y/n): ").strip().lower()
        if export_pdf == "y":
            generate_pdf_report(stats)
            print("Statistics exported as PDF.")

    except FileNotFoundError:
        print("Session log file not found. Please log a session first.")
    except RuntimeError as e:
        print(f"Error: {e}")

def view_statistics():
    """Fetch and display practice statistics with export options."""
    try:
        stats = calculate_statistics()

        print("\n--- Practice Statistics ---")
        print(f"Total arrows shot: {stats['total_arrows']}")
        print(f"Overall accuracy: {stats['overall_accuracy']:.2f}%")
        print(f"Most practiced distances: {', '.join(map(str, stats['most_practiced_distances']))}")

        print("\nAccuracy Trends by Date:")
        for trend in stats['accuracy_trends']:
            print(f"  {trend['date']}: {trend['accuracy']:.2f}% accuracy")
            print(f"    Weather - Temp: {trend['temperature']:.1f}°F, Wind: {trend['wind_speed']:.1f} mph, Precip: {trend['precipitation']:.1f} mm")

        print("\nPractice Frequency by Distance:")
        for distance, count in stats['practice_frequency'].items():
            print(f"  {distance} yards: {count} sessions")

        print("\nAccuracy by Distance:")
        for distance, details in stats['accuracy_by_distance'].items():
            print(f"  {distance} yards:")
            print(f"    Most Recent Best: {details['most_recent_best'][0]:.2f}% on {details['most_recent_best'][1]}")
            for year, avg in details['average_by_year'].items():
                print(f"    Average for {year}: {avg:.2f}%")

        print(f"\nConsistency score (lower is better): {stats['consistency_score']:.2f}")

        # Prompt to export statistics
        export_json = input("\nWould you like to export the statistics to a JSON report? (y/n): ").strip().lower()
        if export_json == "y":
            generate_json_report(stats)
            print("Statistics exported as JSON.")

        export_pdf = input("Would you like to export the statistics to a PDF report? (y/n): ").strip().lower()
        if export_pdf == "y":
            generate_pdf_report(stats)
            print("Statistics exported as PDF.")

    except FileNotFoundError:
        print("Session log file not found. Please log a session first.")
    except RuntimeError as e:
        print(f"Error: {e}")

# --- Feature: Generating a JSON Report ---
def generate_json_report(stats):
    """
    Generates a JSON report of the calculated statistics.
    """
    json_file_path = os.path.join(BASE_DIR, "data", "progress_report.json")

    def convert_types(obj):
        """Convert non-serializable types to serializable ones."""
        if isinstance(obj, (np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()  # Convert numpy arrays to lists
        return obj

    try:
        # Convert the stats dictionary to ensure all values are JSON serializable
        serializable_stats = {key: convert_types(value) for key, value in stats.items()}

        with open(json_file_path, "w") as file:
            json.dump(serializable_stats, file, indent=4)
        print(f"JSON report saved to {json_file_path}")
    except Exception as e:
        print(f"An error occurred while saving the JSON report: {e}")

# --- Feature: Generating a PDF Report ---
def generate_pdf_report(stats):
    """
    Generates a PDF report of the calculated statistics.
    """
    pdf_file_path = os.path.join(BASE_DIR, "data", "progress_report.pdf")
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
    pdf.ln(10)

    # Most practiced distances
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 10, "Most Practiced Distances:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, ", ".join(map(str, stats['most_practiced_distances'])), ln=True)
    pdf.ln(10)

    # Accuracy trends by date
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 10, "Accuracy Trends by Date:", ln=True)
    pdf.set_font("Arial", size=12)
    for trend in stats['accuracy_trends']:
        pdf.cell(0, 10, f"{trend['date']}: {trend['accuracy']:.2f}% accuracy", ln=True)
        pdf.cell(0, 10, f"  Temp: {trend['temperature']}°F, Wind: {trend['wind_speed']} mph, Precip: {trend['precipitation']} mm", ln=True)
    pdf.ln(10)

    # Practice frequency by distance
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 10, "Practice Frequency by Distance:", ln=True)
    pdf.set_font("Arial", size=12)
    for distance, count in stats['practice_frequency'].items():
        pdf.cell(0, 10, f"{distance} yards: {count} sessions", ln=True)
    pdf.ln(10)

    # Accuracy by distance
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 10, "Accuracy by Distance:", ln=True)
    pdf.set_font("Arial", size=12)
    for distance, details in stats['accuracy_by_distance'].items():
        pdf.cell(0, 10, f"{distance} yards:", ln=True)
        pdf.cell(0, 10, f"  Most Recent Best: {details['most_recent_best'][0]:.2f}% on {details['most_recent_best'][1]}", ln=True)
        for year, avg in details['average_by_year'].items():
            pdf.cell(0, 10, f"  Average for {year}: {avg:.2f}%", ln=True)
    pdf.ln(10)

    # Consistency score
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 10, "Consistency Score (lower is better):", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"{stats['consistency_score']:.2f}", ln=True)
    pdf.ln(10)

    # Save PDF
    try:
        pdf.output(pdf_file_path)
        print(f"PDF report saved to {pdf_file_path}")
    except Exception as e:
        print(f"An error occurred while saving the PDF report: {e}")

# --- Feature: Distance-Based Recommendations ---
def recommend_distances(threshold=75, max_distance=100):
    """
    Recommends distances to focus on based on accuracy thresholds.
    """
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