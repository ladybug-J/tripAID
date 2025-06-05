from langchain.tools import Tool
import openmeteo_requests
import copy
import requests
import datetime
import dateparser
from typing import *

from location import get_coordinates

def parse_date(date_str: str):
    parsed_date = dateparser.parse(date_str)
    if not parsed_date:
        return f"Could not parse the date: '{date_str}'"

    return parsed_date.date()

def get_weather_forecast_or_history(
        location: str,
        target_date: datetime.datetime
):

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
            return f"Temperature Max: {t_max}°C, Min: {t_min}°C - Rain: {rain} mm"

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

        return f"Temperature Max: {t_max}°C, Min: {t_min}°C - Rain: {rain} mm"


def return_weather_dict(cities: Dict[str, int], start_date: datetime.datetime):
    weather_dict = {}
    date = copy.deepcopy(start_date)
    for city, days in cities.items():
        for day in range(int(days)):
            key = city + "_" + date.strftime("%Y-%m-%d") # Combine city and date in key
            weather_dict[key] = get_weather_forecast_or_history(city, date)
            date += datetime.timedelta(days=1)

    return weather_dict

