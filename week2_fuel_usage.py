def main():
    """Main function to handle user input and display results."""
    # Get the starting odometer value in miles.
    start_miles = float(input("Enter the first odometer reading (miles): "))
    # Get the ending odometer value in miles.
    end_miles = float(input("Enter the second odometer reading (miles): "))
    # Get the amount of fuel used in gallons.
    amount_gallons = float(input("Enter the amount of fuel used (gallons): "))
    
    # Call the miles_per_gallon function to compute mpg.
    mpg = miles_per_gallon(start_miles, end_miles, amount_gallons)
    # Call the lp100k_from_mpg function to convert mpg to liters per 100 kilometers.
    lp100k = lp100k_from_mpg(mpg)
    
    # Display the results.
    print(f"{mpg:.1f} miles per gallon")
    print(f"{lp100k:.2f} liters per 100 kilometers")


def miles_per_gallon(start_miles, end_miles, amount_gallons):
    """
    Compute and return the average number of miles
    that a vehicle traveled per gallon of fuel.
    Parameters:
      start_miles: An odometer value in miles.
      end_miles: Another odometer value in miles.
      amount_gallons: A fuel amount in U.S. gallons.
    Return:
      Fuel efficiency in miles per gallon.
    """
    # Calculate the miles traveled.
    miles_traveled = end_miles - start_miles
    # Calculate and return the miles per gallon.
    return miles_traveled / amount_gallons


def lp100k_from_mpg(mpg):
    """
    Convert miles per gallon to liters per 100 kilometers
    and return the converted value.
    Parameters:
      mpg: A value in miles per gallon.
    Return:
      The converted value in liters per 100 kilometers.
    """
    # Conversion factor: 1 mile per gallon equals 235.215 liters per 100 km.
    return 235.215 / mpg


# Call the main function to start the program.
main()
