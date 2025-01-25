# Lecture 16 Stream Response
import asyncio
import os
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

os.environ["GOOGLE_API_KEY"]=os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest")
prompt = ChatPromptTemplate.from_template("tell me a essay about {topic}")
parser = StrOutputParser()
chain = prompt | llm | parser

async def stream_response():
    async for event in chain.astream_events({"topic": "India"}, version="v2"):
        kind = event["event"]
        if kind == "on_chat_model_stream":
            print(event['data'], end="|", flush=True)

asyncio.run(stream_response())