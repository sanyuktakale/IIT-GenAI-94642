import requests

API_KEY = "716e2fe84e9281bad398a2b4c1c74870"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

city = input("Enter city name: ")


url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"


response = requests.get(url)
data = response.json()

if data.get("cod") != 200:
    print("City not found or invalid API request")
else:
    print("\nWeather Report:")
    print("City:", data["name"])
    print("Temperature:", data["main"]["temp"], "°C")
    print("Weather:", data["weather"][0]["description"])
    print("Humidity:", data["main"]["humidity"], "%")
    print("Wind Speed:", data["wind"]["speed"], "m/s")
