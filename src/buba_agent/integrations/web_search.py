# integrations/web_search.py

import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

class WebSearch:

    def __init__(self):

        self.client = TavilyClient(
            api_key=os.getenv("TAVILY_API_KEY")
        )

    def search(self, query: str, max_results: int = 5):

        result = self.client.search(
            query=query,
            max_results=max_results
        )
        return result