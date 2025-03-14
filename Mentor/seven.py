from agents import Agent, Runner, input_guardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")  # type: ignore

# This function acts as a guardrail to check incoming messages
@input_guardrail
async def bad_word_checker(ctx,agent,message):
    """
    Input guardrail function to check for inappropriate words in user messages.
    
    Parameters:
        ctx: The context object containing metadata about the current conversation and execution state.
            This includes information like conversation history, run IDs, and other execution context.
        
        agent: The Agent instance that is processing this message. This allows the guardrail
            to access agent properties like name, instructions, or other configuration.
            
        message: The actual user input text that needs to be checked by this guardrail.
    
    Returns:
        GuardrailFunctionOutput: Contains the result of the check and whether to trigger the tripwire.
    """
    # Define the word we want to filter out
    bad_word = "badword"
    
    # Check if the message contains the bad word (case-insensitive)
    found_bad_word = bad_word in message.lower()
    
    # Return the result of our check
    return GuardrailFunctionOutput(
        output_info={"found_bad_word": found_bad_word},  # Additional information about the check
        tripwire_triggered=found_bad_word  # When True, this raises an InputGuardrailTripwireTriggered exception
    )

# Initialize an agent with our input guardrail
agent = Agent(
    name="WordChecker",
    instructions="Check messages for bad words",
    input_guardrails=[bad_word_checker]  # Apply our guardrail function to filter incoming messages
)

# Test the agent with a message that should pass the filter
result = Runner.run_sync(agent, "Hi, bro")
print(result.final_output)

# Test with a message containing a filtered word
try:
    # This should trigger our guardrail since it contains "badword"
    result = Runner.run_sync(agent, "This message has a badword in it.")
    print("Our filter missed the bad word!")
except InputGuardrailTripwireTriggered as e:
    # This exception handler runs when the guardrail is triggered
    # The exception is raised because tripwire_triggered was set to True
    print("Our filter caught the bad word!")
