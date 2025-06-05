from langchain_core.prompts import ChatPromptTemplate

# Inputs: country, nr_days, weather_forecast

planner_prompt = ChatPromptTemplate.from_template(
    """
    You are a travel assistant helping a user plan a holiday in {country}.
    The user wants to know an itinerary for a {nr_days} day vacation, where several cities are visited.
    The weather forecast or the historic data for those cities and dates is: {weather_forecast}.

    Based on the forecast and general plans to do depending on the weather, respond with:
    - Weather summary.
    - 3 things to do per day.
    - Commute times and options between cities, if changing cities from day to day.
    - At the end of the entire plan, what to pack for the trip.

    Answer:
    """
)