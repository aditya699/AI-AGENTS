from serpapi import GoogleSearch
import os

from dotenv import load_dotenv
load_dotenv()

def get_search_links(query, num_results=5):
    """
    Perform a Google search and return the top links from organic results.
    
    Args:
        query (str): The search query
        num_results (int): Number of links to return (default: 5)
        
    Returns:
        list: A list of the top links from organic results
    """
    params = {
        "engine": "google",
        "q": query,
        "api_key": os.getenv("SERP_API_KEY")
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results.get("organic_results", [])
    
    # Extract just the links from the results
    links = []
    for result in organic_results[:num_results]:
        if "link" in result:
            links.append(result["link"])
    
    return links

# Example usage
if __name__ == "__main__":
    query = "latest trends in AI"
    links = get_search_links(query)
    print(links)


