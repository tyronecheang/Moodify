import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

load_dotenv()

open_weather_key = os.getenv("OPEN_WEATHER_KEY")

def main():
    weather_data = get_weather("Vancouver")
    print(weather_data["weather"][0]["main"])
    local_time = get_local_time(weather_data)
    low_bpm, high_bpm = weather_to_bpm(weather_data["weather"][0]["main"], local_time)
    print("Low BPM:", low_bpm, "\nHigh BPM:", high_bpm)


    if weather_data is None:
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
    
    return data

def get_local_time(data):
    timestamp = data["dt"]
    offset = data["timezone"]

    return datetime.fromtimestamp(
        timestamp,
        timezone(timedelta(seconds=offset))
    )

def weather_to_bpm(weather, time):
    weather_ranges = {
        "Clear": (120, 140),
        "Clouds": (100, 120),
        "Rain": (80, 100),
        "Drizzle": (85, 105),
        "Thunderstorm": (130, 160),
        "Snow": (70, 90),
    }

    low, high = weather_ranges.get(weather, (90, 110))

    hour = time.hour

    if 5 <= hour < 12:
        low += 10
        high += 10
    elif 17 <= hour < 22:
        low -= 10
        high -= 10
    elif hour >= 22 or hour < 5:
        low -= 20
        high -= 20

    return low, high

def generate_playlist(bpm):
    ...

if __name__ == "__main__":
    main()