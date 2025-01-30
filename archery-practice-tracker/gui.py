import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import StringVar, IntVar, messagebox
import os
from utils import log_practice_session, calculate_statistics
from weather_utils import fetch_weather
from visualizations import plot_accuracy_over_time, plot_accuracy_by_distance

# Initialize application window
app = ttk.Window(themename="flatly")
app.title("Evans Archery Practice Tracker")
app.geometry("800x600")

# --- Color Palette ---
PRIMARY_COLOR = "#219EBC"
SECONDARY_COLOR = "#023047"
LIGHT_GREEN = "#606C38"
DARK_GREEN = "#283618"
YELLOW = "#FFB703"
ORANGE = "#FB8500"
WHITE = "#FFFFFF"

# --- Styles ---
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10, foreground=WHITE, background=LIGHT_GREEN, bordercolor=WHITE)
style.map("TButton", background=[["hover", DARK_GREEN]])
style.configure("TLabel", font=("Helvetica", 14))
style.configure("TFrame.DarkBlue.TFrame", background=SECONDARY_COLOR)
style.configure("TLabel.DarkBlue.TLabel", background=SECONDARY_COLOR, foreground=WHITE)
style.configure("Header.TLabel", font=("Helvetica", 16, "bold"), background=SECONDARY_COLOR, foreground=YELLOW)

# --- Tabbed Layout ---
tabs = ttk.Notebook(app)
tabs.pack(fill=BOTH, expand=YES, padx=10, pady=10)

# --- Log Session Tab ---
log_frame = ttk.Frame(tabs, style="TFrame.DarkBlue.TFrame")
tabs.add(log_frame, text="Log Session")

ttk.Label(log_frame, text="Log a New Practice Session", style="Header.TLabel").pack(pady=10)

date_var = StringVar()
distance_var = IntVar()
arrows_var = IntVar()
hits_var = IntVar()

def submit_session():
    """Logs the session and clears input fields."""
    date = date_var.get()
    distance = distance_var.get()
    arrows = arrows_var.get()
    hits = hits_var.get()

    if not date or distance <= 0 or arrows <= 0 or hits < 0 or hits > arrows:
        messagebox.showerror("Invalid Input", "Please provide valid input for all fields.")
        return

    # Log session using the existing logic from utils.py
    try:
        log_practice_session(date, distance, arrows, hits)
        messagebox.showinfo("Success", "Session logged successfully!")
        date_var.set("")
        distance_var.set(0)
        arrows_var.set(0)
        hits_var.set(0)
        display_statistics()  # Refresh statistics after logging a session
    except Exception as e:
        messagebox.showerror("Error", f"Failed to log session: {e}")

ttk.Label(log_frame, text="Date (MM/DD/YYYY):", style="TLabel.DarkBlue.TLabel").pack(anchor=W, padx=10, pady=5)
ttk.Entry(log_frame, textvariable=date_var, width=30).pack(padx=10, pady=5)

ttk.Label(log_frame, text="Distance (yards):", style="TLabel.DarkBlue.TLabel").pack(anchor=W, padx=10, pady=5)
ttk.Entry(log_frame, textvariable=distance_var, width=30).pack(padx=10, pady=5)

ttk.Label(log_frame, text="Total Arrows Shot:", style="TLabel.DarkBlue.TLabel").pack(anchor=W, padx=10, pady=5)
ttk.Entry(log_frame, textvariable=arrows_var, width=30).pack(padx=10, pady=5)

ttk.Label(log_frame, text="Hits on Target:", style="TLabel.DarkBlue.TLabel").pack(anchor=W, padx=10, pady=5)
ttk.Entry(log_frame, textvariable=hits_var, width=30).pack(padx=10, pady=5)

ttk.Button(log_frame, text="Submit Session", command=submit_session).pack(pady=10)

# --- View Statistics Tab ---
stats_frame = ttk.Frame(tabs, style="TFrame.DarkBlue.TFrame")
tabs.add(stats_frame, text="View Statistics")

def display_statistics():
    """Fetches and displays statistics in the GUI."""
    try:
        stats = calculate_statistics()
        formatted_stats = (f"Total arrows shot: {stats['total_arrows']}\n"
                           f"Overall accuracy: {stats['overall_accuracy']:.2f}%\n"
                           f"Most practiced distances: {', '.join(map(str, stats['most_practiced_distances']))}\n"
                           f"\nAccuracy Trends by Date:\n")
        for trend in stats['accuracy_trends']:
            formatted_stats += (f"  {trend['date']}: {trend['accuracy']:.2f}% accuracy\n"
                                f"    Weather - Temp: {trend['temperature']:.1f}°F, Wind: {trend['wind_speed']:.1f} mph, Precip: {trend['precipitation']:.1f} mm\n")

        formatted_stats += "\nPractice Frequency by Distance:\n"
        for distance, count in stats['practice_frequency'].items():
            formatted_stats += f"  {distance} yards: {count} sessions\n"

        formatted_stats += "\nAccuracy by Distance:\n"
        for distance, details in stats['accuracy_by_distance'].items():
            formatted_stats += (f"  {distance} yards:\n"
                                f"    Most Recent Best: {details['most_recent_best'][0]:.2f}% on {details['most_recent_best'][1]}\n")
            for year, avg in details['average_by_year'].items():
                formatted_stats += f"    Average for {year}: {avg:.2f}%\n"

        formatted_stats += f"\nConsistency score (lower is better): {stats['consistency_score']:.2f}\n"

        stats_text.set(formatted_stats)
    except Exception as e:
        stats_text.set(f"Error fetching statistics: {e}")

ttk.Label(stats_frame, text="Practice Statistics", style="Header.TLabel").pack(pady=10)
stats_text = StringVar()
stats_label = ttk.Label(stats_frame, textvariable=stats_text, style="TLabel.DarkBlue.TLabel", wraplength=750)
stats_label.pack(pady=10)

ttk.Button(stats_frame, text="Refresh Statistics", command=display_statistics).pack(pady=10)

display_statistics()

# --- Weather Tab ---
weather_frame = ttk.Frame(tabs, style="TFrame.DarkBlue.TFrame")
tabs.add(weather_frame, text="Weather")

def display_weather():
    """Fetches and displays current weather data."""
    try:
        weather = fetch_weather("40.2837", "-111.635")  # Default coordinates
        weather_text.set(f"Temperature: {weather['temperature']}°F\n"
                         f"Wind Speed: {weather['wind_speed']} mph\n"
                         f"Precipitation: {weather['precipitation']}%\n"
                         f"Forecast: {weather['forecast']}")
    except Exception as e:
        weather_text.set(f"Error fetching weather: {e}")

ttk.Label(weather_frame, text="Current Weather", style="Header.TLabel").pack(pady=10)
weather_text = StringVar()
weather_label = ttk.Label(weather_frame, textvariable=weather_text, style="TLabel.DarkBlue.TLabel", wraplength=750)
weather_label.pack(pady=10)

display_weather()

# --- Visualizations Tab ---
visualizations_frame = ttk.Frame(tabs, style="TFrame.DarkBlue.TFrame")
tabs.add(visualizations_frame, text="Visualizations")

def display_visualization(option):
    """Displays the selected visualization."""
    if option == "accuracy_over_time":
        plot_accuracy_over_time()
    elif option == "accuracy_by_distance":
        plot_accuracy_by_distance()

ttk.Label(visualizations_frame, text="Practice Visualizations", style="Header.TLabel").pack(pady=10)

ttk.Button(visualizations_frame, text="Accuracy Over Time", command=lambda: display_visualization("accuracy_over_time")).pack(pady=10)

ttk.Button(visualizations_frame, text="Accuracy by Distance", command=lambda: display_visualization("accuracy_by_distance")).pack(pady=10)

# --- Run the App ---
app.mainloop()