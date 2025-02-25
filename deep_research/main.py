'''
Author : Aditya Bhatt 24-02-2025 

NOTE:
1.We are to create a deep research clone

BUG:

TODO:

'''

from client.azure import Client
from openai import AzureOpenAI
from schemas.user_query import UserQuery, ResearchQuery
import matplotlib.pyplot as plt
from client.serp import get_search_links
from link_scrapper import extract_content_from_urls
import json
import os
from datetime import datetime


def initialize_trackers():
    """Initialize token and cost trackers"""
    input_token_tracker = 0
    output_token_tracker = 0
    print("Current token count: (for the run of this script)", input_token_tracker + output_token_tracker)
    print("Current script running cost", 0, "dollars")
    return input_token_tracker, output_token_tracker


def update_and_display_metrics(input_token_tracker, output_token_tracker):
    """Update and display token usage metrics and cost"""
    total_tokens = input_token_tracker + output_token_tracker
    input_cost_per_million_tokens = 0.15
    output_cost_per_million_tokens = 0.60

    # Calculate costs separately for input and output tokens
    input_cost = (input_token_tracker / 1_000_000) * input_cost_per_million_tokens
    output_cost = (output_token_tracker / 1_000_000) * output_cost_per_million_tokens
    current_cost = input_cost + output_cost
    
    print("Current token count: (for the run of this script)", total_tokens)
    print("Current script running cost: ${:.5f} dollars".format(current_cost))

    # Create a plot for token usage and cost
    plt.figure(figsize=(10, 5))
    plt.bar(['Input Tokens', 'Output Tokens', 'Current Cost'], 
            [input_token_tracker, output_token_tracker, current_cost], 
            color=['blue', 'orange', 'green'])
    plt.title('Token Usage and Cost')
    plt.ylabel('Value')
    plt.xlabel('Type')
    plt.axhline(y=total_tokens, color='r', linestyle='--', label='Total Tokens')
    plt.legend()
    plt.grid(axis='y')
    plt.show()
    
    return total_tokens, current_cost


def get_search_query(client, user_query, input_token_tracker, output_token_tracker):
    """Transform user query into search query using LLM"""
    USER_QUERY_PROMPT = f"""
    Given the user query transform it into a search query for a search engine.Only return the search query, no other text.Do not add any other text apart from the user query.

    Example:
    User Query: "What is the weather in Tokyo?"
    Search Query: "weather in Tokyo"

    User Query: "Need help about the latest trends in AI"
    Search Query: "latest trends in AI"

    User Query: {user_query}

    """
    print("Here is the prompt for the llm to transform the user query into a search query: ", USER_QUERY_PROMPT)

    try:
        completion = client.beta.chat.completions.parse(
            model="mini-deployment",  # replace with the model deployment name of your gpt-4o 2024-08-06 deployment
            messages=[
                {"role": "system", "content": "You are a helpful assistant that transforms user queries into search queries for a search engine."},
                {"role": "user", "content": USER_QUERY_PROMPT},
            ],
            response_format=UserQuery,
        )
        
        # Update token trackers
        input_token_tracker += completion.usage.prompt_tokens
        output_token_tracker += completion.usage.completion_tokens
        print("LLM response has been generated successfully")

        search_query = completion.choices[0].message.parsed
        print("Here is the search query: ", search_query.query)
        
        return search_query, input_token_tracker, output_token_tracker
    
    except Exception as e:
        print("Error in generating the LLM response: ", e)
        return None, input_token_tracker, output_token_tracker


def get_research_queries(client, search_query, input_token_tracker, output_token_tracker):
    """Generate research queries from the search query"""
    print("Generating the research queries for the search query process has started")
    
    RESEARCH_PROMPT = f"""
        Please analyze the following search query and decompose it into a list of specific research queries that are suitable for detailed reporting and analysis.

        Example:
        Search Query: "latest trends in AI"
        Research Queries: ["History of AI","Current Trends in AI","Future Trends in AI","Opportunities in AI","Challenges in AI","Can AI Replace Humans?"]

        Search Query: {search_query}

    """

    print("Here is the prompt for the llm to transform the user query into a research queries: ", RESEARCH_PROMPT)

    try:
        completion = client.beta.chat.completions.parse(
            model="mini-deployment",  # replace with the model deployment name of your gpt-4o 2024-08-06 deployment
            messages=[
                {"role": "system", "content": "You are a helpful assistant that transforms user queries into research queries for a research report."},
                {"role": "user", "content": RESEARCH_PROMPT},
            ],
            response_format=ResearchQuery,
        )

        # Update token trackers
        input_token_tracker += completion.usage.prompt_tokens
        output_token_tracker += completion.usage.completion_tokens
        print("LLM response has been generated successfully")

        research_queries = completion.choices[0].message.parsed
        print("Here is the research queries: ", research_queries.queries)
        
        return research_queries, input_token_tracker, output_token_tracker
    
    except Exception as e:
        print("Error in generating the LLM response for research queries:", e)
        return None, input_token_tracker, output_token_tracker


def summarize_content(client, url, content, input_token_tracker, output_token_tracker):
    """Summarize the content from a URL using LLM"""
    try:
        SUMMARY_PROMPT = f"""
        Please summarize the following content from the URL: {url}
        
        CONTENT:
        {content}  
        
        Provide a concise summary that captures the key information.
        """
        
        completion = client.chat.completions.create(
            model="mini-deployment",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that Extracts the key information from the web content accurately.Only Extract Meaningful Information from the content.Do not add any other text apart from the summary"},
                {"role": "user", "content": SUMMARY_PROMPT},
            ]
        )
        
        # Update token trackers
        input_token_tracker += completion.usage.prompt_tokens
        output_token_tracker += completion.usage.completion_tokens
        
        summary = completion.choices[0].message.content
        return summary, input_token_tracker, output_token_tracker
    
    except Exception as e:
        print(f"Error summarizing content from {url}: {e}")
        return f"Failed to summarize content from {url}", input_token_tracker, output_token_tracker


def save_summaries_to_json(summaries, user_query):
    """Save URL summaries to a JSON file"""
    # Create a directory for research results if it doesn't exist
    os.makedirs("research_results", exist_ok=True)
    
    # Create a timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create a safe filename from the user query
    safe_query = "".join(c if c.isalnum() else "_" for c in user_query)[:50]
    
    # Create the filename
    filename = f"research_results/{safe_query}_{timestamp}.json"
    
    # Save the summaries to the JSON file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(summaries, f, indent=4, ensure_ascii=False)
    
    print(f"Summaries saved to {filename}")
    return filename


def main():
    """Main function to run the deep research process"""
    # Initialize token trackers
    input_token_tracker, output_token_tracker = initialize_trackers()
    
    # Get user query
    user_query = input("Enter the topic on which you want to do research on: ")
    print(f"User Query: {user_query}")
    
    # Initialize the Azure OpenAI client
    azure_client = Client()
    client = azure_client.get_azure_client()
    
    # Get search query
    search_query, input_token_tracker, output_token_tracker = get_search_query(
        client, user_query, input_token_tracker, output_token_tracker
    )
    
    if search_query:
        # Update and display metrics
        update_and_display_metrics(input_token_tracker, output_token_tracker)
        
        # Get research queries
        research_queries, input_token_tracker, output_token_tracker = get_research_queries(
            client, search_query, input_token_tracker, output_token_tracker
        )
        
        if research_queries:
            # Final update and display metrics
            update_and_display_metrics(input_token_tracker, output_token_tracker)

    # Create a single dictionary to store all summaries
    all_summaries = {}
    
    #Iterate over the research queries and get the links
    for research_query in research_queries.queries:
        print("Here is the research query: ", research_query)
        try:
            # Get links for the research query
            links = get_search_links(research_query)
            print("Here are the links for the research query: ", links)
            
            # Extract content from the links
            print("Extracting the content from the links")
            url_content_dict = extract_content_from_urls(links)
            
            # Process each URL and its content
            for url, content in url_content_dict.items():
                print(f"Summarizing content from: {url}")
                if content:
                    summary, input_token_tracker, output_token_tracker = summarize_content(
                        client, url, content, input_token_tracker, output_token_tracker
                    )
                    all_summaries[url] = summary
                    print(f"Summary for {url}: {summary[:150]}...")
                else:
                    print(f"No content extracted from {url}")
            
            # Update metrics after processing each research query
            update_and_display_metrics(input_token_tracker, output_token_tracker)
            
        except Exception as e:
            print(f"Error processing research query '{research_query}': {e}")
            continue
    
    # Save all summaries to a single JSON file
    if all_summaries:
        json_file = save_summaries_to_json(all_summaries, user_query)
        print(f"All summaries saved to {json_file}")


if __name__ == "__main__":
    main()
