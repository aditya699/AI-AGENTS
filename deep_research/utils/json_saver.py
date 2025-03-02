from datetime import datetime
import os
import json



def save_summaries_to_json(summaries, user_query):
    """Save URL summaries to a JSON file"""
    print("\n=== Starting JSON Save Process ===")
    # Create a directory for research results if it doesn't exist
    print("Creating research_results directory if it doesn't exist...")
    os.makedirs("research_results", exist_ok=True)
    
    # Create a timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"Generated timestamp: {timestamp}")
    
    # Create a safe filename from the user query
    safe_query = "".join(c if c.isalnum() else "_" for c in user_query)[:50]
    print(f"Sanitized query for filename: {safe_query}")
    
    # Create the filename
    filename = f"research_results/{safe_query}_{timestamp}.json"
    print(f"Final filename: {filename}")
    
    # Save the summaries to the JSON file
    print("Writing summaries to JSON file...")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(summaries, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Summaries successfully saved to {filename}")
    print(f"File size: {os.path.getsize(filename)} bytes")
    print("=== JSON Save Process Complete ===\n")
    return filename