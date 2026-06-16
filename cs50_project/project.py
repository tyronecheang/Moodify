import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPEN_WEATHER_KEY")

def main():
    ...

def get_weather(location):
    ...

def weather_to_bpm(weather):
    ...

def generate_playlist(bpm):
    ...