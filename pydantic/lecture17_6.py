from pydantic_ai import Agent
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GEMINI_API_KEY"]=os.getenv("GEMINI_API_KEY")

agent = Agent(  
    'google-gla:gemini-1.5-flash',
    system_prompt='Be concise, reply with one sentence.',  
)

result1 = agent.run_sync('Where does India come from?')  

print("The first result is:")
# print(result1)
print(result1.data)
# print(result1._usage)

result2 = agent.run_sync('What was the first question I said?',message_history=result1._all_messages)
print("The second result is:")
# print(result2)
print(result2.data)
# print(result2._usage)