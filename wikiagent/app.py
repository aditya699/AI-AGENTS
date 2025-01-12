'''
Can we create a simple agent that will help me generate a single wiki page?

NOTE:
This is a simple agent that will help you generate a wiki page, which made using simple python and langchain no fancy stuff.
'''
import os
import re
import streamlit as st


os.environ["GOOGLE_API_KEY"] = st.secrets["GEMINI_API_KEY"]

from langchain_google_genai import ChatGoogleGenerativeAI

st.header("Wiki Single Page Generator")
st.write("This is a simple agent that will help you generate a wiki page using Python and Langchain.")
st.write("This should be used for projects where you want to generate a single page wiki for a project.")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest")

# Input fields
project_description = st.text_area("Enter the project description:")
what_you_did = st.text_area("Enter what you did:")
what_you_learned = st.text_area("Enter what you learned:")
what_tech_stack_used = st.text_area("Enter what tech stack you used:")
any_special_message = st.text_area("Enter any special message:")

did_you_use_any_urls = st.radio("Did you use any URLs?", ("yes", "no"))

if did_you_use_any_urls == "yes":
    urls = st.text_input("Enter the URLs (separated by commas):")
else:
    urls = "No URL was used in this project."

if st.button("Generate Wiki"):
    with st.spinner("Generating project description..."):
        worker1_prompt = f"""
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

        worker1_response = llm.invoke(worker1_prompt)
        project_description = extract_project_description(worker1_response.content)
        st.write("Project Description:", project_description)

    with st.spinner("Generating methodology..."):
        worker2_prompt = f"""
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

        worker2_response = llm.invoke(worker2_prompt)
        methodology = extract_methodology(worker2_response.content)
        st.write("Methodology:", methodology)

    with st.spinner("Generating tech stack..."):
        worker3_prompt = f"""
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

        worker3_response = llm.invoke(worker3_prompt)
        tech_stack = extract_tech_stack(worker3_response.content)
        st.write("Tech Stack:", tech_stack)

    with st.spinner("Generating other notes..."):
        worker4_prompt = f"""
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

        worker4_response = llm.invoke(worker4_prompt)
        other_notes = extract_other_notes(worker4_response.content)
        st.write("Other Notes:", other_notes)

    with st.spinner("Generating mermaid chart..."):
        worker5_prompt = f"""
        You are a mermaid chart expert.(Never add any other information to the mermaid chart which is not given to you)

        You are given a project description: {project_description}

        You are also given what the developer did: {what_you_did}

        You are also given what tech stack the developer used: {what_tech_stack_used}.(Never add any other information to the mermaid chart which is not given to you)

        You are also given any special message: {any_special_message}.(Never add any other information to the mermaid chart which is not given to you)

        You need to give a mermaid chart for the project.(The project flow and the tech stack used should be clearly visible in the mermaid chart,make sure simple flow diagram kind of files)

        example:
        ```mermaid
            graph LR
            A[Project: Forecast Sales FY2025] --> B[Historical Data];
            B --> C[LSTM Arch];
            C --> D[Neural Net Training];
            D --> E[Azure VM GPU];
            E --> F[PyTorch/Python];
            F --> G[Sales Forecast];
            G --> A;
            subgraph "Tech Stack"
            F
            E
            end
        ```

        Note: Do not use curly braces for nodes - use square brackets [] instead. Valid node shapes include:
        - square/rectangle [text]

        Always have [text] for nodes.do not use brackets or any other special characters inside the brackets([]).
  

        Always follow the XML format strictly(only output the XML format, nothing else).

        <mermaid_chart>
        Enter here the mermaid chart.
        </mermaid_chart>
        """

        def extract_mermaid_chart(text):
            return text.split('```')[1].split('<mermaid_chart>')[1].split("</mermaid_chart>")[0].strip()

        worker5_response = llm.invoke(worker5_prompt)
        mermaid_chart = extract_mermaid_chart(worker5_response.content)
        st.write("Mermaid Chart:", mermaid_chart)

    with st.spinner("Validating mermaid chart..."):
        worker7_prompt = f"""
        You are a mermaid chart expert.

        You are given a mermaid chart: {mermaid_chart}

        Make sure the syntax is correct.

        Do not add any other information to the mermaid chart.
                example:
        ```mermaid
            graph LR
            A[Project: Forecast Sales FY2025] --> B[Historical Data];
            B --> C[LSTM Arch];
            C --> D[Neural Net Training];
            D --> E[Azure VM GPU];
            E --> F[PyTorch/Python];
            F --> G[Sales Forecast];
            G --> A;
            subgraph "Tech Stack"
            F
            E
            end
        ```

   
        Note: Do not use curly braces for nodes - use square brackets [] instead. Valid node shapes include:
        - square/rectangle [text]

        Always have [text] for nodes.do not use brackets or any other special characters inside the brackets([]).

        Always follow the XML format strictly(only output the XML format, nothing else).

        <mermaid_chart>
        <mermaid_chart>
        Enter here the mermaid chart.
        </mermaid_chart>
        """

        def extract_mermaid_chart(text):
            return text.split('```')[1].split('<mermaid_chart>')[1].split("</mermaid_chart>")[0].strip()

        worker7_response = llm.invoke(worker7_prompt)
        mermaid_chart = extract_mermaid_chart(worker7_response.content)
        st.write("Mermaid Chart:", mermaid_chart)


    with st.spinner("Generating learning..."):
        worker6_prompt = f"""
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

        worker6_response = llm.invoke(worker6_prompt)
        learning = extract_learning(worker6_response.content)
        st.write("Learning:", learning)

    with st.spinner("Generating final markdown..."):
        main_prompt = f"""
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

        You need to generate a md file for the project.(Make sure to add following to the md file: Project Description, Methodology, Tech Stack, Other Notes, Mermaid Chart(Architecture), Urls(If any), and Learning)

        Always follow the XML format strictly(only output the XML format, nothing else).

        <md_file>
        Enter here the md file.
        </md_file>
        """

        def extract_md_file(text):
            """
            Extracts content between <md_file> tags from a text string, handling nested code blocks
            including Mermaid charts.
            """
            import re
            
            clean_text = text.strip('`')
            if clean_text.startswith('xml'):
                clean_text = clean_text[3:].lstrip()
                
            pattern = r'<md_file>([\s\S]*?)</md_file>'
            match = re.search(pattern, clean_text)
            
            if not match:
                raise ValueError("No <md_file> tags found in the input text")
                
            content = match.group(1)
            return content.strip()

        worker6_response = llm.invoke(main_prompt)
        md_file = extract_md_file(worker6_response.content)
        
        st.markdown("## Generated Wiki")
        st.markdown(md_file)
        
        # Save to file and trigger download
        st.download_button(
            label="Download Wiki",
            data=md_file,
            file_name="wiki.md",
            mime="text/markdown"
        )
        st.success("Wiki has been generated! Click above to download.")
