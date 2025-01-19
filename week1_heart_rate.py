"""
When you physically exercise to strengthen your heart, you
should maintain your heart rate within a range for at least 20
minutes. To find that range, subtract your age from 220. This
difference is your maximum heart rate per minute. Your heart
simply will not beat faster than this maximum (220 - age).
When exercising to strengthen your heart, you should keep your
heart rate between 65% and 85% of your heart’s maximum rate.
"""

# Prompt the user to enter their age
age = int(input("Please enter your age: "))

# Calculate the maximum heart rate by subtracting the age from 220
max_heart_rate = 220 - age

# Calculate the lower and upper bounds of the target heart rate range
# These values are percentages of the maximum heart rate
lower_bound = int(max_heart_rate * 0.65)  # 65% of max heart rate
upper_bound = int(max_heart_rate * 0.85)  # 85% of max heart rate

# Display the results to the user
print("\nWhen you exercise to strengthen your heart, you should")
print(f"keep your heart rate between {lower_bound} and {upper_bound} beats per minute.")
