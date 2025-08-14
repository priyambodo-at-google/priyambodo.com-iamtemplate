import os
import requests

# Load environment variables from .env file
# This is handled by the main app, but good practice for standalone testing
# from dotenv import load_dotenv; load_dotenv()

SERPAPI_API_KEY = os.environ.get("SERPAPI_API_KEY")

def third_party_web_search(query: str):
    """Performs a web search using SerpApi for the given query."""
    if not SERPAPI_API_KEY:
        return "Error: SERPAPI_API_KEY not set. Cannot perform web search."

    url = "https://serpapi.com/search"
    params = {
        "api_key": SERPAPI_API_KEY,
        "q": query,
        "engine": "google", # You can change this to other engines like "bing", "duckduckgo"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Raise an exception for HTTP errors
        search_results = response.json()

        # Extract relevant information (e.g., organic results titles and snippets)
        if "organic_results" in search_results:
            formatted_results = []
            for result in search_results["organic_results"]:
                title = result.get("title", "N/A")
                snippet = result.get("snippet", "N/A")
                link = result.get("link", "N/A")
                formatted_results.append(f"Title: {title}\nSnippet: {snippet}\nLink: {link}\n")
            return "\n".join(formatted_results)
        else:
            return "No organic search results found."

    except requests.exceptions.RequestException as e:
        return f"Error performing web search: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"