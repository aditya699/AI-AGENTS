'''
Author : Aditya Bhatt
Date : 12-02-2025
Structured Response
'''

from pydantic import BaseModel
from pydantic_ai import Agent
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GEMINI_API_KEY"]=os.getenv("GEMINI_API_KEY")

class Response(BaseModel):
    rating:int


agent = Agent(
    'google-gla:gemini-1.5-flash',
    system_prompt='Given a product review, rate it from 1 to 10.',
    result_type=Response
)

result = agent.run_sync('The product is super slow and boring.')
print(result.data)


result = agent.run_sync('The product is super cool and amazing.')
print(result.data)





