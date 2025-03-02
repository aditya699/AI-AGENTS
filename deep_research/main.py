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



def main():
    pass


if __name__ == "__main__":
    main()
