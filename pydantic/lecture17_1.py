'''
Author : Aditya Bhatt
Date : 12-02-2025

PydanticAI is a Python agent framework designed to make it less painful to build production grade applications with Generative AI.

PydanticAI is a Python Agent Framework designed to make it less painful to build production grade applications with Generative AI.

FastAPI revolutionized web development by offering an innovative and ergonomic design, built on the foundation of Pydantic.

Similarly, virtually every agent framework and LLM library in Python uses Pydantic, yet when we began to use LLMs in Pydantic Logfire, we couldn't find anything that gave us the same feeling.

We built PydanticAI with one simple aim: to bring that FastAPI feeling to GenAI app development.
'''
# Agents are PydanticAI's primary interface for interacting with LLMs.

# In some use cases a single Agent will control an entire application or component, but multiple agents can also interact to embody more complex workflows.

'''
Hello World 
'''
from pydantic_ai import Agent
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GEMINI_API_KEY"]=os.getenv("GEMINI_API_KEY")

agent = Agent(  
    'google-gla:gemini-1.5-flash',
    system_prompt='Be funny, reply with one sentence.',  
)

result = agent.run_sync('What is pythagoras theorem?')  
print(result.data)

print(dir(result))



