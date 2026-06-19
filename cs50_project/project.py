import os
import requests
import random
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from getpass import getpass

load_dotenv()
OPEN_WEATHER_KEY = None
LASTFM_KEY = None
sp = None

def validate_openweather_key(key):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": "London",
        "appid": key
    }

    r = requests.get(url, params=params)
    return r.status_code == 200

def validate_lastfm_key(key):
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "tag.getinfo",
        "tag": "pop",
        "api_key": key,
        "format": "json"
    }

    r = requests.get(url, params=params)
    return r.status_code == 200

def validate_spotify_key(client_id, client_secret):
    try:
        auth_manager = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri="http://127.0.0.1:8888/callback",
            scope="playlist-modify-public playlist-modify-private playlist-read-private",
            cache_path=".spotify_cache",
            show_dialog=True
        )

        sp = spotipy.Spotify(auth_manager=auth_manager)

        sp.current_user()
        return True

    except Exception as e:
        print("Spotify auth error:", e)
        return False

def initialize():
    global OPEN_WEATHER_KEY
    global LASTFM_KEY
    global sp
    print("Please enter your API keys to access Moodify. Your input will be hidden for security purposes.\n")
    while True:
        OPEN_WEATHER_KEY = getpass(
            "https://openweathermap.org" + "\nOpenWeather API Key (Leave blank and tap 'enter' key to use .env): "
        ).strip()

        if not OPEN_WEATHER_KEY:
            OPEN_WEATHER_KEY = os.getenv("OPEN_WEATHER_KEY")

        if OPEN_WEATHER_KEY and validate_openweather_key(OPEN_WEATHER_KEY):
            print("✔ OpenWeather key valid\n")
            break

        print("✖ Invalid or missing OpenWeather key. Try again.\n")

    while True:
        LASTFM_KEY = getpass(
            "https://www.last.fm/api" + "\nLastFM API Key (Leave blank and tap 'enter' key to use .env): "
        ).strip()

        if not LASTFM_KEY:
            LASTFM_KEY = os.getenv("LASTFM_KEY")

        if LASTFM_KEY and validate_lastfm_key(LASTFM_KEY):
            print("✔ LastFM key valid\n")
            break

        print("✖ Invalid or missing LastFM key. Try again.\n")

    while True:
        SPOTIFY_ID_KEY = getpass("https://developer.spotify.com/" + "\nSpotify Client ID (Leave blank and tap 'enter' key to use .env): ").strip()
        
        if not SPOTIFY_ID_KEY:
            SPOTIFY_ID_KEY = os.getenv("SPOTIFY_CLIENT_ID")
        
        SPOTIFY_SECRET_KEY = getpass("Spotify Client Secret (Leave blank and tap 'enter' key to use .env): ").strip()

        if not SPOTIFY_SECRET_KEY:
            SPOTIFY_SECRET_KEY = os.getenv("SPOTIFY_CLIENT_SECRET")
        
        if SPOTIFY_ID_KEY and SPOTIFY_SECRET_KEY and validate_spotify_key(SPOTIFY_ID_KEY, SPOTIFY_SECRET_KEY):
            print("✔ Spotify ID and secret valid\n")
            break

        print("✖ Invalid or missing Spotify ID and/or secret. Try again.\n")

    auth_manager = SpotifyOAuth(
                        client_id=SPOTIFY_ID_KEY,
                        client_secret=SPOTIFY_SECRET_KEY,
                        redirect_uri="http://127.0.0.1:8888/callback",
                        scope="playlist-modify-public playlist-modify-private playlist-read-private",
                        cache_path=".spotify_cache",
                        show_dialog=True
                    )

    sp = spotipy.Spotify(auth_manager=auth_manager)


def main():
    initialize()
    city = input("City: ").strip()

    weather_data = get_weather(city)
    if not weather_data:
        print("✖ City not found or API error")
        return

    weather = weather_data["weather"][0]["main"]
    local_time = get_local_time(weather_data)

    print(f"\n🌤️ Weather: {weather}")

    moods = weather_to_mood(weather, local_time)
    songs = generate_playlist(moods)

    print("\n🎧 Generated Songs:")
    for s in songs:
        print(f"{s['name']} - {s['artist']}")

    print("\n📡 Searching Spotify + creating playlist...")
    create_spotify_playlist(songs, weather)

def get_weather(location):
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": location,
        "appid": OPEN_WEATHER_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Weather API error:", response.text)
        return None

    return response.json()


def get_local_time(data):
    return datetime.fromtimestamp(
        data["dt"],
        timezone(timedelta(seconds=data["timezone"]))
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
    return (song["name"] + song["artist"]).isascii()


def get_songs_by_tag(tag):
    url = "http://ws.audioscrobbler.com/2.0/"

    params = {
        "method": "tag.gettoptracks",
        "tag": tag,
        "api_key": LASTFM_KEY,
        "format": "json"
    }

    res = requests.get(url, params=params)

    if res.status_code != 200:
        return []

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


def search_spotify_track(song):
    query = f"{song['name']} {song['artist']}"
    result = sp.search(q=query, type="track", limit=1)

    items = result.get("tracks", {}).get("items", [])
    if not items:
        return None

    return items[0]["uri"]


def create_spotify_playlist(songs, weather):

    today = datetime.now().strftime("%m-%d")

    playlist = sp.current_user_playlist_create(
        name=f"{today} {weather} Moodify",
        description="Generated by Moodify Based on City and Weather"
    )

    uris = []

    print("\n🔎 Matching songs on Spotify...")

    for s in songs:
        uri = search_spotify_track(s)
        if uri:
            uris.append(uri)
            print("✔", s["name"])
        else:
            print("✖ Not found:", s["name"])

    if not uris:
        print("✖ No songs matched on Spotify")
        return

    sp.playlist_add_items(playlist["id"], uris)

    print("👉 Playlist created:", playlist["name"])


if __name__ == "__main__":
    main()