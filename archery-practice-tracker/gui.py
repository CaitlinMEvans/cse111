import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import StringVar, IntVar, messagebox
import os
from utils import (
    log_practice_session,
    calculate_statistics,
    generate_json_report,
    generate_pdf_report,
    recommend_distances,  # Add this if distance recommendations are needed.
)
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

    try:
        log_practice_session(date, distance, arrows, hits)
        messagebox.showinfo("Success", "Session logged successfully!")
        date_var.set("")
        distance_var.set(0)
        arrows_var.set(0)
        hits_var.set(0)
        display_statistics()
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
        stats = calculate_statistics(gui_mode=True)  # Pass gui_mode=True
        formatted_stats = (f"Total arrows shot: {stats['total_arrows']}\n"
                           f"Overall accuracy: {stats['overall_accuracy']:.2f}%\n"
                           f"Most practiced distances: {', '.join(map(str, stats['most_practiced_distances']))}\n")
        stats_text.set(formatted_stats)
    except Exception as e:
        stats_text.set(f"Error fetching statistics: {e}")

def export_statistics(format):
    """Export statistics as JSON or PDF."""
    try:
        stats = calculate_statistics()
        if format == "json":
            generate_json_report(stats)
            messagebox.showinfo("Export Successful", "Statistics exported as JSON.")
        elif format == "pdf":
            generate_pdf_report(stats)
            messagebox.showinfo("Export Successful", "Statistics exported as PDF.")
    except Exception as e:
        messagebox.showerror("Export Failed", f"Failed to export statistics: {e}")

ttk.Label(stats_frame, text="Practice Statistics", style="Header.TLabel").pack(pady=10)
stats_text = StringVar()
stats_label = ttk.Label(stats_frame, textvariable=stats_text, style="TLabel.DarkBlue.TLabel", wraplength=750)
stats_label.pack(pady=10)

ttk.Button(stats_frame, text="Export as JSON", command=lambda: export_statistics("json")).pack(pady=5)
ttk.Button(stats_frame, text="Export as PDF", command=lambda: export_statistics("pdf")).pack(pady=5)

display_statistics()

# --- Weather Tab ---
weather_frame = ttk.Frame(tabs, style="TFrame.DarkBlue.TFrame")
tabs.add(weather_frame, text="Weather")

def display_weather():
    """Fetches and displays current weather data."""
    try:
        use_default_location = messagebox.askyesno("Location", "Are you practicing at the Timpanogos Archery Club?")
        if use_default_location:
            weather = fetch_weather("40.2837,-111.635")
            location = "Timpanogos Archery Club"
        else:
            zipcode = messagebox.askstring("Enter ZIP Code", "Please enter your ZIP code:")
            weather = fetch_weather(zipcode)
            location = f"ZIP Code: {zipcode}"

        if weather:
            weather_text.set(f"Location: {location}\n"
                             f"Temperature: {weather['temperature']}°F\n"
                             f"Wind Speed: {weather['wind_speed']} mph\n"
                             f"Precipitation: {weather['precipitation']} mm\n"
                             f"Condition: {weather['condition']}")
        else:
            weather_text.set("Error fetching weather data. Please try again.")
    except Exception as e:
        weather_text.set(f"Error: {e}")

ttk.Label(weather_frame, text="Current Weather", style="Header.TLabel").pack(pady=10)
weather_text = StringVar()
weather_label = ttk.Label(weather_frame, textvariable=weather_text, style="TLabel.DarkBlue.TLabel", wraplength=750)
weather_label.pack(pady=10)

ttk.Button(weather_frame, text="Refresh Weather", command=display_weather).pack(pady=10)

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
