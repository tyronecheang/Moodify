# Moodify

#### Video Demo: https://youtu.be/OPJTMdkzRTo

#### Description:

Moodify is a Python application that generates a personalized Spotify playlist based on the current weather and local time of a city entered by the user. The project combines multiple APIs and services to create playlists that match the atmosphere of different weather conditions, such as sunny, rainy, snowy, or cloudy days. The goal of the project is to connect music with the emotions and moods that people often associate with different types of weather.

The program begins by prompting the user to provide API credentials. For convenience and security, the credentials can either be entered manually at runtime or loaded automatically from a `.env` file. The application validates the provided API keys before allowing the user to continue, ensuring that the program does not fail later because of invalid credentials.

Once initialization is complete, the user is prompted to enter the name of a city. The application uses the OpenWeather API to retrieve the city's current weather information and timezone data. This allows the program to determine not only the weather condition but also the local time in that specific location.

The weather condition is then mapped to one or more mood tags. For example, clear weather generates moods such as "happy", "upbeat", and "summer", while rainy weather generates moods like "sad", "lofi", and "melancholy". In addition to the weather, the program also considers the local time and appends a time-of-day mood such as "morning", "afternoon", "evening", or "night". This combination allows the generated playlist to better reflect the atmosphere of the chosen city.

After determining the appropriate mood tags, Moodify uses the Last.fm API to retrieve popular songs associated with each mood. Since multiple tags can return duplicate songs, the program removes duplicates before continuing. It also filters out songs that contain non-English characters in the title or artist name to provide a more consistent listening experience.

The Spotify Web API is then used to search for each song and determine whether it exists on Spotify. Any songs that are successfully matched are added to a newly created Spotify playlist on the user's account. The playlist is automatically named using the current date and weather condition, resulting in names such as "06-18 Clear Moodify" or "12-25 Snow Moodify".

To improve the user experience, Spotify authentication tokens are stored in a `.spotify_cache` file. This means that users do not need to repeatedly authorize the application every time they run the program, making subsequent executions much more convenient.

The project requires four credentials:

- OpenWeather API key
- Last.fm API key
- Spotify Client ID
- Spotify Client Secret

The main functions of the program include:

- `get_weather()` – retrieves weather information for a city from the OpenWeather API.
- `get_local_time()` – converts the API response into the city's local time.
- `weather_to_mood()` – maps weather conditions and time of day to mood tags.
- `generate_playlist()` – gathers and filters songs from Last.fm.
- `create_spotify_playlist()` – creates and populates a Spotify playlist.

The files that are contained in this project include:

- `project.py` – contains the main functionality of the application, including the `main()` function and all helper functions.
- `test_project.py` – contains unit tests written using pytest that validate several of the project's functions.
- `requirements.txt` – lists all dependencies required to run the project.
- `README.md` – provides the project description, video demonstration link, file structure, and an explanation of how the application works.

This project was chosen because music and weather are both things that influence a person's mood every day. The goal was to build an application that automatically recommends music based on the atmosphere of a location instead of requiring the user to manually create playlists.

Overall, Moodify aims to provide users with a unique and personalized listening experience by combining weather data, music recommendations, and Spotify playlist generation into a single Python application.
