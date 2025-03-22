#input->Llm1->output1->llm2_>final_output

from agents import Agent,Runner
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

agent_1=Agent(
    name="Agent 1",
    instructions="based on the review, return the rating in 1-5 scale",
)

agent_2=agent_1.clone(
    name="Agent 2",
    instructions="based on the rating, return the sentiment as positive or negative",
)

result=Runner.run_sync(agent_2,"Bad product")

print(result.final_output)
