# import pytest
# from unittest.mock import patch
# from gui import app

# @pytest.fixture
# def setup_gui():
#     """Fixture to initialize and clean up the GUI environment."""
#     gui_app = app  # Reference the GUI instance
#     yield gui_app  # Provide it to tests
#     gui_app.quit()  # Ensure the app is closed properly

# @patch("gui.fetch_weather")
# def test_weather_prompt(mock_fetch_weather, setup_gui):
#     """Test that the weather prompt fetches and displays data correctly."""
#     mock_fetch_weather.return_value = {
#         "temperature": 75.0,
#         "wind_speed": 5.0,
#         "precipitation": 0.0,
#         "condition": "Sunny",
#     }

#     # Access weather tab and simulate clicking the refresh button
#     weather_tab = setup_gui.nametowidget("!notebook.!frame2")
#     refresh_button = weather_tab.children["!button"]
#     refresh_button.invoke()

#     # Verify that weather details are updated
#     weather_label = weather_tab.children["!label"]
#     assert "Sunny" in weather_label.cget("text")

# @patch("gui.log_practice_session")
# def test_log_submission(mock_log_practice_session, setup_gui):
#     """Test logging a practice session."""
#     mock_log_practice_session.return_value = None

#     # Fill out form fields
#     log_tab = setup_gui.nametowidget("!notebook.!frame")
#     log_tab.children["!entry"].insert(0, "01/30/2025")  # Date
#     log_tab.children["!entry2"].insert(0, "30")  # Distance
#     log_tab.children["!entry3"].insert(0, "40")  # Arrows
#     log_tab.children["!entry4"].insert(0, "35")  # Hits

#     # Simulate submit button click
#     submit_button = log_tab.children["!button"]
#     submit_button.invoke()

#     # Verify that the log submission was called
#     mock_log_practice_session.assert_called_once()

# @patch("gui.calculate_statistics")
# def test_statistics_display(mock_calculate_statistics, setup_gui):
#     """Test that statistics are displayed correctly."""
#     mock_calculate_statistics.return_value = {
#         "total_arrows": 100,
#         "overall_accuracy": 90.0,
#         "most_practiced_distances": [20, 30],
#         "accuracy_trends": [{"date": "2025-01-30", "accuracy": 95.0}],
#         "practice_frequency": {20: 3, 30: 2},
#         "accuracy_by_distance": {20: {"most_recent_best": (95.0, "2025-01-30")}},
#         "consistency_score": 5.0,
#     }

#     # Access statistics tab and simulate button click
#     stats_tab = setup_gui.nametowidget("!notebook.!frame3")
#     display_button = stats_tab.children["!button"]
#     display_button.invoke()

#     # Verify that statistics are displayed
#     stats_label = stats_tab.children["!label"]
#     assert "Total arrows shot: 100" in stats_label.cget("text")

# @patch("gui.generate_json_report")
# @patch("gui.generate_pdf_report")
# def test_statistics_export(mock_generate_json, mock_generate_pdf, setup_gui):
#     """Test exporting statistics to JSON and PDF."""
#     mock_generate_json.return_value = None
#     mock_generate_pdf.return_value = None

#     # Access export buttons in the statistics tab
#     stats_tab = setup_gui.nametowidget("!notebook.!frame3")
#     json_button = stats_tab.children["!button2"]
#     pdf_button = stats_tab.children["!button3"]

#     json_button.invoke()
#     pdf_button.invoke()

#     # Verify that export functions were called
#     mock_generate_json.assert_called_once()
#     mock_generate_pdf.assert_called_once()