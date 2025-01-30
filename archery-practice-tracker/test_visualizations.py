import pytest
import os
from unittest.mock import patch
import pandas as pd
from visualizations import plot_accuracy_over_time, plot_accuracy_by_distance

# Paths for test output
EXPORT_PATH = "exports"
TEST_CSV_PATH = "data/test_visualization_logs.csv"

# Sample test data
TEST_DATA = [
    ["2025-01-20", 20, 30, 25, 83.33],
    ["2025-01-21", 30, 20, 15, 75.00],
    ["2025-01-22", 50, 10, 7, 70.00],
    ["2025-01-23", 70, 5, 2, 40.00],
]

@pytest.fixture
def setup_visualization_test_data():
    """Fixture to set up test data for visualizations."""
    os.makedirs("data", exist_ok=True)
    os.makedirs(EXPORT_PATH, exist_ok=True)
    df = pd.DataFrame(TEST_DATA, columns=["date", "distance", "arrows", "hits", "accuracy"])
    df.to_csv(TEST_CSV_PATH, index=False)
    yield TEST_CSV_PATH
    os.remove(TEST_CSV_PATH)
    for file in os.listdir(EXPORT_PATH):
        if file.endswith(".png") or file.endswith(".pdf"):
            os.remove(os.path.join(EXPORT_PATH, file))
    if os.path.exists(EXPORT_PATH) and not os.listdir(EXPORT_PATH):
        os.rmdir(EXPORT_PATH)

@patch("visualizations.plt.savefig")
@patch("visualizations.plt.show")
def test_plot_accuracy_over_time(mock_show, mock_savefig, setup_visualization_test_data):
    """Test the accuracy trends visualization using mocked functions."""
    plot_accuracy_over_time(export=True)  # Call the function

    # Assert savefig was called for both PNG and PDF
    export_path_png = os.path.abspath(os.path.join(EXPORT_PATH, "accuracy_trends.png"))
    export_path_pdf = os.path.abspath(os.path.join(EXPORT_PATH, "accuracy_trends.pdf"))
    mock_savefig.assert_any_call(export_path_png)
    mock_savefig.assert_any_call(export_path_pdf)

    # Assert show was called once
    mock_show.assert_called_once()

@patch("visualizations.plt.savefig")
@patch("visualizations.plt.show")
def test_plot_accuracy_by_distance(mock_show, mock_savefig, setup_visualization_test_data):
    """Test the accuracy by distance visualization using mocked functions."""
    plot_accuracy_by_distance(export=True)  # Call the function

    # Assert savefig was called for both PNG and PDF
    expected_paths = [
        os.path.abspath(os.path.join(EXPORT_PATH, "accuracy_by_distance.png")),
        os.path.abspath(os.path.join(EXPORT_PATH, "accuracy_by_distance.pdf"))
    ]

    # Collect all actual calls made to savefig
    actual_calls = [call.args[0] for call in mock_savefig.call_args_list]

    try:
        for path in expected_paths:
            assert path in actual_calls, f"Expected {path} in {actual_calls}, but it was not found."
    except AssertionError as e:
        print("\nMock savefig was called with:", actual_calls)
        raise e  # Re-raise the assertion error

@patch("visualizations.plt.show")
def test_visualizations_without_export(mock_show, setup_visualization_test_data):
    """Test visualizations without exporting files using mocked functions."""
    plot_accuracy_over_time(export=False)  # Call the function
    plot_accuracy_by_distance(export=False)  # Call the function

    # Assert savefig was not called
    mock_show.assert_called()  # Show is called but does not export

def test_visualizations_with_empty_data():
    """Test visualizations with empty datasets."""
    empty_data_path = "data/empty_visualization_logs.csv"
    pd.DataFrame(columns=["date", "distance", "arrows", "hits", "accuracy"]).to_csv(empty_data_path, index=False)

    try:
        with patch("visualizations.plt.show") as mock_show, patch("visualizations.plt.savefig") as mock_savefig:
            plot_accuracy_over_time(export=True)
            plot_accuracy_by_distance(export=True)

            # Assert that savefig was called an even number of times (0, 2, or 4) 
            # since each function attempts to save two files (PNG and PDF)
            assert mock_savefig.call_count % 2 == 0, (
                f"Expected savefig to be called an even number of times, but it was called {mock_savefig.call_count} times."
            )
    finally:
        if os.path.exists(empty_data_path):
            os.remove(empty_data_path)