import math

# Define the Function to calculate the volume of a cylinder.
def compute_volume(radius, height):
    return math.pi * radius**2 * height

# Define the Function to calculate the surface area of a cylinder.
def compute_surface_area(radius, height):
    return 2 * math.pi * radius * (radius + height)

# Define the Function to calculate storage efficiency.
def compute_storage_efficiency(radius, height):
    volume = compute_volume(radius, height)
    surface_area = compute_surface_area(radius, height)
    return volume / surface_area

# Define the Function to calculate cost efficiency.
def compute_cost_efficiency(volume, cost):
    return volume / cost

def main():
    # Can Sizes and each can has a name, radius, height, and cost.
    cans = [
        {"name": "#1 Picnic", "radius": 6.83, "height": 10.16, "cost": 0.28},
        {"name": "#1 Tall", "radius": 7.78, "height": 11.91, "cost": 0.43},
        {"name": "#2", "radius": 8.73, "height": 11.59, "cost": 0.45},
        {"name": "#2.5", "radius": 10.32, "height": 11.91, "cost": 0.61},
        {"name": "#3 Cylinder", "radius": 10.79, "height": 17.78, "cost": 0.86},
        {"name": "#5", "radius": 13.02, "height": 14.29, "cost": 0.83},
        {"name": "#6Z", "radius": 5.40, "height": 8.89, "cost": 0.22},
        {"name": "#8Z Short", "radius": 6.83, "height": 7.62, "cost": 0.26},
        {"name": "#10", "radius": 15.72, "height": 17.78, "cost": 1.53},
        {"name": "#211", "radius": 6.83, "height": 12.38, "cost": 0.34},
        {"name": "#300", "radius": 7.62, "height": 11.27, "cost": 0.38},
        {"name": "#303", "radius": 8.10, "height": 11.11, "cost": 0.42},
    ]

    # Variables to keep track of the best cans for storage and cost efficiency.
    best_storage_efficiency = 0
    best_cost_efficiency = 0
    best_storage_can = None
    best_cost_can = None

    # Print a table header.
    print(f"{'Can':<12}{'Storage Efficiency':>20}{'Cost Efficiency':>20}")
    print("-" * 52)

    # Loop through each can to calculate and display its efficiency values.
    for can in cans:
        name = can["name"]  # Get the can's name
        radius = can["radius"]  # Get the radius
        height = can["height"]  # Get the height
        cost = can["cost"]  # Get the cost

        # Calculate the volume, storage efficiency, and cost efficiency for a can.
        volume = compute_volume(radius, height)
        storage_efficiency = compute_storage_efficiency(radius, height)
        cost_efficiency = compute_cost_efficiency(volume, cost)

        # Print the results for the can
        print(f"{name:<12}{storage_efficiency:>20.2f}{cost_efficiency:>20.2f}")

        # Check if this can has the best storage efficiency
        if storage_efficiency > best_storage_efficiency:
            best_storage_efficiency = storage_efficiency
            best_storage_can = name

        # Check if this can has the best cost efficiency
        if cost_efficiency > best_cost_efficiency:
            best_cost_efficiency = cost_efficiency
            best_cost_can = name

    # Priint out the best cans for storage and cost efficiency.
    print("\nBEST Can for Storage Efficiency:")
    print(f"{best_storage_can} with efficiency {best_storage_efficiency:.2f}")

    print("\nBEST Can for Cost Efficiency:")
    print(f"{best_cost_can} with efficiency {best_cost_efficiency:.2f}")

# Call the main function to run everything.
if __name__ == "__main__":
    main()
