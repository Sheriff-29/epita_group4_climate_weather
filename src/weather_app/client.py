import requests
from .config import API_KEY, BASE_URL


def get_weather(city: str) -> dict:
    """Fetch current weather information for a city."""

    params = {
        "key": API_KEY,
        "q": city,
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as error:
        if response.status_code == 400:
            raise ValueError(f"City not found or invalid: {city}") from error
        raise RuntimeError(f"WeatherAPI error: {error}") from error

    except requests.exceptions.RequestException as error:
        raise RuntimeError(f"Could not connect to WeatherAPI: {error}") from error