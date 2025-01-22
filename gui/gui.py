# gui.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from styles import COLORS, FONT_LARGE, FONT_MEDIUM, FONT_SMALL
from calculation_utils import calculate_area

def main():
    """
    Main function to initialize and run the GUI.
    """
    root = tk.Tk()
    root.title("Area of a Circle Calculator")
    root.geometry("450x300")
    root.configure(bg=COLORS["background"])

    # Status bar text variable
    status_text = tk.StringVar(value="Enter a radius to calculate the area.")

    # Styling for ttk widgets
    style = ttk.Style()
    style.configure(
        "TButton",
        font=FONT_MEDIUM,
        padding=6,
        background=COLORS["primary"],
        foreground="black",
    )
    style.map("TButton", background=[("active", COLORS["secondary"])])

    def calculate():
        """
        Calculate the area and update the GUI.
        """
        radius = radius_entry.get()
        try:
            area = calculate_area(radius)
            result_label.config(
                text=f"Area: {area:.2f} square units", fg=COLORS["success"]
            )
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
    tk.Label(
        root,
        text="Radius:",
        font=FONT_MEDIUM,
        bg=COLORS["background"],
    ).grid(row=0, column=0, pady=10, padx=10, sticky="e")

    radius_entry = tk.Entry(
        root,
        font=FONT_MEDIUM,
        width=15,
        relief="solid",
        bd=1,
        highlightbackground=COLORS["entry_border"],
        highlightcolor=COLORS["secondary"],
        highlightthickness=2,
    )
    radius_entry.grid(row=0, column=1, pady=10, padx=10, sticky="w")

    calculate_button = ttk.Button(root, text="Calculate", command=calculate)
    calculate_button.grid(row=1, column=0, pady=10, padx=10)

    clear_button = ttk.Button(root, text="Clear", command=clear)
    clear_button.grid(row=1, column=1, pady=10, padx=10)

    result_label = tk.Label(
        root,
        text="",
        font=FONT_LARGE,
        bg=COLORS["background"],
        fg=COLORS["success"],
    )
    result_label.grid(row=2, column=0, columnspan=2, pady=10)

    status_bar = tk.Label(
        root,
        textvariable=status_text,
        font=FONT_SMALL,
        bg=COLORS["secondary"],
        fg="white",
        anchor="w",
    )
    status_bar.grid(row=3, column=0, columnspan=2, sticky="we")

    # Run the GUI
    root.mainloop()

if __name__ == "__main__":
    main()