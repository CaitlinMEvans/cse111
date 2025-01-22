# calculation_utils.py
import math

def calculate_area(radius):
    """
    Calculate the area of a circle given its radius.
    """
    try:
        radius = float(radius)
        if radius < 0:
            raise ValueError("Radius cannot be negative.")
        return math.pi * radius ** 2
    except ValueError as e:
        raise ValueError(f"Invalid input: {e}")
