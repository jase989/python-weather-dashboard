from datetime import datetime
from html import escape as _e

OUTPUT_FILE = "dashboard.html"

# Map OpenWeatherMap icon codes to Meteocons (basmilius/weather-icons) names
ICON_MAP = {
    "01d": "clear-day",                 "01n": "clear-night",
    "02d": "partly-cloudy-day",         "02n": "partly-cloudy-night",
    "03d": "cloudy",                    "03n": "cloudy",
    "04d": "overcast-day",              "04n": "overcast-night",
    "09d": "rain",                      "09n": "rain",
    "10d": "partly-cloudy-day-rain",    "10n": "partly-cloudy-night-rain",
    "11d": "thunderstorms-rain",        "11n": "thunderstorms-rain",
    "13d": "snow",                      "13n": "snow",
    "50d": "mist",                      "50n": "mist",
}
ICON_CDN = "https://cdn.jsdelivr.net/gh/basmilius/weather-icons@v2.0.0/production/fill/all"


def _icon_url(owm_code):
    name = ICON_MAP.get(owm_code, "clear-day")
    return f"{ICON_CDN}/{name}.svg"


def _forecast_rows(forecast):
    # builds the 5 day columns — one div per day, nothing fancy
    rows = ""
    for day in forecast:
        label = datetime.strptime(day["date"], "%Y-%m-%d").strftime("%a %-d %b")
        desc = _e(day["description"])
        rows += f"""
            <div class="forecast-day">
                <div class="fc-label">{label}</div>
                <img src="{_icon_url(day['icon'])}" alt="{desc}" width="56" height="56">
                <div class="fc-desc">{desc}</div>
                <div class="fc-temps">
                    <span class="fc-high">{day['max_temp']:.0f}°</span>
                    <span class="fc-low">{day['min_temp']:.0f}°</span>
                </div>
            </div>"""
    return rows


def build_dashboard(weather, forecast):
    icon_url = _icon_url(weather["icon"])
    city = _e(weather["city"])
    country = _e(weather["country"])
    description = _e(weather["description"])

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather — {city}</title>
    <style>
        body {{
            font-family: sans-serif;
            max-width: 640px;
            margin: 60px auto;
            padding: 0 20px;
            background: #f0f4f8;
            color: #333;
        }}
        .card {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 16px;
        }}
        h1 {{ margin: 0 0 4px; font-size: 2rem; }}
        .subtitle {{ color: #666; margin-bottom: 20px; }}
        .temp {{ font-size: 3.5rem; font-weight: bold; margin: 10px 0; }}
        .details {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-top: 24px;
        }}
        .detail {{
            background: #f0f4f8;
            padding: 12px 16px;
            border-radius: 8px;
        }}
        .detail label {{
            font-size: 0.75rem;
            color: #888;
            display: block;
            margin-bottom: 4px;
        }}
        .detail span {{ font-size: 1.1rem; font-weight: 500; }}

        /* forecast strip at the bottom */
        .forecast-card {{
            background: white;
            border-radius: 12px;
            padding: 20px 24px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }}
        .forecast-card h2 {{
            margin: 0 0 16px;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #888;
        }}
        .forecast-grid {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 8px;
            text-align: center;
        }}
        .forecast-day {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
        }}
        .fc-label {{
            font-size: 0.78rem;
            font-weight: 600;
            color: #555;
        }}
        .fc-desc {{
            font-size: 0.68rem;
            color: #888;
            line-height: 1.2;
        }}
        .fc-temps {{
            display: flex;
            gap: 6px;
            font-size: 0.9rem;
        }}
        .fc-high {{ font-weight: 600; }}
        .fc-low {{ color: #999; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>{city}, {country}</h1>
        <p class="subtitle">{description}</p>
        <img class="main-icon" src="{icon_url}" alt="{description}" width="120" height="120">
        <div class="temp">{weather['temp']:.1f}°C</div>
        <div class="details">
            <div class="detail">
                <label>Feels like</label>
                <span>{weather['feels_like']:.1f}°C</span>
            </div>
            <div class="detail">
                <label>Humidity</label>
                <span>{weather['humidity']}%</span>
            </div>
            <div class="detail">
                <label>Wind speed</label>
                <span>{weather['wind_speed']} m/s</span>
            </div>
        </div>
    </div>

    <div class="forecast-card">
        <h2>5-day outlook</h2>
        <div class="forecast-grid">{_forecast_rows(forecast)}
        </div>
    </div>
</body>
</html>"""

    with open(OUTPUT_FILE, "w") as f:
        f.write(doc)

    print(f"Dashboard saved to {OUTPUT_FILE}")
