from week4_chemistry2 import make_periodic_table, compute_molar_mass, sum_protons, get_formula_name, calculate_molecules_from_mass
from week4_formula import parse_formula
from pytest import approx
import pytest


def test_make_periodic_table():
    """Test that make_periodic_table creates a correct dictionary."""
    periodic_table = make_periodic_table()
    assert periodic_table["H"] == ["Hydrogen", 1.00794, 1]
    assert periodic_table["O"] == ["Oxygen", 15.9994, 8]
    assert periodic_table["C"] == ["Carbon", 12.0107, 6]


def test_compute_molar_mass():
    """Test the compute_molar_mass function."""
    periodic_table = make_periodic_table()

    # Test for water (H2O)
    symbol_quantity_list = [["H", 2], ["O", 1]]
    molar_mass = compute_molar_mass(symbol_quantity_list, periodic_table)
    assert molar_mass == approx(18.01528, rel=1e-5)

    # Test for carbon dioxide (CO2)
    symbol_quantity_list = [["C", 1], ["O", 2]]
    molar_mass = compute_molar_mass(symbol_quantity_list, periodic_table)
    assert molar_mass == approx(44.0098, rel=1e-5)

    # Test for methane (CH4)
    symbol_quantity_list = [["C", 1], ["H", 4]]
    molar_mass = compute_molar_mass(symbol_quantity_list, periodic_table)
    assert molar_mass == approx(16.04246, rel=1e-5)


def test_sum_protons():
    """Test the sum_protons function."""
    periodic_table = make_periodic_table()

    # Test for water (H2O)
    symbol_quantity_list = [["H", 2], ["O", 1]]
    total_protons = sum_protons(symbol_quantity_list, periodic_table)
    assert total_protons == 10

    # Test for methane (CH4)
    symbol_quantity_list = [["C", 1], ["H", 4]]
    total_protons = sum_protons(symbol_quantity_list, periodic_table)
    assert total_protons == 10


def test_get_formula_name():
    """Test the get_formula_name function."""
    known_molecules_dict = {
        "H2O": "water",
        "C6H12O6": "glucose",
        "CO2": "carbon dioxide",
    }

    assert get_formula_name("H2O", known_molecules_dict) == "water"
    assert get_formula_name("CO2", known_molecules_dict) == "carbon dioxide"
    assert get_formula_name("XYZ", known_molecules_dict) == "unknown compound"


def test_calculate_molecules_from_mass():
    """Test the calculate_molecules_from_mass function."""
    molar_mass = 18.01528  # Molar mass of water (H2O)
    mass = 36.03  # Mass in grams (2 moles of water)

    num_molecules = calculate_molecules_from_mass(mass, molar_mass)
    expected_num_molecules = 2 * 6.022e23  # 2 moles
    assert num_molecules == approx(expected_num_molecules, rel=1e-4)  # Adjusted tolerance


# Run pytest
pytest.main(["-v", "--tb=line", "-rN", __file__])