import pandas as pd
import matplotlib.pyplot as plt
import requests
import csv
from datetime import datetime

# --- Feature: Logging Practice Sessions ---
def log_practice_session():
    """
    Prompts the user to log one or more practice sessions. For each session, the user enters:
    - Date (default: today if left blank or reuse the previous date)
    - Distance practiced
    - Total arrows shot
    - Hits (arrows on target)
    Saves the session data to a CSV file and calculates accuracy.
    """
    previous_date = None  # Track the previous date used
    while True:
        # Ask if they want to use the previous date (if applicable)
        if previous_date:
            reuse_date = input(f"Use the same date as the previous session ({previous_date})? (y/n): ").strip().lower()
            if reuse_date == 'y':
                date = previous_date
            else:
                date = input("Enter the date (YYYY-MM-DD) or press Enter for today: ").strip()
                if not date:
                    date = datetime.today().strftime('%Y-%m-%d')  # Default to today
        else:
            date = input("Enter the date (YYYY-MM-DD) or press Enter for today: ").strip()
            if not date:
                date = datetime.today().strftime('%Y-%m-%d')  # Default to today

        # Save the date for reuse
        previous_date = date

        try:
            distance = int(input("Enter the distance practiced (in yards): "))
            arrows = int(input("Enter the total number of arrows shot: "))
            hits = int(input("Enter the number of hits (arrows on target): "))

            # Validate inputs
            if arrows <= 0 or hits < 0 or hits > arrows:
                print("Invalid input: Arrows must be positive, and hits must be between 0 and total arrows.")
                continue

            # Calculate accuracy of arrow hits to total number of arrows 
            accuracy = (hits / arrows) * 100

            # Append data to CSV
            file_path = "data/session_logs.csv"
            with open(file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([date, distance, arrows, hits, round(accuracy, 2)])

            print(f"Session logged: {date}, {distance} yards, {arrows} arrows, {hits} hits, {round(accuracy, 2)}% accuracy")

        except ValueError:
            print("Invalid input: Please enter numeric values for distance, arrows, and hits.")
            continue

        # Ask if the user wants to log another session
        another = input("Would you like to log another session? (y/n): ").strip().lower()
        if another != 'y':
            print("Returning to the main menu...")
            break


# --- Feature: Calculating Statistics ---
def calculate_statistics():
    """
    Reads session data from the CSV file and calculates aggregated statistics,
    including total arrows, overall accuracy, and most practiced distances.
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

        print(f"Total arrows shot: {total_arrows}")
        print(f"Overall accuracy: {overall_accuracy:.2f}%")
        print(f"Most practiced distance(s): {', '.join(map(str, most_practiced_distances))} yards")

    except FileNotFoundError:
        print("No session log file found. Please log a session first.")
    except KeyError as e:
        print(f"Missing column in session log: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- Main Menu ---
if __name__ == "__main__":
    while True:
        print("\n--- Archery Practice Tracker ---")
        print("1. Log a new practice session")
        print("2. View practice statistics")
        print("3. Quit")
        
        choice = input("Enter your choice (1/2/3): ").strip()
        if choice == "1":
            log_practice_session()
        elif choice == "2":
            calculate_statistics()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")