import os
import datetime
import streamlit as st

from dotenv import load_dotenv
from langchain_together import ChatTogether

from weather import get_weather_forecast_or_history
from retrieve import get_image

st.set_page_config(
        page_title="TripAid",
        page_icon=":ferris_wheel:",
        layout="wide"
)

load_dotenv()
try:
    api_key = os.getenv("TOGETHER_API_KEY")
except:
    st.text_input(
        "Input your together API key"
    )

DEBUG = False

if __name__ == "__main__":

    st.title("TripAid")
    st.write("")

    col1, col2 = st.columns([3,1])

    with col1:
        location = st.text_input(
            "Where do you want to travel?",
            value=None
        )
        start_date = st.date_input(
            "Start date:",
            value=datetime.date(2025, 6, 2)
        )
        end_date = st.date_input(
                "End date:",
                value=datetime.date(2025, 6, 4)
            )

        nr_days = (end_date-start_date).days
        weather_forecast = dict()
        for i in range(nr_days+1):
            weather_forecast.update(
                get_weather_forecast_or_history(
                    location,
                    start_date + datetime.timedelta(days=i)
                )
            )
    with col2:
        if location:
            image = get_image(location)
            st.image(image)

    llm = ChatTogether(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        temperature=0.7,
        max_tokens=512,
        max_retries=2,
        api_key=api_key
    )

    prompt = f"""
        You are a travel assistant helping a user plan a holiday in {location}.
        The user wants to know an itinerary for a {nr_days} vacation.
        The weather forecast or the historic data for those dates is: {weather_forecast}.
    
        Based on the forecast and general plans to do depending on the weather, respond with:
        1. 3 things to do per day.
        2. A short explanation why.
        3. Packing tips per day.
    
        Answer:
    """

    messages = [
        (
            "system",
            prompt
         )
    ]

    if st.button("Run planner"):
        response = llm.invoke(messages)
        st.markdown(response.content)