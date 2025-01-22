# gui.py
import tkinter as tk
from tkinter import messagebox
from styles import COLORS, FONT_LARGE, FONT_MEDIUM, FONT_SMALL
from calculation_utils import calculate_area

def main():
    """
    Main function to initialize and run the GUI.
    """
    root = tk.Tk()
    root.title("Area of a Circle Calculator")
    root.geometry("400x300")

    # Status bar text variable
    status_text = tk.StringVar(value="Enter a radius to calculate the area.")

    def calculate():
        """
        Calculate the area and update the GUI.
        """
        radius = radius_entry.get()
        try:
            area = calculate_area(radius)
            result_label.config(text=f"Area: {area:.2f} square units", fg=COLORS["success"])
            status_text.set("Calculation successful!")
        except ValueError as e:
            result_label.config(text="", fg=COLORS["error"])
            status_text.set(str(e))

    def clear():
        """
        Clear all inputs and outputs.
        """
        radius_entry.delete(0, tk.END)
        result_label.config(text="")
        status_text.set("Inputs cleared. Enter a radius to calculate the area.")

    # Widgets
    tk.Label(root, text="Radius:", font=FONT_MEDIUM).grid(row=0, column=0, pady=10, padx=10, sticky="w")

    radius_entry = tk.Entry(root, font=FONT_MEDIUM, width=15)
    radius_entry.grid(row=0, column=1, pady=10, padx=10, sticky="w")

    calculate_button = tk.Button(root, text="Calculate", font=FONT_MEDIUM, bg=COLORS["primary"], fg="white", command=calculate)
    calculate_button.grid(row=1, column=0, pady=10, padx=10)

    clear_button = tk.Button(root, text="Clear", font=FONT_MEDIUM, bg=COLORS["secondary"], fg="white", command=clear)
    clear_button.grid(row=1, column=1, pady=10, padx=10)

    result_label = tk.Label(root, text="", font=FONT_LARGE)
    result_label.grid(row=2, column=0, columnspan=2, pady=10)

    status_bar = tk.Label(root, textvariable=status_text, font=FONT_SMALL, bg=COLORS["secondary"], fg="white", anchor="w")
    status_bar.grid(row=3, column=0, columnspan=2, sticky="we")

    # Run the GUI
    root.mainloop()

if __name__ == "__main__":
    main()