import pytest
import os
import pandas as pd
from visualizations import plot_accuracy_over_time, plot_accuracy_by_distance

# Paths for test output
TEST_CSV_PATH = "data/test_visualization_logs.csv"
EXPORT_PATH = "exports"  # Directory for exported plots

# Sample test data for visualizations
TEST_DATA = [
    ["2025-01-20", 20, 30, 25, 83.33],
    ["2025-01-21", 30, 20, 15, 75.00],
    ["2025-01-22", 50, 10, 7, 70.00],
    ["2025-01-23", 70, 5, 2, 40.00],  # Low accuracy case
]

@pytest.fixture
def setup_visualization_test_data():
    """Fixture to create a test CSV file before running tests and clean up after."""
    os.makedirs("data", exist_ok=True)
    os.makedirs(EXPORT_PATH, exist_ok=True)  # Ensure export directory exists
    df = pd.DataFrame(TEST_DATA, columns=["date", "distance", "arrows", "hits", "accuracy"])
    df.to_csv(TEST_CSV_PATH, index=False)
    yield TEST_CSV_PATH
    os.remove(TEST_CSV_PATH)  # Cleanup after tests
    # Remove exported files if they exist
    for file in os.listdir(EXPORT_PATH):
        if file.endswith(".png") or file.endswith(".pdf"):
            os.remove(os.path.join(EXPORT_PATH, file))

def test_plot_accuracy_over_time(setup_visualization_test_data):
    """Test if accuracy trends visualization is created without errors."""
    print("\nTesting Accuracy Trends Visualization...\n")
    plot_accuracy_over_time(export=True)  # No file path needed, as it's hardcoded in the function

    # Verify that the PNG and PDF files were created
    assert os.path.exists(os.path.join(EXPORT_PATH, "accuracy_trends.png")), "PNG Accuracy Trends plot was not created."
    assert os.path.exists(os.path.join(EXPORT_PATH, "accuracy_trends.pdf")), "PDF Accuracy Trends plot was not created."

def test_plot_accuracy_by_distance(setup_visualization_test_data):
    """Test if accuracy by distance visualization is created without errors."""
    print("\nTesting Accuracy by Distance Visualization...\n")
    plot_accuracy_by_distance(export=True)  # No file path needed, as it's hardcoded in the function

    # Verify that the PNG and PDF files were created
    assert os.path.exists(os.path.join(EXPORT_PATH, "accuracy_by_distance.png")), "PNG Accuracy by Distance plot was not created."
    assert os.path.exists(os.path.join(EXPORT_PATH, "accuracy_by_distance.pdf")), "PDF Accuracy by Distance plot was not created."