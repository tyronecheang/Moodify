from project import weather_to_mood, get_local_time, is_english_song
from datetime import datetime


def test_weather_to_mood_clear_morning():
    time = datetime(2025, 1, 1, 9, 0)
    assert weather_to_mood("Clear", time) == [
        "happy",
        "upbeat",
        "summer",
        "morning"
    ]


def test_weather_to_mood_rain_night():
    time = datetime(2025, 1, 1, 23, 0)
    assert weather_to_mood("Rain", time) == [
        "sad",
        "lofi",
        "melancholy",
        "night"
    ]


def test_weather_to_mood_unknown_weather():
    time = datetime(2025, 1, 1, 14, 0)
    assert weather_to_mood("Fog", time) == [
        "neutral",
        "afternoon"
    ]


def test_get_local_time_utc():
    data = {
        "dt": 0,
        "timezone": 0
    }

    result = get_local_time(data)

    assert result.year == 1970
    assert result.month == 1
    assert result.day == 1
    assert result.hour == 0


def test_get_local_time_positive_offset():
    data = {
        "dt": 0,
        "timezone": 3600
    }

    result = get_local_time(data)

    assert result.hour == 1


def test_is_english_song_true():
    song = {
        "name": "Shape of You",
        "artist": "Ed Sheeran"
    }

    assert is_english_song(song) is True


def test_is_english_song_false():
    song = {
        "name": "夜に駆ける",
        "artist": "YOASOBI"
    }

    assert is_english_song(song) is False