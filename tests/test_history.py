
import csv
import tempfile
import unittest
from pathlib import Path

from src.weather_app.history import save_weather_history


# Sample weather data for testing
SAMPLE_WEATHER_DATA = {
    "location": {
        "name": "Paris",
        "country": "France",
    },
    "current": {
        "temp_c": 18.5,
        "condition": {
            "text": "Partly cloudy",
        },
        "humidity": 65,
        "wind_kph": 12.0,
    },
}


class TestWeatherHistory(unittest.TestCase):

    def test_csv_file_is_created(self):
        with tempfile.TemporaryDirectory() as temp_folder:
            csv_path = Path(temp_folder) / "weather_history.csv"

            save_weather_history(SAMPLE_WEATHER_DATA, str(csv_path))

            self.assertTrue(csv_path.exists())

    def test_weather_data_is_saved(self):
        with tempfile.TemporaryDirectory() as temp_folder:
            csv_path = Path(temp_folder) / "weather_history.csv"

            save_weather_history(SAMPLE_WEATHER_DATA, str(csv_path))

            with open(csv_path, newline="", encoding="utf-8") as csv_file:
                reader = csv.DictReader(csv_file)
                records = list(reader)

            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["City"], "Paris")
            self.assertEqual(records[0]["Country"], "France")

    def test_new_record_is_appended(self):
        with tempfile.TemporaryDirectory() as temp_folder:
            csv_path = Path(temp_folder) / "weather_history.csv"

            save_weather_history(SAMPLE_WEATHER_DATA, str(csv_path))
            save_weather_history(SAMPLE_WEATHER_DATA, str(csv_path))

            with open(csv_path, newline="", encoding="utf-8") as csv_file:
                records = list(csv.DictReader(csv_file))

            self.assertEqual(len(records), 2)

    def test_invalid_weather_data_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_folder:
            csv_path = Path(temp_folder) / "weather_history.csv"

            with self.assertRaises(ValueError):
                save_weather_history({}, str(csv_path))

    def test_file_error_is_handled(self):
        with tempfile.TemporaryDirectory() as temp_folder:
            folder_path = Path(temp_folder)

            with self.assertRaises(RuntimeError):
                save_weather_history(SAMPLE_WEATHER_DATA, str(folder_path))
