import pandas as pd
import matplotlib.pyplot as plt
import os

# File path for session logs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "data", "session_logs.csv")

def plot_accuracy_over_time(export=False):
    """
    Generates a line chart for accuracy trends over time.
    :param export: Boolean, if True, saves the chart as PNG and PDF.
    """
    try:
        data = pd.read_csv(file_path)

        # Ensure the data types are correct
        data["date"] = pd.to_datetime(data["date"], errors="coerce")
        data["accuracy"] = pd.to_numeric(data["accuracy"], errors="coerce")

        if data.empty:
            print("No data available for plotting.")
            return

        # Group by date and calculate average accuracy
        accuracy_trends = data.groupby("date")["accuracy"].mean()

        # Plot the line graph
        plt.figure(figsize=(10, 6))
        plt.plot(accuracy_trends.index, accuracy_trends.values, marker="o", linestyle="-", label="Accuracy (%)")
        plt.title("Accuracy Trends Over Time", fontsize=16)
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Accuracy (%)", fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()

        if export:
            export_path = os.path.join(BASE_DIR, "exports")
            if not os.path.exists(export_path):
                os.makedirs(export_path)
            plt.savefig(os.path.join(export_path, "accuracy_trends.png"))
            plt.savefig(os.path.join(export_path, "accuracy_trends.pdf"))
            print(f"Line chart saved to: {export_path}/accuracy_trends.png and accuracy_trends.pdf")

        plt.show()

    except FileNotFoundError:
        print("No session log file found. Please log a session first.")
    except Exception as e:
        print(f"An error occurred: {e}")

def plot_accuracy_by_distance(export=False):
    """
    Generates a bar chart for accuracy trends by distance.
    :param export: Boolean, if True, saves the chart as PNG and PDF.
    """
    try:
        data = pd.read_csv(file_path)

        # Ensure the data types are correct
        data["distance"] = pd.to_numeric(data["distance"], errors="coerce")
        data["accuracy"] = pd.to_numeric(data["accuracy"], errors="coerce")

        if data.empty:
            print("No data available for plotting.")
            return

        # Group by distance and calculate average accuracy
        accuracy_by_distance = data.groupby("distance")["accuracy"].mean()

        # Plot the bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(accuracy_by_distance.index, accuracy_by_distance.values, color="skyblue")
        plt.title("Accuracy by Distance", fontsize=16)
        plt.xlabel("Distance (yards)", fontsize=12)
        plt.ylabel("Average Accuracy (%)", fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(axis="y")

        if export:
            export_path = os.path.join(BASE_DIR, "exports")
            if not os.path.exists(export_path):
                os.makedirs(export_path)
            plt.savefig(os.path.join(export_path, "accuracy_by_distance.png"))
            plt.savefig(os.path.join(export_path, "accuracy_by_distance.pdf"))
            print(f"Bar chart saved to: {export_path}/accuracy_by_distance.png and accuracy_by_distance.pdf")

        plt.show()

    except FileNotFoundError:
        print("No session log file found. Please log a session first.")
    except Exception as e:
        print(f"An error occurred: {e}")