import os
import requests
from dotenv import load_dotenv

load_dotenv()

open_weather_key = os.getenv("OPEN_WEATHER_KEY")

def main():
    weather = get_weather("Vancouver")

    if weather is None:
        print("City not found or API error")
        return

def get_weather(location):
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": location,
        "appid": open_weather_key,
        "units": "metric"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code != 200:
        return None
    
    return data["weather"][0]["main"]

def weather_to_bpm(weather):
    ...

def generate_playlist(bpm):
    ...