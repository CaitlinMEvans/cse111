import math

# Constants
EARTH_ACCELERATION_OF_GRAVITY = 9.8066500  # m/s^2
WATER_DENSITY = 998.2000000  # kg/m^3
WATER_DYNAMIC_VISCOSITY = 0.0010016  # Pa.s

def pressure_loss_from_fittings(fluid_velocity, quantity_fittings):
    """Calculate pressure loss due to fittings."""
    pressure_loss = (-0.04 * WATER_DENSITY * fluid_velocity**2 * quantity_fittings) / 2000
    return pressure_loss

def reynolds_number(hydraulic_diameter, fluid_velocity):
    """Calculate the Reynolds number for water flowing through a pipe."""
    reynolds = (WATER_DENSITY * hydraulic_diameter * fluid_velocity) / WATER_DYNAMIC_VISCOSITY
    return reynolds

def pressure_loss_from_pipe_reduction(larger_diameter, fluid_velocity, reynolds_number, smaller_diameter):
    """Calculate pressure loss due to pipe reduction."""
    k = 0.1 + (50 / reynolds_number) * ((larger_diameter / smaller_diameter)**4 - 1)
    pressure_loss = (-k * WATER_DENSITY * fluid_velocity**2) / 2000
    return pressure_loss

def kpa_to_psi(kpa):
    """Convert pressure from kPa to psi."""
    return kpa * 0.145038

def main():
    # Inputs
    tower_height = float(input("Height of water tower (meters): "))
    tank_height = float(input("Height of water tank walls (meters): "))
    length1 = float(input("Length of supply pipe from tank to lot (meters): "))
    quantity_angles = int(input("Number of 90° angles in supply pipe: "))
    length2 = float(input("Length of pipe from supply to house (meters): "))
    
    # Calculations
    water_height = tower_height + tank_height
    pressure = WATER_DENSITY * EARTH_ACCELERATION_OF_GRAVITY * water_height / 1000  # in kPa
    diameter = 0.28687  # PVC pipe diameter in meters
    friction = 0.013  # PVC pipe friction factor
    velocity = 1.65  # Supply velocity
    reynolds = reynolds_number(diameter, velocity)
    loss = pressure_loss_from_fittings(velocity, quantity_angles)
    pressure += loss
    loss = pressure_loss_from_pipe_reduction(diameter, velocity, reynolds, 0.048692)
    pressure += loss
    diameter = 0.048692  # Smaller pipe diameter
    friction = 0.018  # HDPE friction factor
    velocity = 1.75  # Household velocity
    pressure += (-friction * WATER_DENSITY * velocity**2 * length2) / 2000
    
    # Output
    print(f"Pressure at house: {pressure:.1f} kilopascals")
    print(f"Pressure at house: {kpa_to_psi(pressure):.1f} psi")

if __name__ == "__main__":
    main()