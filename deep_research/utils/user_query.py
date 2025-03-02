from schemas.user_query import UserQuery


def get_search_query(client, user_query, input_token_tracker, output_token_tracker):
    """Transform user query into search query using LLM"""
    print("\n=== Starting Search Query Generation ===")
    USER_QUERY_PROMPT = f"""
    Given the user query transform it into a search query for a search engine.Only return the search query, no other text.Do not add any other text apart from the user query.

    Example:
    User Query: "What is the weather in Tokyo?"
    Search Query: "weather in Tokyo"

    User Query: "Need help about the latest trends in AI"
    Search Query: "latest trends in AI"

    User Query: {user_query}

    """
    print("Preparing prompt for LLM...")
    print("User query prompt:", USER_QUERY_PROMPT)

    try:
        print("Sending request to LLM...")
        completion = client.beta.chat.completions.parse(
            model="mini-deployment",  # replace with the model deployment name of your gpt-4o 2024-08-06 deployment
            messages=[
                {"role": "system", "content": "You are a helpful assistant that transforms user queries into search queries for a search engine."},
                {"role": "user", "content": USER_QUERY_PROMPT},
            ],
            response_format=UserQuery,
        )
        
        # Update token trackers
        input_token_tracker += completion.usage.prompt_tokens
        output_token_tracker += completion.usage.completion_tokens
        # print(f"Tokens used - Input: {completion.usage.prompt_tokens}, Output: {completion.usage.completion_tokens}")
        # print("LLM response generated successfully")

        search_query = completion.choices[0].message.parsed
        print("Generated search query:", search_query.query)
        print("=== Search Query Generation Complete ===\n")
        
        return search_query, input_token_tracker, output_token_tracker
    
    except Exception as e:
        print("❌ Error in generating the LLM response: ", e)
        print("=== Search Query Generation Failed ===\n")
        return None, input_token_tracker, output_token_tracker