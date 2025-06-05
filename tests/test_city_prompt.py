import os

from dotenv import load_dotenv
from langchain_together import ChatTogether

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

print(
    llm.invoke(
        city_prompt.invoke(
            {'country': 'Cyprus', 'nr_days': 9}
        )
    ).content
)