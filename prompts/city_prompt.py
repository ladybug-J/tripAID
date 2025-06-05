from langchain_core.prompts import ChatPromptTemplate

city_prompt = ChatPromptTemplate.from_template(
    """
    Think of the cities you would propose to visit in {country} for {nr_days} days. Decide where are the main 
    attractions, consider the distances between cities to choose a reasonable amount of cities to visit the given amount
    of days. Return ONLY the names of the cities (as keys) and the number of day to spend in each (as values) in JSON 
    format. Respond only with the JSON object, without markdown or formatting like ```json...```
    
    Example: 
    Input: 'country': 'Germany', 'nr_days': 5
    Output:  'cities': 
                    - 'Berlin': 2,
                    - 'Dresden':1,
                    - 'Munich': 2
    """
)