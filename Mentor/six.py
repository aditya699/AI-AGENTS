#Handoffs let one agent delegate a conversation to another agent. This is useful when you have multiple specialized agents (e.g., a “Spanish-only” agent vs. “English-only” agent) or domain-specific agents (tech support vs. billing).


from agents import Agent, Runner, handoff
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") # type: ignore

spanish_agent = Agent(name="hindi_agent", instructions="You only speak Hindi.")
english_agent = Agent(name="english_agent", instructions="You only speak English.")

triage_agent = Agent(
  name="triage_agent",
  instructions="Handoff to the appropriate agent based on language.",
  handoffs=[spanish_agent, english_agent],
)


out = Runner.run_sync(triage_agent, "क्या हाल है?")
print(out.final_output)
