from langchain_core.tools import tool
import requests, re
from secret_keys import open_weather_key


@tool
def get_current_weather(location) -> dict:
    """
    get current weather information for a given city, country code. The input must be in the format 'City,CountryCode'
    """
    pattern = r'^[^,]+,[A-Za-z]{2}$'
    if not re.match(pattern, location):
        return "error: Invalid input format. Expected 'City,CountryCode', e.g., 'Jerusalem,IL'"

    params = {
        "appid": open_weather_key,
        "units": "metric",
        "lang": "en",
        "q": location,
    }

    res = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params)
    if res.status_code == 200:
        data = res.json()
        return f"temp: {data['main']['temp']}°C, description: {data['weather'][0]['description']}"
    else:
        return "error: Failed to fetch weather data"


if __name__ == "__main__":
    weather = get_current_weather.invoke(
        input={"location": "Tel Aviv,IL"}
    )
    print(f"{weather['temp']}°C, {weather['description']}")
