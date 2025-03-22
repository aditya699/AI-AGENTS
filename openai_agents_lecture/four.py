# handoffs

from agents import Agent,Runner
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

agent_1=Agent(
    name="Hindi agent",
    instructions="You are a hindi agent, which can talk in hindi"
    
)

agent_2=Agent(
    name="English agent",
    instructions="You are a english agent, which can talk in english"
)

#handoff

agent_3=Agent(
    name="Language agent",
    instructions="You are a language agent, which delegates the conversation to the appropriate agent based on the language of the user",
    handoffs=[agent_1,agent_2]
)

result=Runner.run_sync(agent_3,"Hello how are you")

print(result.final_output)

