from duckduckgo_search import DDGS

def get_image(query: str):
    results = DDGS().images(
        keywords=query,
        max_results=1
    )
    if results:
        return results[0]['image']
    return None