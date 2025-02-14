'''
Author : Aditya Bhatt
Date : 12-02-2025

PydanticAI is a Python agent framework designed to make it less painful to build production-grade applications with Generative AI.

FastAPI revolutionized web development by offering an innovative and ergonomic design, built on the foundation of Pydantic.

Similarly, virtually every agent framework and LLM library in Python uses Pydantic, yet when we began to use LLMs in Pydantic Logfire, we couldn't find anything that gave us the same feeling.

We built PydanticAI with one simple aim: to bring that FastAPI feeling to GenAI app development.
'''

from pydantic_ai import Agent
import os
from dotenv import load_dotenv
import logfire

# Load environment variables
load_dotenv()
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

# Configure Logfire for logging
logfire.configure()
logfire.instrument_httpx(capture_all=True)  
os.environ["LOGFIRE_TOKEN"]=os.getenv("LOGFIRE_TOKEN")
# Define the first agent
agent_1 = Agent(  
    'google-gla:gemini-1.5-flash',
    system_prompt='Be funny, reply with one sentence.',  
)

result_1 = agent_1.run_sync('What is Pythagoras theorem?')  
print(result_1.data)

# Logfire logging for better visualization
logfire.log("Pythagoras theorem response", result_1.data)

# Define the second agent
agent_2 = Agent(
    'google-gla:gemini-1.5-flash',
    system_prompt='Be funny, reply with one sentence.',  
)
result_2 = agent_2.run_sync('What is the capital of France?')
print(result_2.data)

# Logfire logging
logfire.log("Capital of France response", result_2.data)
