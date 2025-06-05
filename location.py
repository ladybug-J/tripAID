import requests
import pycountry
import streamlit as st

def get_coordinates(location: str):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1"
    geo_res = requests.get(geo_url).json()
    if "results" not in geo_res:
        return None, None
    loc = geo_res["results"][0]
    return loc["latitude"], loc["longitude"]

def select_country():
    country_list = sorted([country.name for country in pycountry.countries])
    st.session_state.country = st.multiselect(
        "Type to search a country:",
        country_list,
        max_selections=1
    )

def select_cities():
    url = "https://countriesnow.space/api/v0.1/countries/cities"
    payload = {"country": st.session_state.country}
    response = requests.post(url, json=payload)
    st.session_state.cities = st.multiselect(
        "Select citites",
        response.json()["data"]
    )

def select_llm_cities(llm):
    pass