import os
from collections import defaultdict
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


def get_weather(city):
    # metric units — because nobody wants to do Fahrenheit maths at 45°C
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()  # blows up if the city doesn't exist or the key's wrong

    data = response.json()

    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temp": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],  # usually worse than the actual temp
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"].capitalize(),
        "wind_speed": data["wind"]["speed"],
        "icon": data["weather"][0]["icon"]
    }


def get_forecast(city):
    # returns 3-hour slots for the next 5 days — 40 entries total, we group them by day
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(FORECAST_URL, params=params)
    response.raise_for_status()

    slots = response.json()["list"]

    by_day = defaultdict(list)
    for slot in slots:
        date = slot["dt_txt"].split(" ")[0]  # "2026-05-25 12:00:00" → "2026-05-25"
        by_day[date].append(slot)

    days = []
    for date in sorted(by_day.keys())[:5]:
        entries = by_day[date]

        # midday slot gives the most representative icon — fallback to first if it's missing
        midday = next((e for e in entries if "12:00:00" in e["dt_txt"]), entries[0])

        days.append({
            "date": date,
            "min_temp": min(e["main"]["temp_min"] for e in entries),
            "max_temp": max(e["main"]["temp_max"] for e in entries),
            "description": midday["weather"][0]["description"].capitalize(),
            "icon": midday["weather"][0]["icon"],
        })

    return days
