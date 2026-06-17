import os
import requests
import random
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

load_dotenv()

OPEN_WEATHER_KEY = os.getenv("OPEN_WEATHER_KEY")
LASTFM_KEY = os.getenv("LASTFM_KEY")

def main():
    city = input("City: ").strip()

    if not city:
        print("Please enter a city.")
        return

    weather_data = get_weather(city)

    if weather_data is None:
        print("City not found or API error")
        return

    weather = weather_data["weather"][0]["main"]

    print(f"Weather in {city.title()}: {weather}")

    local_time = get_local_time(weather_data)
    moods = weather_to_mood(weather, local_time)
    playlist = generate_playlist(moods)

    print("\n🎧 Moodify Playlist")

    print(f"🌤️  Based on weather in {city}")
    print(f"🎵 Mood tags: {', '.join(moods)}\n")

    for i, song in enumerate(playlist, 1):
        print(f"{i:02d}. {song['name']} — {song['artist']}")

def get_weather(location):
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": location,
        "appid": OPEN_WEATHER_KEY,
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

def weather_to_mood(weather, time):
    mapping = {
        "Clear": ["happy", "upbeat", "summer"],
        "Clouds": ["calm", "chill"],
        "Rain": ["sad", "lofi", "melancholy"],
        "Drizzle": ["soft", "chill"],
        "Thunderstorm": ["dark", "intense"],
        "Snow": ["peaceful", "winter"]
    }

    moods = mapping.get(weather, ["neutral"])

    hour = time.hour

    if 5 <= hour < 12:
        moods.append("morning")
    elif 12 <= hour < 17:
        moods.append("afternoon")
    elif 17 <= hour < 21:
        moods.append("evening")
    else:
        moods.append("night")

    return moods

def is_english_song(song):
    text = song["name"] + song["artist"]
    return text.isascii()

def get_songs_by_tag(tag):
    url = "http://ws.audioscrobbler.com/2.0/"

    params = {
        "method": "tag.gettoptracks",
        "tag": tag,
        "api_key": LASTFM_KEY,
        "format": "json"
    }

    res = requests.get(url, params=params)
    data = res.json()

    tracks = data.get("tracks", {}).get("track", [])

    random.shuffle(tracks)

    return [
        {
            "name": t["name"],
            "artist": t["artist"]["name"]
        }
        for t in tracks[:10]
    ]

def generate_playlist(moods):
    songs = []

    for mood in moods:
        songs.extend(get_songs_by_tag(mood))

    songs = list({(s["name"], s["artist"]): s for s in songs}.values())
    songs = [s for s in songs if is_english_song(s)]

    random.shuffle(songs)
    return songs[:30]

if __name__ == "__main__":
    main()