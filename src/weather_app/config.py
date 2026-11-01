import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")

if not API_KEY:
    raise ValueError(
        "WEATHER_API_KEY is missing. Please check your .env file."
    )

BASE_URL = "https://api.weatherapi.com/v1/current.json"