#tool calling

from agents import Agent, Runner, trace, set_tracing_export_api_key
import os
from dotenv import load_dotenv
from agents.tool import function_tool

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") # type: ignore

# Set the tracing export API key
set_tracing_export_api_key(os.getenv("OPENAI_API_KEY")) # type: ignore

agent_1 = Agent(
    name="Health Advisor",
    instructions="You are a health advisor.You have access to a tool called bmi_calculator.You need to calculate the bmi of the user based on their weight and height.",
    model="gpt-4o-mini")

@function_tool
def bmi_calculator(weight_in_kg: float, height_in_m: float) -> float:
    """
    Calculate the Body Mass Index (BMI) of a person.
    """
    bmi = weight_in_kg / (height_in_m ** 2)

    if bmi < 18.5:
        return "You are underweight" # type: ignore
    elif bmi >= 18.5 and bmi <= 24.9:
        return "You are normal weight" # type: ignore
    elif bmi >= 25 and bmi <= 29.9:
        return "You are overweight" # type: ignore
    else:
        return "You are obese" # type: ignore
    
agent_1.tools.append(bmi_calculator)

# Using trace without conditional check since we've set the API key explicitly
with trace("health_agent"):
    result = Runner.run_sync(agent_1, "My height is 1.8 m and my weight is 70 kg, what is my bmi?")
    print(result.final_output)
