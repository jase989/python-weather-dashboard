from weather_api import get_weather, get_forecast
from dashboard import build_dashboard


def main():
    city = input("Enter a city name: ").strip()

    if not city:
        print("No city entered, exiting.")
        return

    print(f"Fetching weather for {city}...")

    try:
        weather = get_weather(city)
        forecast = get_forecast(city)
    except Exception as e:
        # usually a bad city name or an API key that hasn't activated yet
        print(f"Could not get weather data: {e}")
        return

    build_dashboard(weather, forecast)

    print(f"{weather['city']}, {weather['country']} — {weather['temp']:.1f}°C, {weather['description']}")


if __name__ == "__main__":
    main()
