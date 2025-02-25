from langchain_community.document_loaders import UnstructuredURLLoader

def extract_content_from_urls(urls):
    """
    Extract content from a list of URLs and return it in a dictionary format
    where keys are URLs and values are the extracted text content.
    
    Args:
        urls (list): List of URLs to extract content from
        
    Returns:
        dict: Dictionary with URLs as keys and extracted content as values
    """
    try:
        # Initialize the URL loader
        loader = UnstructuredURLLoader(urls=urls)
        
        # Load the data from URLs
        data = loader.load()
        
        # Create a dictionary to store URL and content pairs
        url_content_dict = {}
        
        # Process each document and map it to its URL
        for i, document in enumerate(data):
            if i < len(urls):  # Ensure we don't go out of bounds
                url_content_dict[urls[i]] = document.page_content
        
        return url_content_dict
    except Exception as e:
        print(f"Error extracting content from URLs: {e}")
        return {}

# Example usage
if __name__ == "__main__":
    sample_urls = [
        'https://en.wikipedia.org/wiki/Indian_cuisine',
        'https://journalofethnicfoods.biomedcentral.com/articles/10.1186/s42779-022-00129-4',
        'https://www.britannica.com/topic/Indian-cuisine',
        'https://www.culinaryschools.org/international/indian-cuisine.php',
        'https://www.littleindiami.com/exploring-5000-years-of-indian-culinary-history-a-rich-and-diverse-legacy/'
    ]
    
    url_content_map = extract_content_from_urls(sample_urls)
    
    # Print the results in a structured way
    for url, content in url_content_map.items():
        print(f"\nURL: {url}")
        print(f"Content length: {len(content)} characters")
        print(f"Content preview: {content[:150]}...\n")
        print("-" * 80)
