import datetime

from weather import return_weather_dict

# Output from LLM dict
cities = {
    'Berlin': 2,
    'Dresden': 1,
    'Munich': 1
}
# Date
start_date = datetime.date.today()

print(return_weather_dict(cities, start_date))