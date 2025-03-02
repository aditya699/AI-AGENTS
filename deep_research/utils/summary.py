from openai import AzureOpenAI
from pydantic import BaseModel

class Summary(BaseModel):
    content_extracted: str

def summarize_content(client, url, content, input_token_tracker, output_token_tracker):
    """Summarize the content from a URL using LLM"""
    print(f"\n--- Starting Content Summarization for {url} ---")
    try:
        print("Preparing summary prompt...")
        SUMMARY_PROMPT = f"""
        You are a helpful assistant that extracts essential information from raw HTML content. The extracted content should be concise and relevant, enabling an analyst to create a comprehensive report. Please eliminate any extraneous text and focus on delivering the main content.
        
        CONTENT:
        {content}  
        
        """
        
        print("Sending request to LLM...")
        completion = client.beta.chat.completions.parse(
            model="mini-deployment",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that Extracts the key information from the web content accurately.Only Extract Meaningful Information from the content.Do not add any other text apart from the summary"},
                {"role": "user", "content": SUMMARY_PROMPT},
            ],
            response_format=Summary,
        )
        
        # Update token trackers
        input_token_tracker += completion.usage.prompt_tokens
        output_token_tracker += completion.usage.completion_tokens
        # print(f"Tokens used - Input: {completion.usage.prompt_tokens}, Output: {completion.usage.completion_tokens}")
        print(completion.choices[0].message)
        summary = completion.choices[0].message.parsed

        print("Summary generated successfully")
        # print(f"Summary length: {len(summary)} characters")
        # print("--- Content Summarization Complete ---\n")
        return summary.content_extracted, input_token_tracker, output_token_tracker
    
    except Exception as e:
        print(f"❌ Error summarizing content from {url}: {e}")
        print("--- Content Summarization Failed ---\n")
        return f"Failed to summarize content from {url}", input_token_tracker, output_token_tracker
