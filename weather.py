from langchain.tools import Tool
import openmeteo_requests
import requests
import datetime
import dateparser

def get_coordinates(location: str):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1"
    geo_res = requests.get(geo_url).json()
    if "results" not in geo_res:
        return None, None
    loc = geo_res["results"][0]
    return loc["latitude"], loc["longitude"]

def parse_date(date_str: str):
    parsed_date = dateparser.parse(date_str)
    if not parsed_date:
        return f"Could not parse the date: '{date_str}'"

    return parsed_date.date()

def get_weather_forecast_or_history(location: str, target_date: datetime.datetime):

    lat, lon = get_coordinates(location)

    if lat is None:
        return f"Could not find coordinates for '{location}'."

    today = datetime.date.today()

    if target_date >= today:
        # Use forecast API
        forecast_url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
            f"&timezone=auto"
        )
        res = requests.get(forecast_url).json()
        if "daily" not in res:
            return "Forecast data not available."

        try:
            idx = res["daily"]["time"].index(str(target_date))
            t_max = res["daily"]["temperature_2m_max"][idx]
            t_min = res["daily"]["temperature_2m_min"][idx]
            rain = res["daily"]["precipitation_sum"][idx]
            return {
                target_date:
                f"Temperature Max: {t_max}°C, Min: {t_min}°C\n"
                f"Rain: {rain} mm"
            }
        except ValueError:
            print(f"⚠️ Forecast for {target_date} not available yet. Calling historic data...")

        historic_target_date = target_date.replace(year=target_date.year-1)

        # Use historical API
        history_url = (
            f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}"
            f"&start_date={historic_target_date}&end_date={historic_target_date}"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
            f"&timezone=auto"
        )
        res = requests.get(history_url).json()
        if "daily" not in res or len(res["daily"]["time"]) == 0:
            print(f"No historical data found for {historic_target_date}.")

        t_max = res["daily"]["temperature_2m_max"][0]
        t_min = res["daily"]["temperature_2m_min"][0]
        rain = res["daily"]["precipitation_sum"][0]

        return {
            target_date:
            f"Temperature Max: {t_max}°C, Min: {t_min}°C\n"
            f"Rain: {rain} mm"
        }
