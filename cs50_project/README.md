# Moodify

#### Video Demo: https://youtu.be/gyE5n7kR6Zs

#### Description:

Moodify is a Python application that generates a Spotify playlist based on the current weather and local time of a city entered by the user. The project combines multiple APIs to create playlists that match the atmosphere of different weather conditions, such as sunny, rainy, snowy, or cloudy days.

The program uses the OpenWeather API to retrieve the current weather and timezone information for a given city. The weather conditions are then mapped to different moods and times of day. For example, clear weather generates happy and upbeat moods, while rainy weather generates sad and lofi moods. The application also takes into account whether it is morning, afternoon, evening, or night in the selected city.

After determining the appropriate moods, Moodify uses the Last.fm API to retrieve popular songs associated with those mood tags. The program filters out duplicate songs and removes songs with non-English titles or artists to create a cleaner playlist.

Finally, the Spotify Web API is used to search for the songs on Spotify and automatically create a new playlist in the user's Spotify account. The playlist is named using the current date and weather condition, such as "06-18 Clear Moodify".

The program requires four API credentials:

- OpenWeather API key
- Last.fm API key
- Spotify Client ID
- Spotify Client Secret

For convenience, these credentials can either be entered manually when the program starts or stored in a `.env` file. Spotify authentication tokens are cached in a `.spotify_cache` file so that the user does not need to repeatedly authorize the application.

The main functions of the program include:

- `get_weather()` – retrieves weather information for a city.
- `get_local_time()` – converts the API response into the city's local time.
- `weather_to_mood()` – maps weather conditions and time of day to mood tags.
- `generate_playlist()` – creates a list of songs from Last.fm tags.
- `create_spotify_playlist()` – creates and populates a Spotify playlist.

Moodify aims to provide users with a personalized listening experience by connecting music to the atmosphere and mood created by the weather.
