import pytest
import os
import json
import pandas as pd
import numpy as np
from unittest.mock import patch, mock_open, MagicMock
from utils import (
    log_practice_session,
    calculate_statistics,
    recommend_distances,
    generate_json_report,
    generate_pdf_report,
    view_statistics,
    export_terminal
)

# Set up test paths
TEST_CSV_PATH = os.path.join("data", "test_session_logs.csv")
TEST_JSON_PATH = os.path.join("data", "test_progress_report.json")
TEST_PDF_PATH = os.path.join("data", "test_progress_report.pdf")


# --- Test: Logging a Practice Session ---
@patch("builtins.open", new_callable=mock_open)
@patch("utils.csv.writer")
def test_log_practice_session(mock_csv_writer, mock_open_file):
    """Test that logging a practice session correctly writes data."""
    log_practice_session("2025-01-30", 30, 40, 35, 87.5, 75, 5, 0)

    expected_file_path = os.path.abspath(os.path.join("data", "session_logs.csv"))
    actual_file_path = mock_open_file.call_args[0][0]  # Get the actual file path used

    assert os.path.abspath(actual_file_path) == expected_file_path, f"Expected {expected_file_path}, but got {actual_file_path}."
    mock_csv_writer.assert_called_once()


# --- Test: Calculating Statistics ---
@patch("pandas.read_csv")
def test_calculate_statistics(mock_read_csv):
    """Test that statistics calculation correctly processes session data."""
    mock_data = pd.DataFrame({
        "date": ["2025-01-30", "2025-01-31"],
        "distance": [30, 40],
        "arrows": [40, 30],
        "hits": [35, 25],
        "accuracy": [87.5, 83.3],
        "temperature": [70, 75],
        "wind_speed": [5, 3],
        "precipitation": [0, 0]
    })

    mock_read_csv.return_value = mock_data

    stats = calculate_statistics()

    assert stats["total_arrows"] == 70
    assert stats["overall_accuracy"] > 85
    assert stats["most_practiced_distances"] == [30, 40]
    assert isinstance(stats["accuracy_trends"], list)
    assert "accuracy_by_distance" in stats


# --- Test: Exporting JSON Report ---
@patch("builtins.open", new_callable=mock_open)
def test_generate_json_report(mock_open_file):
    """Test that the JSON report is correctly created."""
    stats = {"total_arrows": 100, "overall_accuracy": 90.0}
    generate_json_report(stats)

    expected_file_path = os.path.abspath(os.path.join("data", "progress_report.json"))
    actual_file_path = os.path.abspath(mock_open_file.call_args[0][0])

    assert actual_file_path == expected_file_path, f"Expected {expected_file_path}, but got {actual_file_path}."


# --- Test: Exporting PDF Report ---
@patch("utils.FPDF")
def test_generate_pdf_report(mock_fpdf):
    """Test that the PDF report is correctly generated with all updated statistics."""
    # Mock statistics dictionary with all required keys
    stats = {
        "total_arrows": 243,
        "overall_accuracy": 82.72,
        "most_practiced_distances": [10, 20, 30],
        "accuracy_trends": [
            {"date": "2025-02-01", "accuracy": 85.0, "temperature": 50, "wind_speed": 10, "precipitation": 0},
            {"date": "2025-02-02", "accuracy": 95.0, "temperature": 55, "wind_speed": 8, "precipitation": 1},
        ],
        "practice_frequency": {10: 5, 20: 3, 30: 2},
        "accuracy_by_distance": {
            10: {
                "most_recent_best": (95.0, "2025-02-02"),
                "average_by_year": {"2025": 85.0},
            },
            20: {
                "most_recent_best": (90.0, "2025-02-01"),
                "average_by_year": {"2025": 80.0},
            },
        },
        "consistency_score": 5.2,
    }

    # Call the function to test
    generate_pdf_report(stats)

    # Ensure the PDF object is created and methods are called correctly
    mock_fpdf.assert_called_once()
    pdf_instance = mock_fpdf.return_value
    pdf_instance.add_page.assert_called()
    pdf_instance.set_font.assert_called()

    # Verify specific calls for PDF content
    pdf_instance.cell.assert_any_call(0, 10, "Overall Statistics:", ln=True)
    pdf_instance.cell.assert_any_call(0, 10, "Total arrows shot: 243", ln=True)
    pdf_instance.cell.assert_any_call(0, 10, "Overall accuracy: 82.72%", ln=True)
    pdf_instance.cell.assert_any_call(0, 10, "Most Practiced Distances:", ln=True)
    pdf_instance.cell.assert_any_call(0, 10, "10, 20, 30", ln=True)
    pdf_instance.cell.assert_any_call(0, 10, "Accuracy Trends by Date:", ln=True)
    pdf_instance.cell.assert_any_call(0, 10, "2025-02-01: 85.0% accuracy", ln=True)
    pdf_instance.cell.assert_any_call(0, 10, "  Temp: 50°F, Wind: 10 mph, Precip: 0 mm", ln=True)
    pdf_instance.cell.assert_any_call(0, 10, "Practice Frequency by Distance:", ln=True)
    pdf_instance.cell.assert_any_call(0, 10, "10 yards: 5 sessions", ln=True)
    pdf_instance.cell.assert_any_call(0, 10, "Accuracy by Distance:", ln=True)
    pdf_instance.cell.assert_any_call(0, 10, "10 yards:", ln=True)
    pdf_instance.cell.assert_any_call(0, 10, "  Most Recent Best: 95.0% on 2025-02-02", ln=True)
    pdf_instance.cell.assert_any_call(0, 10, "Consistency score (lower is better): 5.20", ln=True)

    # Resolve full path for output verification
    expected_pdf_path = os.path.abspath(os.path.join("data", "progress_report.pdf"))
    pdf_instance.output.assert_called_once_with(expected_pdf_path)


# --- Test: Viewing Statistics ---
@patch("utils.generate_json_report")
@patch("utils.generate_pdf_report")
@patch("utils.calculate_statistics")
def test_view_statistics(mock_calculate_statistics, mock_generate_pdf, mock_generate_json):
    """Test that viewing statistics retrieves data and offers export options."""
    mock_calculate_statistics.return_value = {
        "total_arrows": 100,
        "overall_accuracy": 85.5,
        "most_practiced_distances": [20, 30],
        "accuracy_trends": [
            {
                "date": "2025-01-30",
                "accuracy": 90.0,
                "temperature": 70.0,
                "wind_speed": 5.0,
                "precipitation": 0.0
            }
        ],
        "practice_frequency": {20: 3, 30: 2},
        "accuracy_by_distance": {
            20: {
                "most_recent_best": (95.0, "2025-01-30"),
                "average_by_year": {"2025": 92.5}
            },
            30: {
                "most_recent_best": (85.0, "2025-01-30"),
                "average_by_year": {"2025": 80.0}
            }
        },
        "consistency_score": 5.0
    }

    with patch("builtins.input", side_effect=["y", "y"]):  # Simulate "Yes" for both export prompts
        view_statistics()

    mock_calculate_statistics.assert_called_once()
    mock_generate_json.assert_called_once_with(mock_calculate_statistics.return_value)
    mock_generate_pdf.assert_called_once_with(mock_calculate_statistics.return_value)

# --- Test: Exporting Statistics in Terminal ---
@patch("utils.generate_json_report")
@patch("utils.generate_pdf_report")
def test_export_terminal(mock_generate_pdf, mock_generate_json):
    """Test that export prompts handle JSON and PDF generation correctly."""
    stats = {
        "total_arrows": 100,
        "overall_accuracy": 85.5,
        "most_practiced_distances": [20, 30]
    }

    with patch("builtins.input", side_effect=["y", "y"]):  # Simulate "Yes" for both exports
        export_terminal(stats)

    mock_generate_json.assert_called_once_with(stats)
    mock_generate_pdf.assert_called_once_with(stats)


# --- Test: Distance-Based Recommendations ---
@patch("pandas.read_csv")
def test_recommend_distances(mock_read_csv):
    """Test that distance-based recommendations function correctly."""
    mock_data = pd.DataFrame({
        "distance": [20, 30, 40],
        "accuracy": [80, 70, 50]
    })

    mock_read_csv.return_value = mock_data

    with patch("builtins.print") as mock_print:
        recommend_distances()

    mock_read_csv.assert_called_once()

    # Verify expected output
    output = [call.args[0] for call in mock_print.call_args_list]
    assert "Distance: 20 yards | Avg Accuracy: 80.00% | Status: Good Performance" in output
    assert "Distance: 30 yards | Avg Accuracy: 70.00% | Status: Needs Improvement" in output
    assert "Distance: 40 yards | Avg Accuracy: 50.00% | Status: Needs Improvement" in output
