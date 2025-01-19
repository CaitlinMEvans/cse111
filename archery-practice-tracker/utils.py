import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import requests
import csv
from datetime import datetime 

# import testing successful - commenting out 
# def test_imports():
#     print("Running import tests...")  # Debugging line to confirm function runs
#     print("Pandas version:", pd.__version__)
#     print("Matplotlib version:", matplotlib.__version__)
#     print("Requests version:", requests.__version__)

# if __name__ == "__main__":
#     print("Starting the script...")  # Debugging line
#     test_imports()

# ############################################################
# Feature: Logging Practice Sessions
# Goal: Allow users to log practice session details, such as:
# Date, Distance practiced, Number of arrows shot, Number of hits (arrows on target), Calculate accuracy automatically
# NOTE: The data will be stored in the session_logs.csv file located in the data/ directory. 
# # ############################################################  

def log_practice_session():
    # Get user inputs
    date = input("Enter the date (YYYY-MM-DD) or press Enter for today: ").strip()
    if not date:
        date = datetime.today().strftime('%Y-%m-%d')  # Default to today

    try:
        distance = int(input("Enter the distance practiced (in yards): "))
        arrows = int(input("Enter the total number of arrows shot: "))
        hits = int(input("Enter the number of hits (arrows on target): "))

        # Validate inputs
        if arrows <= 0 or hits < 0 or hits > arrows:
            print("Invalid input: Arrows must be positive, and hits must be between 0 and total arrows.")
            return

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
    
if __name__ == "__main__":
        log_practice_session()

# # ############################################################  
# Feature: Calculating Statistics

# Goal: Summarize the data in session_logs.csv to provide useful aggregated statistics, such as:
# Total arrows shot: Sum of all arrows shot across all sessions.
# Overall accuracy: Weighted average accuracy across all sessions.
# Most practiced distance: The distance with the highest number of sessions.
# # ############################################################  
def calculate_statistics():
    file_path = "data/session_logs.csv"

    try:
        # Load data into a DataFrame
        data = pd.read_csv(file_path)

        # Check if the file is empty
        if data.empty:
            print("No practice sessions logged yet.")
            return

        # Calculate total arrows
        total_arrows = data["arrows"].sum()

        # Calculate overall accuracy (weighted by arrows)
        total_hits = data["hits"].sum()
        overall_accuracy = (total_hits / total_arrows) * 100

        # Find the most practiced distance
        most_practiced_distance = data["distance"].mode()[0]

        # Display the results
        print(f"Total arrows shot: {total_arrows}")
        print(f"Overall accuracy: {overall_accuracy:.2f}%")
        print(f"Most practiced distance: {most_practiced_distance} yards")

    except FileNotFoundError:
        print("No session log file found. Please log a session first.")
    except KeyError as e:
        print(f"Missing column in session log: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    calculate_statistics()
