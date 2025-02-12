# Lectore 17-Introduction to Pydantic AI

'''
Hello World in pydantic AI

1.Basic Agent Usage
2.Basic Message History
'''
from pydantic_ai import Agent
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GEMINI_API_KEY"]=os.getenv("GEMINI_API_KEY")

# agent = Agent(  
#     'google-gla:gemini-1.5-flash',
#     system_prompt='Be concise, reply with one sentence.',  
# )

# result1 = agent.run_sync('Where does India come from?')  

# print("The first result is:")
# # print(result1)
# print(result1.data)
# # print(result1._usage)

# result2 = agent.run_sync('What was the first question I said?',message_history=result1._all_messages)
# print("The second result is:")
# # print(result2)
# print(result2.data)
# # print(result2._usage)

'''
Pydantic AI is great for structured output.
'''

# # Example 1 with float rating
# from pydantic import BaseModel

# class Response(BaseModel):
#     rating: float

# agent = Agent(
#     'google-gla:gemini-1.5-flash',
#     system_prompt='Given a movie review, rate it from 1 to 10.',
#     result_type=Response
# )


# result = agent.run_sync('The movie is super slow and boring.')
# print(result.data)

# # Example 2 with int rating
# from pydantic import BaseModel

# class Response(BaseModel):
#     rating: int


# agent = Agent(
#     'google-gla:gemini-1.5-flash',
#     system_prompt='Given a movie review, rate it from 1 to 10.',
#     result_type=Response
# )

# result = agent.run_sync('The movie is super slow and boring.')
# print(result.data)

'''
A better structured output example
'''

from pydantic import BaseModel
from enum import Enum

class Action(str, Enum):
    Yes = 'Yes'
    No = 'No'

class Response(BaseModel):
    rating: float
    action_take: Action

agent = Agent(
    'google-gla:gemini-1.5-flash',
    system_prompt='Given a product review, rate it from 1 to 10 and decide if the internal team needs to take action for bad reviews.',
    result_type=Response
)

result = agent.run_sync('The product is super slow and boring.')
print(result.data)


