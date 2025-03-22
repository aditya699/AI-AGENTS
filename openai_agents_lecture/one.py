from agents import Agent,Runner
import os
from dotenv import load_dotenv
load_dotenv()
from pydantic import BaseModel

#this is known as structured output
class Joke(BaseModel):
    joke: str
    topic: str

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

agent=Agent(
    name="Joke Assistant",
    instructions="You are a joke assistant,which returns a joke and topic",
    model="gpt-4o-mini",
    output_type=Joke
)

result=Runner.run_sync(agent,"Tell me a joke")

print(result.final_output.joke)
print(result.final_output.topic)




