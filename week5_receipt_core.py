import csv


def read_dictionary(filename, key_column_index):
    dictionary = {}
    with open(filename, "rt") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) < 3:  # Ensure the row has all required columns
                print(f"Skipping incomplete row: {row}")
                continue
            key = row[key_column_index]
            # Store product name and price in the dictionary
            value = [row[1], float(row[2])]  # Convert price to float
            dictionary[key] = value
    return dictionary


def main():
    # Read the products.csv file into a dictionary
    filename = "products.csv"
    key_column_index = 0
    products_dict = read_dictionary(filename, key_column_index)

    print("All Products")
    print(products_dict)

    # Open and process the request.csv file
    request_file = "request.csv"
    print("\nRequested Items")
    with open(request_file, "rt") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip the header row
        for row in reader:
            product_number = row[0]
            quantity = int(row[1])
            if product_number in products_dict:
                product_info = products_dict[product_number]
                product_name = product_info[0]
                product_price = product_info[1]
                print(f"{product_name}: {quantity} @ {product_price}")
            else:
                print(f"Product number {product_number} not found in products.csv")


if __name__ == "__main__":
    main()