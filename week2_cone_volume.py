"""Compute and print the volume of a right circular cone."""
# Import the standard math module so that
# math.pi can be used in this program.
import math

def main():
    """Main function to compute and display cone volumes."""
    # Call the cone_volume function to compute
    # the volume of an example cone.
    ex_radius = 2.8
    ex_height = 3.2
    ex_vol = cone_volume(ex_radius, ex_height)  # Fixed: Pass example values as arguments

    # Print several lines that describe this program.
    print("This program computes the volume of a right")
    print("circular cone. For example, if the radius of a")
    print(f"cone is {ex_radius} and the height is {ex_height},")
    print(f"then the volume is {ex_vol:.1f}")
    print()

    # Get the radius and height of the cone from the user.
    radius = float(input("Please enter the radius of the cone: "))
    height = float(input("Please enter the height of the cone: "))

    # Call the cone_volume function to compute the volume
    # for the radius and height that came from the user.
    vol = cone_volume(radius, height)  # Fixed: Pass user inputs as arguments

    # Print the radius, height, and volume for the user to see.
    print(f"Radius: {radius}")
    print(f"Height: {height}")
    print(f"Volume: {vol:.1f}")

def cone_volume(radius, height):
    """Compute and return the volume of a right circular cone.
    
    Parameters:
      radius: The radius of the cone's base.
      height: The height of the cone.
      
    Return:
      The volume of the cone.
    """
    volume = math.pi * radius**2 * height / 3
    return volume

# Start this program by calling the main function.
main()
