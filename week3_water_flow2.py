import math

# Constants
EARTH_ACCELERATION_OF_GRAVITY = 9.8066500  # m/s^2
WATER_DENSITY = 998.2000000  # kg/m^3
WATER_DYNAMIC_VISCOSITY = 0.0010016  # Pa.s

# Pipe specifications
PVC_SCHED80_INNER_DIAMETER = 0.28687 # (meters)  11.294 inches
PVC_SCHED80_FRICTION_FACTOR = 0.013  # (unitless)
SUPPLY_VELOCITY = 1.65               # (meters / second)
HDPE_SDR11_INNER_DIAMETER = 0.048692 # (meters)  1.917 inches
HDPE_SDR11_FRICTION_FACTOR = 0.018   # (unitless)
HOUSEHOLD_VELOCITY = 1.75            # (meters / second)

def water_column_height(tower_height, tank_height):
    """Calculate the water column height based on tower and tank heights."""
    return tower_height + (3 * tank_height) / 4

def pressure_gain_from_water_height(height):
    """Calculate the pressure gain from water height."""
    return (WATER_DENSITY * EARTH_ACCELERATION_OF_GRAVITY * height) / 1000

def pressure_loss_from_pipe(pipe_diameter, pipe_length, friction_factor, fluid_velocity):
    """Calculate and return the pressure loss due to friction within a pipe."""
    return (-friction_factor * pipe_length * WATER_DENSITY * fluid_velocity**2) / (2000 * pipe_diameter)

def pressure_loss_from_fittings(fluid_velocity, quantity_fittings):
    """Calculate pressure loss due to fittings."""
    pressure_loss = (-0.04 * WATER_DENSITY * fluid_velocity**2 * quantity_fittings) / 2000
    return pressure_loss

def reynolds_number(hydraulic_diameter, fluid_velocity):
    """Calculate the Reynolds number for water flowing through a pipe."""
    reynolds = (WATER_DENSITY * hydraulic_diameter * fluid_velocity) / WATER_DYNAMIC_VISCOSITY
    return reynolds

def pressure_loss_from_pipe_reduction(larger_diameter, fluid_velocity, reynolds_number, smaller_diameter):
    """Calculate the pressure loss due to a reduction in pipe diameter."""
    k = 0.1 + ((50 / reynolds_number) * (((larger_diameter / smaller_diameter)**4) - 1))
    pressure_loss = (-k * WATER_DENSITY * fluid_velocity**2) / 2000
    return pressure_loss

def kpa_to_psi(kpa):
    """Convert pressure from kPa to psi."""
    return kpa * 0.145038

def main():
    # Get user inputs for water tower and pipe details
    tower_height = float(input("Height of water tower (meters): "))
    tank_height = float(input("Height of water tank walls (meters): "))
    length1 = float(input("Length of supply pipe from tank to lot (meters): "))
    quantity_angles = int(input("Number of 90° angles in supply pipe: "))
    length2 = float(input("Length of pipe from supply to house (meters): "))

    # Calculate water column height and pressure gain
    water_height = water_column_height(tower_height, tank_height)
    pressure = pressure_gain_from_water_height(water_height)

    # First pipe section calculations
    pressure += pressure_loss_from_pipe(PVC_SCHED80_INNER_DIAMETER, length1, PVC_SCHED80_FRICTION_FACTOR, SUPPLY_VELOCITY)
    pressure += pressure_loss_from_fittings(SUPPLY_VELOCITY, quantity_angles)
    reynolds = reynolds_number(PVC_SCHED80_INNER_DIAMETER, SUPPLY_VELOCITY)
    pressure += pressure_loss_from_pipe_reduction(PVC_SCHED80_INNER_DIAMETER, SUPPLY_VELOCITY, reynolds, HDPE_SDR11_INNER_DIAMETER)

    # Second pipe section calculations
    pressure += pressure_loss_from_pipe(HDPE_SDR11_INNER_DIAMETER, length2, HDPE_SDR11_FRICTION_FACTOR, HOUSEHOLD_VELOCITY)

    # Display final pressure results
    print(f"Pressure at house: {pressure:.1f} kilopascals")
    print(f"Pressure at house: {kpa_to_psi(pressure):.1f} psi")

    # Pressure warning system
    psi_pressure = kpa_to_psi(pressure)
    if psi_pressure < 20:
        print("Warning: The pressure at the house is too low. Consider increasing the tower height or reducing pipe lengths.")
    elif psi_pressure > 80:
        print("Warning: The pressure at the house is too high. Consider decreasing the tower height or using a pressure regulator.")

if __name__ == "__main__":
    main()