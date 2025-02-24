from pydantic import BaseModel
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class Client:
    def __init__(self):
        self.client = None

    def get_azure_client(self):
        """Creates and returns Azure OpenAI API client"""
        try:
            client = AzureOpenAI(
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT") or "", 
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                api_version="2024-10-21"
            )
            return client
        except Exception as e:
            print(f"Error creating Azure client: {e}")
            return None

