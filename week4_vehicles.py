def main():
    """This program allows the user to enter a VIN (Vehicle Identification Number)
    and returns the manufacturer, model, and color of the vehicle associated with it,
    if found in the predefined dictionary.
    """

    # Create a dictionary that contains data about six vehicles.
    # The key for each vehicle in the dictionary is the vehicle's VIN.
    # The value is a list containing details about the vehicle.
    vehicles_dict = {
        # VIN: [year, manufacturer, model, color, eng_design, eng_displace]
        "1J4GL48K4UF993861": [2002, "Jeep", "Liberty", "blue", "V6", 3.7],
        "1YVGF22C8AN381568": [2002, "Mazda", "626", "white", "I4", 2.0],
        "WP0AA0926HG410293": [1987, "Porsche", "924S", "red", "I4", 2.5],
        "5TDZA23CXTU102983": [2006, "Toyota", "Sienna", "gold", "V6", 3.3],
        "1GKKVRED5ZL382610": [2011, "GMC", "Acadia", "charcoal", "V6", 3.5],
        "2T3BF4DV9QR146782": [2012, "Toyota", "RAV 4", "green", "I4", 2.5]
    }

    # Indices for the vehicle details within the dictionary values
    MANUFACTURER_INDEX = 1
    MODEL_INDEX = 2
    COLOR_INDEX = 3

    # Prompt the user for a VIN
    vin = input("Please enter a VIN: ").strip()

    # Check if the VIN exists in the dictionary
    if vin in vehicles_dict:
        # Retrieve the data for the specified VIN
        vehicle_data = vehicles_dict[vin]

        # Extract the manufacturer, model, and color from the vehicle's data
        manufacturer = vehicle_data[MANUFACTURER_INDEX]
        model = vehicle_data[MODEL_INDEX]
        color = vehicle_data[COLOR_INDEX]

        # Display the relevant details about the vehicle
        print(f"Manufacturer: {manufacturer}")
        print(f"Model: {model}")
        print(f"Color: {color}")
    else:
        # Inform the user if the VIN is not in the dictionary
        print(f"{vin} is not in the dictionary.")


# If this file was executed directly, call the main function.
if __name__ == "__main__":
    main()