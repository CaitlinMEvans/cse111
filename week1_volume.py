#####
# When you physically exercise to strengthen your heart, you
# should maintain your heart rate within a range for at least 20 minutes. To find that range, subtract your age from 220.
# This difference is your maximum heart rate per minute. Your heart simply will not beat faster than this maximum (220 - age).
# When exercising to strengthen your heart, you should keep your heart rate between 65% and 85% of your heart’s maximum rate.

# Importing necessary modules
from datetime import datetime

# Constants for converting percentages to decimals
LOWER_BOUND = 0.65
UPPER_BOUND = 0.85

# Prompt the user for their age
age = int(input("Please enter your age: "))

# Calculate the maximum heart rate
max_heart_rate = 220 - age

# Calculate the target heart rate range
lower_target = int(max_heart_rate * LOWER_BOUND)
upper_target = int(max_heart_rate * UPPER_BOUND)

# Display the target heart rate range to the user
print("\nWhen you exercise to strengthen your heart, you should")
print(f"keep your heart rate between {lower_target} and {upper_target} beats per minute.")

# Additional Exceeding Requirements
# Ask if the user wants to log this data
log_data = input("\nWould you like to save this information? (yes/no): ").strip().lower()

# If they choose to save it, write it to a file
if log_data == "yes":
    # Get the current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Open or create the file "heart_rate_logs.txt" for appending
    with open("heart_rate_logs.txt", "a") as file:
        # Write the user's information to the file
        file.write(f"{current_date}, {age}, {max_heart_rate}, {lower_target}-{upper_target}\n")
    print("Your data has been saved successfully!")
else:
    print("Your data has not been saved. Thank you!")