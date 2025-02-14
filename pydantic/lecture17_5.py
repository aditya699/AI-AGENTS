'''
1. Dependency Injection (DI) is a design pattern where dependencies (external services, databases, API clients, etc.) 
   are provided to a class or function rather than being hardcoded inside it. 
   This makes code more modular, reusable, and testable.

2. In this code, we are implementing DI using a `dataclass` (MyDeps), which injects:
   - An API key (used for authorization)
   - An asynchronous HTTP client (`httpx.AsyncClient`) for making API requests.

3. Instead of directly defining a static system prompt, we dynamically fetch the prompt from an external API 
   (`https://example.com`) using DI.

4. The AI agent (`Agent`) is created using the `pydantic_ai` library and configured to use `gemini-1.5-flash`.

5. The `main()` function runs the agent and prints a response to a user query.
'''

# Import necessary libraries
from dataclasses import dataclass  # For creating dependency injection structure
import asyncio  # For handling asynchronous execution
import httpx  # Asynchronous HTTP client for making API calls

# Import AI-related classes from pydantic_ai
from pydantic_ai import Agent, RunContext

import os
from dotenv import load_dotenv  # To load environment variables securely

# Load environment variables from .env file
load_dotenv()
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")  # Store API key in environment variable

# --------------------------- Dependency Injection Setup ---------------------------
@dataclass  # `dataclass` is used to automatically generate __init__, __repr__, etc.
class MyDeps:
    """
    This dataclass is used for Dependency Injection.
    
    It contains:
    - `api_key`: A string storing the API key used for authentication.
    - `http_client`: An instance of `httpx.AsyncClient` for making asynchronous HTTP requests.
    """
    api_key: str
    http_client: httpx.AsyncClient  # Asynchronous HTTP client

# --------------------------- AI Agent Configuration ---------------------------
agent = Agent(
    'google-gla:gemini-1.5-flash',  # Specifies the LLM model to be used
    deps_type=MyDeps,  # Defines the dependency injection type for the agent
)

# --------------------------- Dynamic System Prompt Function ---------------------------
@agent.system_prompt  # This decorator registers the function to generate a system prompt dynamically
async def get_system_prompt(ctx: RunContext[MyDeps]) -> str:
    """
    This function dynamically generates the system prompt for the AI agent.

    - It retrieves text from an external API (`https://example.com`).
    - Uses Dependency Injection (`ctx.deps`) to access:
      - `http_client`: Injected HTTP client for making requests.
      - `api_key`: Injected API key for authentication.
    - Returns the fetched text as a formatted system prompt.

    Parameters:
    - ctx: RunContext[MyDeps] → Provides access to injected dependencies.

    Returns:
    - str: The dynamically fetched system prompt.
    """
    response = await ctx.deps.http_client.get(  # Make an asynchronous HTTP GET request
        'https://example.com',
        headers={'Authorization': f'Bearer {ctx.deps.api_key}'},  # Add API key for authentication
    )
    response.raise_for_status()  # Raise an error if the request fails
    print(f"Response: {response.text}")
    return f'Prompt: {response.text}'  # Return the fetched response text as the system prompt

# --------------------------- Main Function to Run AI Agent ---------------------------
async def main():
    """
    This function initializes the dependencies and runs the AI agent.

    - Creates an instance of `httpx.AsyncClient` for making async HTTP requests.
    - Injects `MyDeps` dependencies (API key + HTTP client) into the AI agent.
    - Calls the AI agent to generate a response for the prompt "Tell me a joke."
    - Prints the response.

    Expected Output:
    - Example: "Did you hear about the toothpaste scandal? They called it Colgate."
    """
    async with httpx.AsyncClient() as client:  # Create an async HTTP client session
        deps = MyDeps('foobar', client)  # Inject dependencies with a placeholder API key
        result = await agent.run('Tell me a joke.', deps=deps)  # Run the AI agent with injected dependencies
        print(result.data)  # Print the response from the AI agent

# --------------------------- Entry Point for Script Execution ---------------------------
if __name__ == '__main__':
    """
    Ensures the script runs only when executed directly, not when imported as a module.
    
    `asyncio.run(main())` runs the main function asynchronously.
    """
    asyncio.run(main())
