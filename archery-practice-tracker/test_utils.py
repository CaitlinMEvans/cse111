import pytest
import pandas as pd
import os
from utils import log_practice_session, recommend_distances, calculate_statistics, generate_json_report, generate_pdf_report

# Path to test CSV file
TEST_CSV_PATH = "data/test_session_logs.csv"

# Sample test data
TEST_DATA = [
    ["2025-01-20", 20, 30, 25, 83.33, 50.0, 5.0, 10.0],
    ["2025-01-21", 30, 20, 15, 75.00, 48.0, 4.5, 5.0],
    ["2025-01-22", 50, 10, 7, 70.00, 47.5, 6.0, 0.0],
    ["2025-01-23", 70, 5, 2, 40.00, 45.0, 10.0, 20.0],  # Low accuracy case
]

@pytest.fixture
def setup_test_data():
    """Fixture to create a test CSV file before running tests and remove it after."""
    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame(TEST_DATA, columns=["date", "distance", "arrows", "hits", "accuracy", "temperature", "wind_speed", "precipitation"])
    df.to_csv(TEST_CSV_PATH, index=False)
    yield TEST_CSV_PATH  # Provide the test CSV file path
    os.remove(TEST_CSV_PATH)  # Cleanup after tests

def test_log_practice_session(setup_test_data):
    """Test logging a practice session."""
    date = "2025-01-25"
    distance = 60
    arrows = 15
    hits = 10
    accuracy = 66.67
    temperature = 30.0
    wind_speed = 3.0
    precipitation = 0.5

    log_practice_session(date, distance, arrows, hits, accuracy, temperature, wind_speed, precipitation)

    # Verify entry in CSV
    df = pd.read_csv(TEST_CSV_PATH)
    assert len(df) == 5, "New session was not logged correctly."
    assert df.iloc[-1]["date"] == date, "Date mismatch in logged session."

def test_recommend_distances(setup_test_data):
    """Test distance recommendations based on accuracy thresholds."""
    recommend_distances(threshold=75, max_distance=100)  # Should highlight 70 yards as needing improvement

def test_calculate_statistics(setup_test_data):
    """Test that statistics are calculated correctly without errors."""
    stats = calculate_statistics(gui_mode=True)
    assert "total_arrows" in stats, "Statistics calculation is missing 'total_arrows'."
    assert stats["total_arrows"] == sum([row[2] for row in TEST_DATA]), "Total arrows mismatch."

def test_json_export(setup_test_data):
    """Test exporting statistics as JSON."""
    stats = calculate_statistics(gui_mode=True)
    generate_json_report(stats)
    assert os.path.exists("data/progress_report.json"), "JSON report was not created."

def test_pdf_export(setup_test_data):
    """Test exporting statistics as PDF."""
    stats = calculate_statistics(gui_mode=True)
    generate_pdf_report(stats)
    assert os.path.exists("data/progress_report.pdf"), "PDF report was not created."