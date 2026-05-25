# Weather Dashboard

Python script that fetches weather data from OpenWeatherMap and generates an HTML page with current conditions and a 5-day forecast.

Built this as a personal project to practice working with APIs and get more comfortable with Python.

**Live demo:** [jase989.github.io/python-weather-dashboard](https://jase989.github.io/python-weather-dashboard/) — static snapshot showing Dubai.

## Running it

You'll need a free API key from [openweathermap.org](https://openweathermap.org/api). New keys take a couple of hours to activate.

Create a `.env` file in the project folder:

```
OPENWEATHER_API_KEY=your_key_here
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run it:

```bash
python main.py
```

It'll ask for a city name, then write a `dashboard.html` file you can open in your browser.

## Files

- `main.py` — entry point
- `weather_api.py` — handles the API calls
- `dashboard.py` — generates the HTML
- `.env` — your API key (don't commit this)
