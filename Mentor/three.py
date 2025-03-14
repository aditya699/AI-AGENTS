# structured output 
from agents import Agent, Runner
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") # type: ignore

#Create a structured output agent
agent_1 = Agent(
    name="Reviewer", # type: ignore
    instructions="Review the following comment and assign a rating between 1 and 5(5 being the highest and 1 being the lowest)",
    output_type=int,
    model="gpt-4o-mini"
)

agent_2 = agent_1.clone(
    name="analyst",
    instructions="Analyze the rating(1-5(5 being the highest and 1 being the lowest)) and classify the comment as positive, negative or neutral",
    output_type=str,
    model="gpt-4o-mini"
)

final_result = Runner.run_sync(agent_2, "Shitty product, team is not good")
print(final_result.final_output)


