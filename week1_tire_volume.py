import math

def main():
    # Ask the user to provide the necessary tire details
    width = float(input("Enter the width of the tire in mm (ex 205): "))
    aspect_ratio = float(input("Enter the aspect ratio of the tire (ex 60): "))
    diameter = float(input("Enter the diameter of the wheel in inches (ex 15): "))

    # Perform the calculation for the tire's volume based on the provided inputs
    volume = (
        math.pi * width**2 * aspect_ratio * (width * aspect_ratio + 2540 * diameter)
    ) / 10000000000

    # Share the calculated volume with the user in a clear format
    print(f"The approximate volume is {volume:.2f} liters")

# Call the main function
if __name__ == "__main__":
    main()