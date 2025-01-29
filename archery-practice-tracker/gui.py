import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import StringVar, DoubleVar, IntVar
import os

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
style.map("TButton", background=[("hover", DARK_GREEN)])
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

# Form fields
ttk.Label(log_frame, text="Date (MM/DD/YYYY):", style="TLabel.DarkBlue.TLabel").pack(anchor=W, padx=10, pady=5)
ttk.Entry(log_frame, textvariable=date_var, width=30).pack(padx=10, pady=5)

ttk.Label(log_frame, text="Distance (yards):", style="TLabel.DarkBlue.TLabel").pack(anchor=W, padx=10, pady=5)
ttk.Entry(log_frame, textvariable=distance_var, width=30).pack(padx=10, pady=5)

ttk.Label(log_frame, text="Total Arrows Shot:", style="TLabel.DarkBlue.TLabel").pack(anchor=W, padx=10, pady=5)
ttk.Entry(log_frame, textvariable=arrows_var, width=30).pack(padx=10, pady=5)

ttk.Label(log_frame, text="Hits on Target:", style="TLabel.DarkBlue.TLabel").pack(anchor=W, padx=10, pady=5)
ttk.Entry(log_frame, textvariable=hits_var, width=30).pack(padx=10, pady=5)

# Buttons
def log_session():
    # Logic to log the session
    print(f"Logged: {date_var.get()}, {distance_var.get()} yards, {arrows_var.get()} arrows, {hits_var.get()} hits")

ttk.Button(log_frame, text="Log Session", command=log_session).pack(pady=10)

# --- View Statistics Tab ---
stats_frame = ttk.Frame(tabs, style="TFrame.DarkBlue.TFrame")
tabs.add(stats_frame, text="View Statistics")

ttk.Label(stats_frame, text="Practice Statistics", style="Header.TLabel").pack(pady=10)

def view_stats():
    # Logic to display stats
    print("Displaying stats...")

ttk.Button(stats_frame, text="View Statistics", command=view_stats).pack(pady=10)

# --- Weather Tab ---
weather_frame = ttk.Frame(tabs, style="TFrame.DarkBlue.TFrame")
tabs.add(weather_frame, text="Weather")

ttk.Label(weather_frame, text="Current Weather", style="Header.TLabel").pack(pady=10)

def fetch_weather():
    # Logic to fetch and display weather
    print("Fetching weather...")

ttk.Button(weather_frame, text="Get Weather", command=fetch_weather).pack(pady=10)

# --- Visualizations Tab ---
visualizations_frame = ttk.Frame(tabs, style="TFrame.DarkBlue.TFrame")
tabs.add(visualizations_frame, text="Visualizations")

ttk.Label(visualizations_frame, text="Practice Visualizations", style="Header.TLabel").pack(pady=10)

def show_visualizations():
    # Logic to display visualizations
    print("Showing visualizations...")

ttk.Button(visualizations_frame, text="Show Visualizations", command=show_visualizations).pack(pady=10)

# --- Run the App ---
app.mainloop()