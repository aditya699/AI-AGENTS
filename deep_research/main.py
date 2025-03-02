'''
Author : Aditya Bhatt 24-02-2025 

NOTE:
1.We are to create a deep research clone

To enhance our deep research capabilities and align more closely with OpenAI's offerings, the following improvements are recommended:
1. Implement a more advanced web scraper to gather data effectively.
2. Integrate a specialized LLM for report generation, potentially a fine-tuned model designed specifically for crafting detailed reports.
3. While the current system excels at summarization, it lacks the depth required for comprehensive analysis.

OpenAI's fine-tuned model (o3) for deep research tasks, particularly in browser-based research and report creation, represents a significant competitive advantage. However, it is essential to recognize that the internet is an open resource, and we can also strive to achieve a similar level of excellence.

This is not to undermine OpenAI's achievements; their deep research capabilities are indeed remarkable. Nonetheless, we believe that with the right enhancements, we can approach that standard.

TODO:
1.New approach to research.
(query->user_query->research_topics->scrape_urls->scrape_content->(each section will go in a llm call)get two things headers and content)

(Once we have the headers and content we can store them as a variable)

(In the last generate a report using the headers and content)

'''

from http import client
from client.azure import Client
from openai import AzureOpenAI
from schemas.user_query import UserQuery, ResearchQuery
from client.serp import get_search_links
from utils.link_scrapper import extract_content_from_urls
import json
import os
from datetime import datetime
from utils.token_tracker import initialize_trackers, update_and_display_metrics
from utils.user_query import get_search_query
from utils.research_query import get_research_queries
from utils.summary import summarize_content
from utils.json_saver import save_summaries_to_json

input_token_tracker, output_token_tracker = initialize_trackers()

def main():
    global input_token_tracker
    global output_token_tracker
    
    input_query = input("Enter the topic on which you want to do research: ")
    print("User Wants to research on: ", input_query)

    print("Getting Search Query based on user query...")
    get_client=Client()
    client=get_client.get_azure_client()

    print("Azure Client Created Successfully,Azure OpenAI will be used for this code")

    search_query, input_token_tracker, output_token_tracker = get_search_query(client, input_query, input_token_tracker, output_token_tracker)

    print("Search Query Generated Successfully")

    print("Search Query: ", search_query.query)
    current_cost_inr = update_and_display_metrics(input_token_tracker, output_token_tracker, "mini")

    print("Input Token Usage: ", input_token_tracker)
    print("Output Token Usage: ", output_token_tracker)
    print(f"Current Cost in ₹: {current_cost_inr:.5f}")


    print("The process of generating research queries is starting...")

    # Based on the search query,break it into subtopics and generate research queries
    research_queries, input_token_tracker, output_token_tracker = get_research_queries(client, search_query.query, input_token_tracker, output_token_tracker)

    print("Research Queries Generated Successfully")

    print("Research Queries: ", research_queries.queries)

    current_cost_inr = update_and_display_metrics(input_token_tracker, output_token_tracker, "mini")

    print("Input Token Usage: ", input_token_tracker)
    print("Output Token Usage: ", output_token_tracker)
    print(f"Current Cost in ₹: {current_cost_inr:.5f}")
    research_queries_list=research_queries.queries[0:2]
    print("For this run we are taking only 2 research queries to save cost and response time")
    print("Research Queries: ", research_queries_list)
    master_data=[]
    for query in research_queries_list:

        query_content=''
        print("Research Query: ", query)

        print("Processing the research query...")

         #Get the search links based on the research query
        search_links = get_search_links(query)

        print("Search Links Generated Successfully")

        print("Search Links: ", search_links)

        #Get the content from the search links
        raw_data_dict = extract_content_from_urls(search_links)

        print("Links Scraped Successfully and raw data is stored in a dictionary")

        #Pass the raw data to the LLM to get the headers and content,in this dict we have url as key and content as value

        for url,content in raw_data_dict.items():
            print("URL: ", url)
            content_exactarcted ,input_token_tracker, output_token_tracker = summarize_content(client,url,content,input_token_tracker, output_token_tracker)

            print("Content Extracted : ", content_exactarcted[0:100])

            query_content+=content_exactarcted

            current_cost_inr = update_and_display_metrics(input_token_tracker, output_token_tracker, "mini")
            print("Input Token Usage: ", input_token_tracker)
            print("Output Token Usage: ", output_token_tracker)
            print(f"Current Cost in ₹: {current_cost_inr:.5f}")


        master_data.append({
            "header": query,
            "content": query_content,
            "url": search_links
        })

    print("Master Data Generated Successfully")
    with open("master_data.json", "w") as f:
        json.dump(master_data, f)
       
    return master_data

if __name__ == "__main__":
    main()
