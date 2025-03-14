# Create a basic agent

#Library
from agents import Agent, Runner
import os
from dotenv import load_dotenv
#Load the environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") # type: ignore

#name means the name of the agent 
#Instructions (like system prompts or dynamic instructions)

#Create a basic agent
agent = Agent(name="Assistant", instructions="You are a Joke Teller, Return funny jokes")

#Run the agent
result = Runner.run_sync(agent, "Write a joke on people who play cricket")
print(result.final_output)
