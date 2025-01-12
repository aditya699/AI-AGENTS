'''
Can we create a simple agent that will help me generate a wiki page?

NOTE:
This is a simple agent that will help you generate a wiki page, which made using simple python and langchain no fancy stuff.
'''
import os
from dotenv import load_dotenv
import re

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest")

project_description=input("Enter the project description:")

what_you_did=input("Enter what you did:")

what_you_learned=input("Enter what you learned:")

what_tech_stack_used=input("Enter what tech stack you used:")

any_special_message=input("Enter any special message:")

did_you_use_any_urls=input("Did you use any urls?(enter yes or no)")

if did_you_use_any_urls=="yes":
    urls=input("Enter the urls(separated by commas):")

else:
    urls="No URL was used in this project."

worker1_prompt=f"""
You are a project description expert.

you are given a project description: {project_description}

Redraft the project description in a way that is more clear.so that any one who reads it can understand it.(Never add any other information to the project description which is not given to you)

Always follow the XML format strictly(only output the XML format, nothing else).

<project_description>
Enter here the redrafted project description.
</project_description>
"""

def extract_project_description(text):
    return text.split('```')[1].split('<project_description>')[1].split("</project_description>")[0].strip()

worker1_response=llm.invoke(worker1_prompt)

project_description=extract_project_description(worker1_response.content)

print(project_description)

worker2_prompt=f"""
You are a Methodology expert.

You are given a project description: {project_description}

You are also given what the developer did: {what_you_did}.(Never add any other information to the methodology which is not given to you)

You need to write a methodology for the project.

Always follow the XML format strictly(only output the XML format, nothing else).

<methodology>
Enter here the methodology focussing on what the developer did.
</methodology>
"""

def extract_methodology(text):
    return text.split('```')[1].split('<methodology>')[1].split("</methodology>")[0].strip()

worker2_response=llm.invoke(worker2_prompt)

methodology=extract_methodology(worker2_response.content)

print(methodology)

worker3_prompt=f"""
You are a tech stack expert.

You are given project description: {project_description}

You are also given what the developer did: {what_you_did}.(Never add any other information to the tech stack which is not given to you)

You are given what tech stack the developer used: {what_tech_stack_used}

You need to write a tech stack used for the project.

Always follow the XML format strictly(only output the XML format, nothing else).

<tech_stack>
Enter here the tech stack.
</tech_stack>
"""

def extract_tech_stack(text):
    return text.split('```')[1].split('<tech_stack>')[1].split("</tech_stack>")[0].strip()

worker3_response=llm.invoke(worker3_prompt)

tech_stack=extract_tech_stack(worker3_response.content)

print(tech_stack)

worker4_prompt=f"""
You are a other notes expert.

You are given a project description: {project_description}

You are also given what the developer did: {what_you_did}

You are also given what tech stack the developer used: {what_tech_stack_used}.(Never add any other information to the other notes which is not given to you)

You are also given any special message: {any_special_message}.(Never add any other information to the other notes which is not given to you)

You need to write a other notes for the project.

Always follow the XML format strictly(only output the XML format, nothing else).

<other_notes>
Enter here the other notes.
</other_notes>
"""

def extract_other_notes(text):
    return text.split('```')[1].split('<other_notes>')[1].split("</other_notes>")[0].strip()

worker4_response=llm.invoke(worker4_prompt)

other_notes=extract_other_notes(worker4_response.content)

print(other_notes)

worker5_prompt=f"""
You are a mermaid chart expert.(Never add any other information to the mermaid chart which is not given to you)

You are given a project description: {project_description}

You are also given what the developer did: {what_you_did}

You are also given what tech stack the developer used: {what_tech_stack_used}.(Never add any other information to the mermaid chart which is not given to you)

You are also given any special message: {any_special_message}.(Never add any other information to the mermaid chart which is not given to you)

You need to give a mermaid chart for the project.

Always follow the XML format strictly(only output the XML format, nothing else).

<mermaid_chart>
Enter here the mermaid chart.
</mermaid_chart>
"""

def extract_mermaid_chart(text):
    return text.split('```')[1].split('<mermaid_chart>')[1].split("</mermaid_chart>")[0].strip()

worker5_response=llm.invoke(worker5_prompt)

mermaid_chart=extract_mermaid_chart(worker5_response.content)

print(mermaid_chart)

worker6_prompt=f"""
You are experrt in writing project learning.

You are given a project description: {project_description}

You are given what learning the developer got: {what_you_learned}.(Never add any other information to the learning which is not given to you)

You need to write a learning for the project.

Always follow the XML format strictly(only output the XML format, nothing else).

<learning>
Enter here the learning.
</learning>
"""

def extract_learning(text):
    return text.split('```')[1].split('<learning>')[1].split("</learning>")[0].strip()

worker6_response=llm.invoke(worker6_prompt)

learning=extract_learning(worker6_response.content)

print(learning)

main_prompt=f"""
You are a md file expert.
You need to generate a md file for the project.

Project Description: {project_description}

Methodology: {methodology}

Tech Stack: {tech_stack}

Other Notes: {other_notes}

Mermaid Chart: {mermaid_chart}

Urls: {urls}

Learning: {learning}

(Never add any other information to the md file which is not given to you)

You need to generate a md file for the project.(Make sure to add following to the md file: Project Description, Methodology, Tech Stack, Other Notes, Mermaid Chart, Urls(If any), and Learning)

Always follow the XML format strictly(only output the XML format, nothing else).

<md_file>
Enter here the md file.
</md_file>
""" 

def extract_md_file(text):
    """
    Extracts content between <md_file> tags from a text string, handling nested code blocks
    including Mermaid charts.
    
    Args:
        text (str): Input text containing markdown content wrapped in <md_file> tags
        
    Returns:
        str: Extracted content between <md_file> tags, with proper handling of nested code blocks
        
    Example:
        >>> text = '''```xml
        ... <md_file>
        ... # Header
        ... ```mermaid
        ... graph LR
        ... A --> B
        ... ```
        ... </md_file>
        ... ```'''
        >>> print(extract_md_file(text))
        # Header
        ```mermaid
        graph LR
        A --> B
        ```
    """
    import re
    
    # First, remove the outer code block markers if present
    clean_text = text.strip('`')
    if clean_text.startswith('xml'):
        clean_text = clean_text[3:].lstrip()
        
    # Extract content between md_file tags
    pattern = r'<md_file>([\s\S]*?)</md_file>'
    match = re.search(pattern, clean_text)
    
    if not match:
        raise ValueError("No <md_file> tags found in the input text")
        
    content = match.group(1)
    return content.strip()

worker6_response=llm.invoke(main_prompt)
print(worker6_response.content)

md_file=extract_md_file(worker6_response.content)

print(md_file)

with open("wiki.md","w") as f:
    f.write(md_file)

