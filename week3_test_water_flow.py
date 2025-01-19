# week3_test_water_flow.py

# Import the pytest module and the functions to be tested
import pytest

from week3_water_flow import (
    pressure_loss_from_fittings,
    reynolds_number,
    pressure_loss_from_pipe_reduction,
)

def test_pressure_loss_from_fittings():
    """Test the pressure loss from fittings function."""
    assert pytest.approx(pressure_loss_from_fittings(0.00, 3), 0.001) == 0.000
    assert pytest.approx(pressure_loss_from_fittings(1.65, 0), 0.001) == 0.000
    assert pytest.approx(pressure_loss_from_fittings(1.65, 2), 0.001) == -0.109
    assert pytest.approx(pressure_loss_from_fittings(1.75, 2), 0.001) == -0.122
    assert pytest.approx(pressure_loss_from_fittings(1.75, 5), 0.001) == -0.306

def test_reynolds_number():
    """Test the Reynolds number function."""
    assert pytest.approx(reynolds_number(0.048692, 0.00), 1) == 0
    assert pytest.approx(reynolds_number(0.048692, 1.65), 1) == 80069
    assert pytest.approx(reynolds_number(0.048692, 1.75), 1) == 84922
    assert pytest.approx(reynolds_number(0.286870, 1.65), 1) == 471729
    assert pytest.approx(reynolds_number(0.286870, 1.75), 1) == 500318

def test_pressure_loss_from_pipe_reduction():
    """Test the pressure loss from pipe reduction function."""
    assert pytest.approx(pressure_loss_from_pipe_reduction(0.28687, 0.00, 1, 0.048692), 0.001) == 0.000
    assert pytest.approx(pressure_loss_from_pipe_reduction(0.28687, 1.65, 471729, 0.048692), 0.001) == -163.744
    assert pytest.approx(pressure_loss_from_pipe_reduction(0.28687, 1.75, 500318, 0.048692), 0.001) == -184.182
