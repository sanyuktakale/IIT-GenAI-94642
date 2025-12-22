# news_api.py
import requests
from config import API_KEY, BASE_URL

def get_news(category, country="us", limit=5):
    params = {
        "apiKey": API_KEY,
        "country": country,
        "category": category,
        "pageSize": limit
    }

    response = requests.get(BASE_URL, params=params)
    return response.json()

