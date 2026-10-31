import requests

api_key = "7ffb1dd65e8d4cf1bad165111263110"

city = input("Enter city name: ")

url = "https://api.weatherapi.com/v1/current.json"

params = {
    "key": api_key,
    "q": city
}

try:
    response = requests.get(url, params=params, timeout=10)

    if response.status_code == 200:
        data = response.json()

        print("\n--- WEATHER REPORT ---")
        print("City:", data["location"]["name"])
        print("Country:", data["location"]["country"])
        print("Temperature:", data["current"]["temp_c"], "°C")
        print("Condition:", data["current"]["condition"]["text"])
        print("Humidity:", data["current"]["humidity"], "%")
        print("Wind Speed:", data["current"]["wind_kph"], "km/h")

    else:
        print("API Error:", response.status_code)
        print(response.text)

except requests.exceptions.RequestException as e:
    print("Connection error:", e)