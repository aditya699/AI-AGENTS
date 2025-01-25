from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")

async def main():
    agent = Agent(
        task="find me jobs with the keyword 'AI' in the title and 2 years of experience",
        llm=llm,
        max_failures=10,
        generate_gif=False
    )
    result = await agent.run()

    print(result)

asyncio.run(main())
