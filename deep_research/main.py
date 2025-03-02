'''
Author : Aditya Bhatt 24-02-2025 

NOTE:
1.We are to create a deep research clone

Improvements needed to match openai's deep research:
1.Add a better scrapper
2.Add a better LLM at report generation(possibly a fine tuned LLM which specializes in report generation(like a report writer))
3.This works great at a summary level.But it can't go indepth.

(OpenAI have fine tuned model(o3 for deep research(on browser tasks and deep research report creation)),that is only moat they have (internet is for all you don't monopolize it))

Note-Nothing taking away from OPENAI . There deep research is exceptional.But i say we can also reach near that level.

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
