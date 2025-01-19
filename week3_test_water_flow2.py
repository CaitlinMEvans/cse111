import pytest
from week3_water_flow2 import ( 
    water_column_height,
    pressure_gain_from_water_height,
    pressure_loss_from_fittings,
    reynolds_number,
    pressure_loss_from_pipe,
    pressure_loss_from_pipe_reduction,
    kpa_to_psi,
)

def test_water_column_height():
    """Test the water column height calculation."""
    assert water_column_height(0.0, 0.0) == 0.0
    assert water_column_height(25.0, 0.0) == 25.0
    assert water_column_height(0.0, 10.0) == 7.5
    assert water_column_height(48.3, 12.8) == pytest.approx(57.9, abs=0.001)

def test_pressure_gain_from_water_height():
    """Test the pressure gain from water height calculation."""
    assert pressure_gain_from_water_height(0.0) == pytest.approx(0.000, abs=0.001)
    assert pressure_gain_from_water_height(30.2) == pytest.approx(295.628, abs=0.001)
    assert pressure_gain_from_water_height(50.0) == pytest.approx(489.450, abs=0.001)

def test_pressure_loss_from_fittings():
    """Test the pressure loss from fittings function."""
    assert pressure_loss_from_fittings(0.00, 3) == pytest.approx(0.000, abs=0.001)
    assert pressure_loss_from_fittings(1.65, 0) == pytest.approx(0.000, abs=0.001)
    assert pressure_loss_from_fittings(1.65, 2) == pytest.approx(-0.109, abs=0.001)
    assert pressure_loss_from_fittings(1.75, 5) == pytest.approx(-0.306, abs=0.001)

def test_pressure_loss_from_pipe():
    """Test the pressure loss from pipe function."""
    assert pressure_loss_from_pipe(0.048692, 0.00, 0.018, 1.75) == pytest.approx(0.000, abs=0.001)
    assert pressure_loss_from_pipe(0.048692, 200.00, 0.000, 1.75) == pytest.approx(0.000, abs=0.001)
    assert pressure_loss_from_pipe(0.048692, 200.00, 0.018, 0.00) == pytest.approx(0.000, abs=0.001)
    assert pressure_loss_from_pipe(0.048692, 200.00, 0.018, 1.75) == pytest.approx(-113.008, abs=0.001)
    assert pressure_loss_from_pipe(0.048692, 200.00, 0.018, 1.65) == pytest.approx(-100.462, abs=0.001)
    assert pressure_loss_from_pipe(0.286870, 1000.00, 0.013, 1.65) == pytest.approx(-61.576, abs=0.001)
    assert pressure_loss_from_pipe(0.286870, 1800.75, 0.013, 1.65) == pytest.approx(-110.884, abs=0.001)

def test_reynolds_number():
    """Test the Reynolds number function."""
    assert reynolds_number(0.048692, 0.00) == pytest.approx(0, abs=1)
    assert reynolds_number(0.048692, 1.65) == pytest.approx(80069, abs=1)
    assert reynolds_number(0.286870, 1.75) == pytest.approx(500318, abs=1)

def test_pressure_loss_from_pipe_reduction():
    """Test the pressure loss from pipe reduction function."""
    larger_diameter = 0.286870
    fluid_velocity = 1.65
    reynolds = reynolds_number(0.286870, 1.65)
    smaller_diameter = 0.048692
    result = pressure_loss_from_pipe_reduction(larger_diameter, fluid_velocity, reynolds, smaller_diameter)
    assert result == pytest.approx(-144.312, abs=0.001)

def test_kpa_to_psi():
    """Test the kPa to psi conversion."""
    assert kpa_to_psi(0.0) == pytest.approx(0.0, abs=0.001)
    assert kpa_to_psi(101.325) == pytest.approx(14.696, abs=0.001)
    assert kpa_to_psi(200.0) == pytest.approx(29.007, abs=0.001)

pytest.main(["-v", "--tb=line", "-rN", __file__])
