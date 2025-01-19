import math  # Importing the math module to use the math.ceil() function

# Ask the user for the number of manufactured items
num_items = int(input("Enter the number of items: "))

# Ask the user for the number of items that will be packed per box
items_per_box = int(input("Enter the number of items per box: "))

# Calculate the number of boxes needed using math.ceil
# This ensures we round up to the nearest whole number, even if there's a remainder
num_boxes = math.ceil(num_items / items_per_box)

# Display the result to the user in a clear and meaningful way
print(f"\nFor {num_items} items, packing {items_per_box} items in each box, you will need {num_boxes} boxes.")
