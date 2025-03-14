#structured output (pydantic)

from agents import Agent, Runner
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") # type: ignore

class Review(BaseModel):
    rating: int
    sentiment: str

agent = Agent(
    name="Reviewer",
    instructions="Review the following comment and assign a rating between 1 and 5(5 being the highest and 1 being the lowest)",
    output_type=Review,
    model="gpt-4o-mini"
)

result = Runner.run_sync(agent, "This product is amazing, I love it!")
print(result.final_output)
print(result.final_output.rating)
print(result.final_output.sentiment)

