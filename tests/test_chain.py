import copy
import datetime
import os
import json
from dotenv import load_dotenv
from typing import *
from langchain_core.runnables import RunnableLambda
from langchain_together import ChatTogether

from weather import return_weather_dict
from prompts.city_prompt import city_prompt


load_dotenv()
api_key = os.getenv("TOGETHER_API_KEY")

llm = ChatTogether(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    temperature=0.7,
    max_tokens=512,
    max_retries=2,
    api_key=api_key
)

city_input = {'country': 'Spain', 'nr_days': 7}
start_date = datetime.date.today()

def run_weather_chain(chain_out):
    return return_weather_dict(chain_out, start_date)

chain = (
        city_prompt
        | llm
        | RunnableLambda(lambda x: json.loads(x.content)['cities'])
        | RunnableLambda(run_weather_chain)
)

response = chain.invoke(city_input)
