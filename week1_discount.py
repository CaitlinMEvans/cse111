# Importing the datetime module to access current date and time
from datetime import datetime

# Define the sales tax rate as a constant
SALES_TAX_RATE = 0.06  # 6% sales tax

# Get the current day of the week from the system
current_date_and_time = datetime.now()
day_of_week = current_date_and_time.weekday()

# Uncomment the line below to test specific days (0 = Monday, ..., 6 = Sunday)
# day_of_week = 2  # Simulate Tuesday for testing purposes

# Prompt the user for their subtotal
subtotal = float(input("Please enter the subtotal: "))

# Initialize variables for the discount and total amounts
discount_amount = 0  # Default discount is 0 unless conditions are met

# Core Requirement: Apply discount only if it's Tuesday or Wednesday and subtotal >= $50
if day_of_week in [1, 2]:  # 1 = Tuesday, 2 = Wednesday
    if subtotal >= 50:
        discount_amount = subtotal * 0.10  # Calculate 10% discount
        subtotal -= discount_amount  # Reduce subtotal by discount
        print(f"Discount amount: {discount_amount:.2f}")
    else:
        print("You can save more! Spend at least $50 to receive a 10% discount.")  # Optional messaging

# Compute the sales tax based on the (possibly discounted) subtotal
sales_tax = subtotal * SALES_TAX_RATE

# Compute the total amount due
total = subtotal + sales_tax

# Display the sales tax and total amount to the user
print(f"Sales tax amount: {sales_tax:.2f}")
print(f"Total: {total:.2f}")

# Stretch Change: Encourage spending to qualify for the discount if applicable
if day_of_week in [1, 2] and subtotal + discount_amount < 50:
    additional_needed = 50 - (subtotal + discount_amount)
    print(f"Spend an additional ${additional_needed:.2f} to qualify for the discount!")

# Stretch Change: Allow the user to input multiple items to compute subtotal
subtotal = 0  # Reset subtotal for multiple item entry
print("\nEnter the price and quantity of each item. Type '0' for price to finish.")
while True:
    price = float(input("Enter the price of the item: "))
    if price == 0:
        break  # Exit loop if the user enters 0
    quantity = int(input("Enter the quantity: "))
    subtotal += price * quantity  # Add item total to subtotal

# Recalculate discount, tax, and total for the new subtotal
discount_amount = 0  # Reset discount
if day_of_week in [1, 2] and subtotal >= 50:
    discount_amount = subtotal * 0.10
    subtotal -= discount_amount
    print(f"Discount amount: {discount_amount:.2f}")

sales_tax = subtotal * SALES_TAX_RATE
total = subtotal + sales_tax

# Display the updated results
print(f"Sales tax amount: {sales_tax:.2f}")
print(f"Total: {total:.2f}")