from schemas.user_query import ResearchQuery

def get_research_queries(client, search_query, input_token_tracker, output_token_tracker):
    """Generate research queries from the search query"""
    print("\n=== Starting Research Queries Generation ===")
    print("Processing search query:", search_query)
    
    RESEARCH_PROMPT = f"""
        Please analyze the following search query and decompose it into a list of specific research queries that are suitable for detailed reporting and analysis.

        Example:
        Search Query: "latest trends in AI"
        Research Queries: ["History of AI","Current Trends in AI","Future Trends in AI","Opportunities in AI","Challenges in AI","Can AI Replace Humans?"]

        Search Query: {search_query}

    """

    print("Preparing research prompt for LLM...")
    print("Research prompt:", RESEARCH_PROMPT)

    try:
        print("Sending request to LLM...")
        completion = client.beta.chat.completions.parse(
            model="mini-deployment",  # replace with the model deployment name of your gpt-4o 2024-08-06 deployment
            messages=[
                {"role": "system", "content": "You are a helpful assistant that transforms user queries into research queries for a research report."},
                {"role": "user", "content": RESEARCH_PROMPT},
            ],
            response_format=ResearchQuery,
        )

        # Update token trackers
        input_token_tracker += completion.usage.prompt_tokens
        output_token_tracker += completion.usage.completion_tokens
        print(f"Tokens used - Input: {completion.usage.prompt_tokens}, Output: {completion.usage.completion_tokens}")
        print("LLM response generated successfully")

        research_queries = completion.choices[0].message.parsed
        print("Generated research queries:", research_queries.queries)
        print("=== Research Queries Generation Complete ===\n")
        
        return research_queries, input_token_tracker, output_token_tracker
    
    except Exception as e:
        print("❌ Error in generating research queries:", e)
        print("=== Research Queries Generation Failed ===\n")
        return None, input_token_tracker, output_token_tracker