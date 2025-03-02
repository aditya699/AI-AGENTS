from openai import AzureOpenAI

def summarize_content(client, url, content, input_token_tracker, output_token_tracker):
    """Summarize the content from a URL using LLM"""
    print(f"\n--- Starting Content Summarization for {url} ---")
    try:
        print("Preparing summary prompt...")
        SUMMARY_PROMPT = f"""
        Please extract all meaningful information that can be used by an analyst to draft a detailed report from the following content at the URL: {url}
        
        CONTENT:
        {content}  
        
        Provide a comprehensive summary that captures the key insights and details.
        """
        
        print("Sending request to LLM...")
        completion = client.chat.completions.create(
            model="mini-deployment",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that Extracts the key information from the web content accurately.Only Extract Meaningful Information from the content.Do not add any other text apart from the summary"},
                {"role": "user", "content": SUMMARY_PROMPT},
            ]
        )
        
        # Update token trackers
        input_token_tracker += completion.usage.prompt_tokens
        output_token_tracker += completion.usage.completion_tokens
        print(f"Tokens used - Input: {completion.usage.prompt_tokens}, Output: {completion.usage.completion_tokens}")
        
        summary = completion.choices[0].message.content
        print("Summary generated successfully")
        print(f"Summary length: {len(summary)} characters")
        print("--- Content Summarization Complete ---\n")
        return summary, input_token_tracker, output_token_tracker
    
    except Exception as e:
        print(f"❌ Error summarizing content from {url}: {e}")
        print("--- Content Summarization Failed ---\n")
        return f"Failed to summarize content from {url}", input_token_tracker, output_token_tracker
