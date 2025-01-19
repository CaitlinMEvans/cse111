# CREATIVITY: made it a little more interative by asking the the user if they want to purchase tires of the entered dimensions and, if so, collect their phone number. 
# If the user does choose to inquire for purchase the number they add is appended to the TXT file. 
# I also updated the user experience if they choose no, then it will ask if htey want to check another tires pressure. 

import math
from datetime import datetime

def main():
    while True:
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

        # Get the current date
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Append the details to the volumes.txt file
        with open("volumes.txt", "a") as file:
            file.write(f"{current_date}, {width}, {aspect_ratio}, {diameter}, {volume:.2f}\n")

        # Ask the user if they want to purchase the tires
        purchase = input("Would you like to purchase tires with these dimensions? (yes/y or no/n): ").strip().lower()
        if purchase in ["yes", "y"]:
            phone_number = input("Please enter your phone number: ")
            with open("volumes.txt", "a") as file:
                file.write(f"Phone number: {phone_number}\n")
            print("Thank you! Your inquiry has been recorded.")

            # Prompt if the user wants to check another tire
            check_another = input("Would you like to check another tire's volume? (yes/y or no/n): ").strip().lower()
            if check_another in ["yes", "y"]:
                continue
            elif check_another in ["no", "n"]:
                print("Goodbye! Thank you for using the tire volume calculator.")
                break
            else:
                print("Invalid input. Exiting program.")
                break
        elif purchase in ["no", "n"]:
            check_another = input("Your inquiry has not been recorded. Would you like to check another tire's volume? (yes/y or no/n): ").strip().lower()
            if check_another in ["yes", "y"]:
                continue
            elif check_another in ["no", "n"]:
                print("Goodbye! Thank you for using the tire volume calculator.")
                break
            else:
                print("Invalid input. Exiting program.")
                break
        else:
            print("Invalid input. Exiting program.")
            break

# Call the main function
if __name__ == "__main__":
    main()
