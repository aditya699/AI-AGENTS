'''
Author : Aditya Bhatt 24-02-2025 

NOTE:
1.We are to create a deep research clone

BUG:

TODO:

'''



from client.azure import Client
from openai import AzureOpenAI
from schemas.user_query import UserQuery
import matplotlib.pyplot as plt


input_token_tracker = 0
output_token_tracker = 0
print("Current token count: (for the run of this script)",input_token_tracker+output_token_tracker)

print("Current script running cost ",0 , "dollars")

user_query = input("Enter the topic on which you want to do research on : ")

print(f"User Query: {user_query}")

USER_QUERY_PROMPT=f"""
Given the user query transform it into a search query for a search engine.Only return the search query, no other text.Do not add any other text apart from the user query.

Example:
User Query: "What is the weather in Tokyo?"
Search Query: "weather in Tokyo"

User Query: "Need help about the latest trends in AI"
Search Query: "latest trends in AI"

User Query: {user_query}

"""

print("Here is the prompt for the llm to transform the user query into a search query: ",USER_QUERY_PROMPT)

# Initialize the Azure OpenAI client
azure_client = Client()

# Get the Azure OpenAI client
client = azure_client.get_azure_client()


try:
    completion = client.beta.chat.completions.parse(
        model="mini-deployment", # replace with the model deployment name of your gpt-4o 2024-08-06 deployment
        messages=[
            {"role": "system", "content": "You are a helpful assistant that transforms user queries into search queries for a search engine."},
            {"role": "user", "content": USER_QUERY_PROMPT},
        ],
        response_format=UserQuery,
    )
    
    # Update token trackers
    input_token_tracker += completion.usage.prompt_tokens
    output_token_tracker += completion.usage.completion_tokens
    print("LLM response has been generated successfully")

    search_query= completion.choices[0].message.parsed

    print("Here is the search query: ",search_query.query)



    total_tokens = input_token_tracker + output_token_tracker
    cost_per_million_tokens = 0.15
    cached_cost_per_million_tokens = 0.075
    output_cost_per_million_tokens = 0.60

    current_cost = (total_tokens / 1_000_000) * cost_per_million_tokens
    print("Current token count: (for the run of this script)", total_tokens)
    print("Current script running cost: ${:.5f} dollars".format(current_cost))

    # Create a plot for token usage and cost
    plt.figure(figsize=(10, 5))
    plt.bar(['Input Tokens', 'Output Tokens', 'Current Cost'], 
            [input_token_tracker, output_token_tracker, current_cost], 
            color=['blue', 'orange', 'green'])
    plt.title('Token Usage and Cost')
    plt.ylabel('Value')
    plt.xlabel('Type')
    plt.axhline(y=total_tokens, color='r', linestyle='--', label='Total Tokens')
    plt.legend()
    plt.grid(axis='y')
    plt.show()



except Exception as e:
    print("Error in generating the LLM response: ",e)

