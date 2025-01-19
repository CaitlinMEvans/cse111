# Exceeding the Requirements: 3 of 4 completed
# 1- print a "return by" date within the 30 days by 9pm
# 2- challenge - buy 1 get 1 half off yogurt with the discounted price listed in the totals section
# 3- added coupon at the bottom for one of the items the customer purchased


import csv
from datetime import datetime, timedelta

def read_dictionary(filename, key_column_index):
    dictionary = {}
    try:
        with open(filename, "rt") as csv_file:
            reader = csv.reader(csv_file)
            next(reader)  # Skip the header row
            for row in reader:
                if len(row) > key_column_index:
                    key = row[key_column_index]
                    value = [row[1], float(row[2])]
                    dictionary[key] = value
    except FileNotFoundError:
        print("Oops! It looks like the file is missing. Please check and try again!")
        exit()
    except PermissionError:
        print("Hmm... it seems I can't access the file. Please check the permissions and try again!")
        exit()
    return dictionary

def main():
    try:
        # Read products.csv into a dictionary
        filename = "products.csv"
        products_dict = read_dictionary(filename, 0)

        print("Caitlin's Shop")
        print("----------------------------")

        # Open and process the request.csv file
        request_file = "request.csv"
        subtotal = 0
        total_items = 0
        sales_tax_rate = 0.06
        total_discount = 0

        print("Requested Items")

        with open(request_file, "rt") as csv_file:
            reader = csv.reader(csv_file)
            next(reader)  # Skip the header row

            for row in reader:
                try:
                    product_number = row[0]
                    quantity = int(row[1])

                    if product_number not in products_dict:
                        raise KeyError(product_number)

                    product_info = products_dict[product_number]
                    product_name = product_info[0]
                    product_price = product_info[1]

                    # CHALLENGE: Apply buy-one-get-one-half-off discount for D083
                    if product_number == "D083":
                        discounted_items = quantity // 2
                        full_price_items = quantity - discounted_items
                        discount = discounted_items * (product_price / 2)
                        item_total = full_price_items * product_price + discounted_items * (product_price / 2)
                        total_discount += discount
                    else:
                        item_total = quantity * product_price

                    subtotal += item_total
                    total_items += quantity

                    print(f"{product_name}: {quantity} @ {product_price:.2f} = {item_total:.2f}")

                except KeyError as e:
                    print("It seems there's a mystery product in the order. Let's take a closer look:", e)

        # Calculate totals before printing totals section
        sales_tax = subtotal * sales_tax_rate
        total = subtotal + sales_tax

        # Totals Section 
        print("\n----------------------------")
        print(f"Number of Items: {total_items}")
        # Discount is for buy-one-get-one-half-off discount for D083
        print(f"Discounts: -{total_discount:.2f}")
        print(f"Subtotal: {subtotal:.2f}")
        print(f"Sales Tax: {sales_tax:.2f}")
        print(f"Total: {total:.2f}")
        print("Thank you for shopping at Caitlin's Shop!")

        # Print current date and time
        current_date_and_time = datetime.now()
        print(f"{current_date_and_time:%a %b %d %I:%M:%S %Y}")

        # "return by" date (30 days in the future at 9:00 PM)
        return_by_date = current_date_and_time + timedelta(days=30)
        print(f"30 day Return by: {return_by_date:%a %b %d %Y} @ 09:00 PM")

        # Print a coupon for one of the purchased products
        if products_dict:
            first_product = list(products_dict.values())[0]
            print("\n----------------------------")
            print("Coupon: Get 10% off your next purchase of")
            print(f"{first_product[0]}!")
            print("Valid until:", f"{return_by_date:%a %b %d %Y}")

    except FileNotFoundError as e:
        print("Oops! It looks like a required file is missing. Please check and try again!", e)
    except PermissionError as e:
        print("Hmm... it seems I can't access one of the files. Please check the permissions and try again!", e)

if __name__ == "__main__":
    main()
