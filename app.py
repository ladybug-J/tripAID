import os
import json
import datetime
import streamlit as st

from dotenv import load_dotenv
from langchain_together import ChatTogether
from langchain_core.runnables import RunnableLambda

from weather import return_weather_dict
from retrieve import get_image
from location import select_country, select_cities, select_llm_cities
from prompts.planner_prompt import planner_prompt

st.set_page_config(
        page_title="tripAID",
        page_icon=":ferris_wheel:",
        layout="wide"
)

load_dotenv()

DEBUG = False

if __name__ == "__main__":

    from prompts.city_prompt import city_prompt

    st.title("tripAID")
    st.write("")

    colkey, colempty = st.columns([1,2])

    if "api_key" not in st.session_state:
        st.session_state.api_key = os.getenv("TOGETHER_API_KEY")
        if st.session_state.api_key is None:
            st.session_state.valid_key = False
        else:
            st.session_state.valid_key = True

    if not st.session_state.valid_key:
        with colkey:
            st.session_state.api_key = st.text_input(
                "Input your Together AI API key",
                type="password",
                help="If you do not own a TogetherAI API key, follow the instructions"
                     " in https://docs.together.ai/reference/authentication-1"
            )
            try:
                llm = ChatTogether(
                    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                    temperature=0.7,
                    max_tokens=512,
                    max_retries=2,
                    api_key=st.session_state.api_key
                )
                llm.invoke("Hello")
                st.session_state.valid_key = True
            except:
                st.error("Invalid API key. Please try again.")

    llm = ChatTogether(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        temperature=0.7,
        max_tokens=None,
        max_retries=2,
        api_key=st.session_state.api_key
    )

    if st.session_state.valid_key:
        col1, col2 = st.columns([3,1])

        with col1:
            select_country()
            #if st.session_state.country:
            #    select_cities()

            start_date = st.date_input(
                "Start date:",
                value=datetime.datetime.now()
            )
            end_date = st.date_input(
                    "End date:",
                    value=datetime.datetime.now()+datetime.timedelta(days=2)
                )
            nr_days = (end_date-start_date).days

            if st.session_state.country:
                def run_weather_chain(chain_out):
                    return return_weather_dict(chain_out, start_date)

                chain = (
                        city_prompt
                        | llm
                        | RunnableLambda(lambda x: json.loads(x.content)['cities'])
                        | RunnableLambda(run_weather_chain)
                )

                weather_forecast = chain.invoke({
                    'country': st.session_state.country,
                    'nr_days': nr_days
                })

            #with col2:
            #    if location:
            #        image = get_image(location)
            #        st.image(image)

                if st.button("Run planner"):
                    response = llm.invoke(
                        planner_prompt.invoke(dict(
                            country=st.session_state.country,
                            nr_days=nr_days,
                            weather_forecast=weather_forecast
                        ))
                    )
                    st.markdown(response.content)