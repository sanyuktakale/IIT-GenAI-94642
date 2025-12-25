from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model
import os
import requests

# Debug check (optional, but useful)
assert os.getenv("GROQ_API_KEY"), "GROQ_API_KEY not found!"

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="groq"
)

# Input city
city = input("Enter city name: ")

# Weather API
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.getenv('OPENWEATHER_API_KEY')}&units=metric"
response = requests.get(url)
data = response.json()

if data.get("cod") != 200:
    print("Weather API error")
    exit()

weather_info = f"""
City: {city}
Temperature: {data['main']['temp']}°C
Humidity: {data['main']['humidity']}%
Condition: {data['weather'][0]['description']}
Wind Speed: {data['wind']['speed']} m/s
"""

# Ask LLM
prompt = f"Explain this weather in simple English:\n{weather_info}"
result = llm.invoke(prompt)

print("\nWeather Explanation:")
print(result.content)
