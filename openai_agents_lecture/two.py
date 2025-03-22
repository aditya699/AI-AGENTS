# tool calling

from agents import Agent,Runner,trace,set_tracing_export_api_key
import os
from dotenv import load_dotenv
from agents.tool import function_tool 

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
set_tracing_export_api_key(os.getenv("OPENAI_API_KEY"))

agent_1=Agent(
    name="Health Assistant",
    instructions="You are a health assistant, which has access to a BMI calculator tool which takes weight in kg and height in m and returns the BMI of the person",
)

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
        return "You are obese" # type: ignor
    
agent_1.tools.append(bmi_calculator)

with trace("health_assistant_1") as run:
    result=Runner.run_sync(agent_1,"What is my BMI if I weigh 70 kg and am 1.8m tall?")

print(result.final_output)


