import csv
from datetime import datetime
from pathlib import Path 

# Column names for the weather history CSV file
CSV_COLUMNS = [
    "City",
    "Country",
    "Temperature_Celsius",
    "Weather_Condition",
    "Humidity",
    "Wind_Speed",
    "Lookup_Date_Time",
]

def save_weather_history(
    weather_data: dict,
    file_path: str = "weather_history.csv"
) -> None:
    """Save one successful weather lookup to a CSV file."""

    # Check that the weather data is a dictionary
    if not isinstance(weather_data, dict):
        raise ValueError("Weather data must be a dictionary.")

    # Get location and current weather information
    location = weather_data.get("location")
    current = weather_data.get("current")

    # Check that both sections contain dictionaries
    if not isinstance(location, dict) or not isinstance(current, dict):
        raise ValueError("Weather data is missing location or current details.")
    
        # Get location and current weather information
    location = weather_data.get("location")
    current = weather_data.get("current")

    # Check that both sections contain dictionaries
    if not isinstance(location, dict) or not isinstance(current, dict):
        raise ValueError("Weather data is missing location or current details.")
    
        # Extract the required weather details
    city = location.get("name")
    country = location.get("country")
    temperature = current.get("temp_c")

    condition_data = current.get("condition")
    if not isinstance(condition_data, dict):
        raise ValueError("Weather condition is missing.")

    condition = condition_data.get("text")
    humidity = current.get("humidity")
    wind_speed = current.get("wind_kph")
    
        # Check that text information is present
    if not all(
        isinstance(value, str) and value.strip()
        for value in (city, country, condition)
    ):
        raise ValueError("City, country, or weather condition is missing.")

    # Check that numeric information is present
    if any(value is None or isinstance(value, bool) for value in (
        temperature, humidity, wind_speed
    )):
        raise ValueError("Temperature, humidity, or wind speed is missing.")

    try:
        temperature = float(temperature)
        humidity = float(humidity)
        wind_speed = float(wind_speed)
    except (TypeError, ValueError):
        raise ValueError("Weather measurements must be numeric.")

    if not all(map(lambda value: value == value and abs(value) != float("inf"),
                   (temperature, humidity, wind_speed))):
        raise ValueError("Weather measurements must be finite numbers.")

    if not 0 <= humidity <= 100 or wind_speed < 0:
        raise ValueError("Humidity or wind speed is outside the valid range.")
    
        # Record the current date and time
    lookup_time = datetime.now().astimezone().isoformat(timespec="seconds")
    
        # Prepare one row of weather history
    weather_record = {
        "City": city,
        "Country": country,
        "Temperature_Celsius": temperature,
        "Weather_Condition": condition,
        "Humidity": humidity,
        "Wind_Speed": wind_speed,
        "Lookup_Date_Time": lookup_time,
    }
        # Open the CSV file in append mode
    try:
        with open(file_path, "a", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=CSV_COLUMNS)

            # Write the column headings if the file is empty
            if csv_file.tell() == 0:
                writer.writeheader()

            # Add the new weather record
            writer.writerow(weather_record)

    except OSError as error:
        raise RuntimeError(
            f"Could not save weather history: {error}"
        ) from error