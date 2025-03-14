# structured output 

from agents import Agent, ModelSettings, Runner
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") # type: ignore

#Create a structured output agent
agent = Agent(
    name="Reviewer", # type: ignore
    instructions="Review the following comment and assign a rating between 1 and 5(5 being the highest and 1 being the lowest)",
    output_type=int,
    model="gpt-4o",
    model_settings=ModelSettings(temperature=0.3)
)

#Run the agent
result = Runner.run_sync(agent, "Great product, Cracked team is awesome")
print(result.final_output)


