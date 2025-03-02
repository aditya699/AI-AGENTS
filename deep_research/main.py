'''
Author : Aditya Bhatt 24-02-2025 

NOTE:
1.We are to create a deep research clone

Improvements:
1.Add a better scrapper
2.Add a better LLM at report generation(possibly a fine tuned LLM which specializes in report generation(like a report writer))
3.This works great at a summary level.But it can't go indepth.

(OpenAI have fine tuned model(o3 for deep research(on browser tasks and deep research report creation)),that is only moat they have (internet is for all you don't monopolize it))

Note-Nothing taking away from OPENAI . There deep research is exceptional.But i say we can also reach near that level.

TODO:

'''

from client.azure import Client
from openai import AzureOpenAI
from schemas.user_query import UserQuery, ResearchQuery
from client.serp import get_search_links
from link_scrapper import extract_content_from_urls
import json
import os
from datetime import datetime


def initialize_trackers():
    """Initialize token and cost trackers"""
    print("Initializing token and cost trackers...")
    input_token_tracker = 0
    output_token_tracker = 0
    print("Current token count: (for the run of this script)", input_token_tracker + output_token_tracker)
    print("Current script running cost: $0 (₹0)")
    print("Trackers initialized successfully")
    return input_token_tracker, output_token_tracker


def update_and_display_metrics(input_token_tracker, output_token_tracker, model):
    """Update and display token usage metrics and cost"""
    print("\n--- Updating Metrics ---")
    total_tokens = input_token_tracker + output_token_tracker
    
    if model == "mini":
        mini_input_cost = 0.15  # per million tokens
        mini_output_cost = 0.60  # per million tokens
    elif model == "o1":
        mini_input_cost = 3.30  # per million tokens
        mini_output_cost = 13.20  # per million tokens

    print(f"Input tokens used: {input_token_tracker}")
    print(f"Output tokens used: {output_token_tracker}")


    
    # For mini deployment
    mini_input_cost_total = (input_token_tracker / 1_000_000) * mini_input_cost
    mini_output_cost_total = (output_token_tracker / 1_000_000) * mini_output_cost
    
    # Total cost combining both models
    current_cost =  mini_input_cost_total + mini_output_cost_total
    
    # Convert to rupees (1 USD = 87 INR)
    current_cost_inr = current_cost * 87
    
    print(f"Total token count: {total_tokens}")
    print(f"Input cost: ${ mini_input_cost_total:.5f}")
    print(f"Output cost: ${ mini_output_cost_total:.5f}")
    print("Current script running cost: ${:.5f} (₹{:.2f})".format(current_cost, current_cost_inr))
    print("--- Metrics Updated ---\n")
    
    return total_tokens, current_cost


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
        print(f"Tokens used - Input: {completion.usage.prompt_tokens}, Output: {completion.usage.completion_tokens}")
        print("LLM response generated successfully")

        search_query = completion.choices[0].message.parsed
        print("Generated search query:", search_query.query)
        print("=== Search Query Generation Complete ===\n")
        
        return search_query, input_token_tracker, output_token_tracker
    
    except Exception as e:
        print("❌ Error in generating the LLM response: ", e)
        print("=== Search Query Generation Failed ===\n")
        return None, input_token_tracker, output_token_tracker


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


def save_summaries_to_json(summaries, user_query):
    """Save URL summaries to a JSON file"""
    print("\n=== Starting JSON Save Process ===")
    # Create a directory for research results if it doesn't exist
    print("Creating research_results directory if it doesn't exist...")
    os.makedirs("research_results", exist_ok=True)
    
    # Create a timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"Generated timestamp: {timestamp}")
    
    # Create a safe filename from the user query
    safe_query = "".join(c if c.isalnum() else "_" for c in user_query)[:50]
    print(f"Sanitized query for filename: {safe_query}")
    
    # Create the filename
    filename = f"research_results/{safe_query}_{timestamp}.json"
    print(f"Final filename: {filename}")
    
    # Save the summaries to the JSON file
    print("Writing summaries to JSON file...")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(summaries, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Summaries successfully saved to {filename}")
    print(f"File size: {os.path.getsize(filename)} bytes")
    print("=== JSON Save Process Complete ===\n")
    return filename


def generate_report(client, json_file, input_token_tracker, output_token_tracker):
    """Generate a comprehensive report from the JSON file using LLM"""
    print("\n=== Starting Report Generation ===")
    try:
        # Read the JSON file
        print(f"Reading JSON file: {json_file}")
        with open(json_file, 'r', encoding='utf-8') as f:
            summaries = json.load(f)
        print(f"Successfully loaded {len(summaries)} summaries")
        
        # Prepare the content for the LLM
        print("Preparing content with sources...")
        content_with_sources = ""
        for url, summary in summaries.items():
            content_with_sources += f"Source: {url}\nSummary: {summary}\n\n"
        
        print("Preparing report prompt...")
        REPORT_PROMPT = f"""
        Generate detailed Python code using python-docx to create a comprehensive research report that:

        IMPORTANT:Do not drop any information from the research summaries.(whatever content is present in the research summaries, it should be present in the report
        1. Include all information from the research summaries without dropping any details
        2. Include all source URLs as citations and hyperlinks
        3. Format the content in a clear and readable way

        Output Format(Must contain all the information from the research summaries)(Add URLs as hyperlinks):
        Example Output:
        ```python
            from docx import Document
from docx.shared import Inches, Pt, RGBColor
            from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_LINE_SPACING
            from docx.enum.style import WD_STYLE_TYPE
            from docx.oxml import OxmlElement
            from docx.oxml.ns import qn

            def create_hyperlink(paragraph, url, text):
              
                part = paragraph.part
                r_id = part.relate_to(url, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)
                hyperlink = OxmlElement('w:hyperlink')
                hyperlink.set(qn('r:id'), r_id)
                
                new_run = OxmlElement('w:r')
                rPr = OxmlElement('w:rPr')
                
                # Add blue color and underline
                color = OxmlElement('w:color')
                color.set(qn('w:val'), '0000FF')
                rPr.append(color)
                
                underline = OxmlElement('w:underline')
                underline.set(qn('w:val'), 'single')
                rPr.append(underline)
                
                new_run.append(rPr)
                
                text_element = OxmlElement('w:t')
                text_element.text = text
                new_run.append(text_element)
                
                hyperlink.append(new_run)
                paragraph._p.append(hyperlink)

            def add_heading_style(document, style_name, level):
              
                styles = document.styles
                style = styles.add_style(style_name, WD_STYLE_TYPE.PARAGRAPH)
                style.base_style = styles['Heading ' + str(level)]
                style.paragraph_format.space_before = Pt(12)
                style.paragraph_format.space_after = Pt(6)
                font = style.font
                font.bold = True
                font.size = Pt(14 - level)
                return style

            def add_section_RetryAadd functions and too much formating le't make sure indepth conetent goes inEditHere's a straightforward Python script using python-docx that focuses on generating a comprehensive report with in-depth content about AI in India:
            pythonCopyfrom docx import Document
            from docx.shared import Inches, Pt
            from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
            from docx.oxml import OxmlElement
            from docx.oxml.ns import qn

            # Create a new document
            doc = Document()

            # Function to create a hyperlink
            def create_hyperlink(paragraph, url, text):
                # Create the hyperlink tag
                part = paragraph.part
                r_id = part.relate_to(url, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)
                hyperlink = OxmlElement('w:hyperlink')
                hyperlink.set(qn('r:id'), r_id)
                
                # Create the text run
                new_run = OxmlElement('w:r')
                rPr = OxmlElement('w:rPr')
                
                # Add formatting (blue color and underline)
                color = OxmlElement('w:color')
                color.set(qn('w:val'), '0000FF')
                rPr.append(color)
                
                underline = OxmlElement('w:underline')
                underline.set(qn('w:val'), 'single')
                rPr.append(underline)
                
                new_run.append(rPr)
                
                # Add the text
                text_element = OxmlElement('w:t')
                text_element.text = text
                new_run.append(text_element)
                
                hyperlink.append(new_run)
                paragraph._p.append(hyperlink)

            # Add title
            title = doc.add_heading('The State of Artificial Intelligence in India: Current Landscape and Future Prospects', level=0)
            title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

            # Add author information
            author_para = doc.add_paragraph()
            author_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            author_para.add_run('Prepared by:RetryAi meant do not use functions nd all keep it stargight and simple focusing n getting indepth conetneEditSure, I'll create a straightforward Python script using python-docx that focuses primarily on generating a comprehensive report with in-depth content about AI in India, without excessive functions or formatting:
            pythonCopyfrom docx import Document
            from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

            # Create a new document
            doc = Document()

            # Add title
            title = doc.add_heading('The State of Artificial Intelligence in India: Current Landscape and Future Prospects', level=0)
            title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

            # Add author information
            author = doc.add_paragraph('Prepared by: AI Research Team')
            author.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            doc.add_paragraph('Date: March 2025')
            author.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

            # Table of Contents header
            doc.add_heading('Table of Contents', level=1)
            doc.add_paragraph('Executive Summary...................................3')
            doc.add_paragraph('1. Introduction......................................4')
            doc.add_paragraph('2. Current AI Market in India........................5')
            doc.add_paragraph('3. Government Initiatives and Policies..............8')
            doc.add_paragraph('4. AI Applications in Key Sectors..................12')
            doc.add_paragraph('5. AI Startups Ecosystem..........................20')
            doc.add_paragraph('6. Workforce and Skills Development...............24')
            doc.add_paragraph('7. Challenges and Opportunities...................29')
            doc.add_paragraph('8. Future Outlook (2025-2030)....................34')
            doc.add_paragraph('9. Case Studies..................................39')
            doc.add_paragraph('10. References...................................45')
            doc.add_page_break()

            # Executive Summary
            doc.add_heading('Executive Summary', level=1)
            summary = doc.add_paragraph()
            summary.add_run("India is rapidly emerging as a significant player in the global artificial intelligence (AI) landscape. With a projected market size of $7.8 billion by 2025 growing at a CAGR of over 40%, India's AI sector is transforming industries while addressing unique local challenges. The government's National AI Strategy and various initiatives are fostering innovation across sectors including healthcare, agriculture, education, and finance. ")
            summary.add_run("India ranks third globally in its AI startup ecosystem with over 70 native generative AI startups that have raised more than $440 million since 2019. The country possesses the third-largest AI talent pool globally, though faces a substantial skills gap with around 150,000 AI job openings against only 50,000 skilled professionals. ")
            summary.add_run("This report provides a comprehensive analysis of India's AI landscape, examining government policies, sectoral applications, startup ecosystem, workforce development, and future prospects through 2030. AI is expected to add US$967 billion to India's economy by 2035, representing a transformative opportunity that requires strategic planning to address challenges in infrastructure, data quality, and equitable AI adoption.")
            doc.add_page_break()

            # Introduction
            doc.add_heading('1. Introduction', level=1)
            intro = doc.add_paragraph()
            intro.add_run("Artificial Intelligence (AI) represents a transformative force in the global economy, with India positioning itself as a key player in this technological revolution. The integration of AI technologies across various sectors is reshaping India's economic and social landscape, driving innovation, efficiency, and growth. This report examines the current state of AI in India, analyzing its market dynamics, government initiatives, sectoral applications, challenges, and future prospects.")
            doc.add_paragraph()

            intro_2 = doc.add_paragraph()
            intro_2.add_run("The evolution of AI in India has transitioned through several stages, from conceptualization in the 1950s to widespread applications in the 2010s. This progression has been marked by significant advancements in computing hardware, algorithm development, and increased data availability. As India navigates this technological transformation, it faces both unique opportunities and challenges shaped by its diverse demographics, linguistic variety, and socioeconomic conditions.")
            doc.add_paragraph()

            intro_3 = doc.add_paragraph()
            intro_3.add_run("With the fourth industrial revolution underway, AI's strategic importance has been recognized by both public and private stakeholders in India. The government's emphasis on 'AI for All' reflects a commitment to harnessing AI's potential for inclusive growth and addressing societal needs. Meanwhile, India's robust IT sector, entrepreneurial ecosystem, and vast talent pool provide a strong foundation for AI innovation and adoption.")

            # Current AI Market in India
            doc.add_heading('2. Current AI Market in India', level=1)
            market = doc.add_paragraph()
            market.add_run("The AI market in India is experiencing remarkable growth, driven by increasing digital adoption, government initiatives, and private sector investments. According to Trade.gov, the AI market in India is projected to reach $8 billion by 2025, growing at a Compound Annual Growth Rate (CAGR) of over 40% from 2020 to 2025. This growth trajectory positions India as one of the fastest-growing AI markets globally.")
            doc.add_paragraph()

            market_size = doc.add_heading('2.1 Market Size and Growth Projections', level=2)
            market_size_para = doc.add_paragraph()
            market_size_para.add_run("The Indian AI market is undergoing substantial expansion across multiple dimensions:")
            doc.add_paragraph("• Current valuation: The AI market in India was valued at approximately $3.1 billion in 2020.")
            doc.add_paragraph("• Projected growth: Expected to reach $7.8-8 billion by 2025, representing a CAGR of 20.2-40% depending on the source.")
            doc.add_paragraph("• Future outlook: AI is expected to contribute US$957 billion (15% of GVA) to India's economy by 2035, potentially increasing annual growth rates by 1.3 percentage points.")
            doc.add_paragraph("• Sector-wise contribution: 60% of Gross Value Added (GVA) is expected to be driven by key sectors including Industrials & Automotive, Healthcare, Retail, and Consumer Packaged Goods (CPG).")
            doc.add_paragraph("• Investment trends: AI investments in India are growing at a CAGR of 30.8% and are projected to reach $881 million in 2023.")
            doc.add_paragraph()

            market_drivers = doc.add_heading('2.2 Key Market Drivers', level=2)
            driver_para = doc.add_paragraph()
            driver_para.add_run("Several factors are contributing to the rapid growth of AI adoption in India:")
            doc.add_paragraph("• Digital Infrastructure Growth: The Digital India initiative has significantly improved internet penetration and digital literacy, creating a conducive environment for AI adoption.")
            doc.add_paragraph("• Vast Talent Pool: India has the third largest AI talent pool globally, with 2.6 million STEM graduates annually, providing a strong human resource base for AI development.")
            doc.add_paragraph("• Government Support: Strategic initiatives like the National AI Strategy and substantial budget allocations (₹10,372 crore for the IndiaAI mission) are accelerating AI adoption.")
            doc.add_paragraph("• Startup Ecosystem: India ranks third among G20 countries for AI startups, with the ecosystem growing at 86% CAGR since 2011.")
            doc.add_paragraph("• Industry Adoption: 80% of Indian companies identify AI as a core strategic priority, with significant planned investments in 2025.")
            doc.add_paragraph("• Data Availability: India's large population generates vast amounts of data, providing the necessary fuel for AI systems development and training.")

            # Government Initiatives and Policies
            doc.add_heading('3. Government Initiatives and Policies', level=1)
            gov_para = doc.add_paragraph()
            gov_para.add_run("The Indian government has recognized AI's transformative potential and has implemented various initiatives and policies to position India as a global AI leader. These efforts aim to create an enabling ecosystem for AI innovation, adoption, and deployment across sectors.")
            doc.add_paragraph()

            national_strategy = doc.add_heading('3.1 National Strategy for Artificial Intelligence', level=2)
            strategy_para = doc.add_paragraph()
            strategy_para.add_run("In 2018, NITI Aayog developed India's national strategy for AI (#AIforAll) focusing on leveraging AI for inclusive growth and addressing societal needs. The strategy identifies five key sectors for AI intervention:")
            doc.add_paragraph("• Healthcare: Enhancing access and affordability of quality healthcare")
            doc.add_paragraph("• Agriculture: Improving farmer income, increasing farm productivity, and reducing wastage")
            doc.add_paragraph("• Education: Enhancing access and quality of education")
            doc.add_paragraph("• Smart Cities and Infrastructure: Addressing urban challenges through AI-driven solutions")
            doc.add_paragraph("• Smart Mobility and Transportation: Improving efficiency and safety in transportation systems")
            doc.add_paragraph()

            india_ai_mission = doc.add_heading('3.2 IndiaAI Mission', level=2)
            mission_para = doc.add_paragraph()
            mission_para.add_run("Launched with a budget of ₹10,372 crore, the IndiaAI Mission aims to:")
            doc.add_paragraph("• Democratize computing access through cloud computing infrastructure")
            doc.add_paragraph("• Improve data quality for AI applications")
            doc.add_paragraph("• Develop local AI capabilities and talent")
            doc.add_paragraph("• Attract AI expertise through various programs")
            doc.add_paragraph("• Foster industry collaboration and startup support")
            doc.add_paragraph("• Ensure socially impactful AI projects")
            doc.add_paragraph("• Promote ethical AI practices")
            doc.add_paragraph()

            budget_para = doc.add_paragraph()
            budget_para.add_run("The Union Budget 2025 allocated ₹2,000 crore for the IndiaAI mission, a substantial increase from ₹551 crore in 2024, demonstrating the government's growing commitment to AI development.")
            doc.add_paragraph()

            other_initiatives = doc.add_heading('3.3 Other Key Initiatives', level=2)
            initiatives_para = doc.add_paragraph()
            initiatives_para.add_run("The government has launched several complementary initiatives to support AI development:")
            doc.add_paragraph("• Responsible AI Draft (2021): Introduced voluntary guidelines focused on ethical AI practices, transparency, accountability, and fairness")
            doc.add_paragraph("• AI for All Initiative: A self-learning online program to democratize AI access")
            doc.add_paragraph("• Digital India Programme: Enhancing digital infrastructure and connectivity essential for AI deployment")
            doc.add_paragraph("• National AI Portal (INDIAai): Platform for sharing AI developments, resources, and opportunities")
            doc.add_paragraph("• AI Research, Innovation, and Startups Program (2022): Support for AI research and entrepreneurship")
            doc.add_paragraph("• Bhashini: Initiative for AI-driven language solutions addressing India's linguistic diversity")
            doc.add_paragraph("• AI Centers of Excellence: Plans to establish three AI Centres of Excellence to integrate AI into education and research")

            # AI Applications in Key Sectors
            doc.add_heading('4. AI Applications in Key Sectors', level=1)
            sectors_intro = doc.add_paragraph()
            sectors_intro.add_run("AI adoption is expanding across numerous sectors in India, transforming traditional practices and addressing unique challenges. The following sections explore AI applications in key sectors including healthcare, agriculture, education, finance, retail, and manufacturing.")

            # Healthcare section
            doc.add_heading('4.1 Healthcare', level=2)
            healthcare_intro = doc.add_paragraph()
            healthcare_intro.add_run("Healthcare represents one of the most promising areas for AI application in India, with potential to address challenges in accessibility, affordability, and quality of care. The Indian healthcare AI market is projected to reach $4.3 billion by 2024.")
            doc.add_paragraph()

            healthcare_apps = doc.add_paragraph()
            healthcare_apps.add_run("Key AI applications in Indian healthcare include:")
            doc.add_paragraph("• Medical Imaging and Diagnostics: Companies like Niramai use thermal imaging and AI for early breast cancer detection, achieving 96% accuracy. Google has developed AI models for diabetic retinopathy screening.")
            doc.add_paragraph("• Remote Monitoring and Telemedicine: AI-powered platforms like Practo overcome language barriers to improve healthcare access, particularly important for India's diverse population.")
            doc.add_paragraph("• Predictive Analytics: AI systems predict disease outbreaks and patient risks, enabling proactive intervention.")
            doc.add_paragraph("• Drug Discovery: AI accelerates pharmaceutical research by generating synthetic images and analyzing scientific literature.")
            doc.add_paragraph("• Personalized Treatment: Apollo Hospitals has launched India's first AI-Precision Oncology Center for personalized cancer treatment.")
            doc.add_paragraph()

            healthcare_case = doc.add_paragraph()
            healthcare_case.add_run("Case Study: Qure.ai, an Indian startup, has developed AI tools for chest X-ray analysis that can detect 15 common abnormalities with high accuracy. Their systems have been deployed in over 35 countries, helping address radiologist shortages and improving early detection rates.")

            # Agriculture section
            doc.add_heading('4.2 Agriculture', level=2)
            agri_intro = doc.add_paragraph()
            agri_intro.add_run("Agriculture employs over 50% of India's population and contributes approximately 18% to the GDP. AI applications in this sector are helping farmers increase productivity, manage resources efficiently, and adapt to climate change.")
            doc.add_paragraph()

            agri_apps = doc.add_paragraph()
            agri_apps.add_run("Major AI applications in Indian agriculture include:")
            doc.add_paragraph("• Precision Farming: AI tools analyze soil health, crop conditions, and environmental factors to optimize resource usage.")
            doc.add_paragraph("• Crop Monitoring and Disease Detection: AI-powered image recognition identifies plant diseases early, enabling timely intervention.")
            doc.add_paragraph("• Weather Prediction: AI systems provide accurate weather forecasts, helping farmers plan activities and mitigate climate risks.")
            doc.add_paragraph("• Supply Chain Optimization: AI improves post-harvest management, reducing wastage and enhancing market access.")
            doc.add_paragraph("• Crop Yield Prediction: Machine learning models predict harvest yields, helping in planning and market stabilization.")
            doc.add_paragraph()

            agri_impact = doc.add_paragraph()
            agri_impact.add_run("Impact: Studies show that AI implementation in Indian agriculture has led to a 30% increase in crop yields and 20% water savings. Startups like CropIn and Fasal have helped farmers increase productivity by 25-30% through AI-driven advisory services.")
            doc.add_paragraph()

            agri_case = doc.add_paragraph()
            agri_case.add_run("Case Study: An AI initiative in Telangana, funded by the Gates Foundation, has improved crop yields by 21% for thousands of farmers through climate-resilient practices and AI-driven agricultural advisories.")

            # Education section
            doc.add_heading('4.3 Education', level=2)
            edu_intro = doc.add_paragraph()
            edu_intro.add_run("India's education sector is undergoing significant transformation through AI integration, with the online education market expected to reach $10 billion by 2025. AI technologies are enhancing learning experiences, personalizing education, and improving administrative efficiency.")
            doc.add_paragraph()

            edu_apps = doc.add_paragraph()
            edu_apps.add_run("Key AI applications in Indian education include:")
            doc.add_paragraph("• Personalized Learning: Adaptive platforms like BYJU's and Embibe analyze student performance to customize content and learning paths.")
            doc.add_paragraph("• Automated Assessment: AI systems provide instant feedback and evaluation, reducing teacher workload by up to 20%.")
            doc.add_paragraph("• Intelligent Tutoring Systems: AI-powered tutors offer real-time guidance and support, enhancing student engagement.")
            doc.add_paragraph("• Content Creation: AI streamlines the development of educational materials, including lesson plans and assessments.")
            doc.add_paragraph("• Administrative Automation: AI handles routine administrative tasks, allowing educators to focus on teaching.")
            doc.add_paragraph("• Language Learning: AI tools support multilingual education, addressing India's linguistic diversity.")
            doc.add_paragraph()

            edu_challenges = doc.add_paragraph()
            edu_challenges.add_run("Challenges in AI adoption in education include:")
            doc.add_paragraph("• Digital divide in rural areas limiting access to AI tools")
            doc.add_paragraph("• High costs of AI solutions making them less accessible")
            doc.add_paragraph("• Need for teacher training to utilize AI effectively")
            doc.add_paragraph("• Data privacy concerns due to student data collection")
            doc.add_paragraph()

            edu_case = doc.add_paragraph()
            edu_case.add_run("Case Study: Gurushala, an AI-powered educational platform, developed an assessment generation tool that creates personalized tests from educational resources. The platform has onboarded 150,000 users and received $2.1 million in funding, demonstrating the growing demand for AI-driven educational solutions in India.")

            # Continue with more sections for Finance, Manufacturing, Retail, etc.

            # AI Startups Ecosystem
            doc.add_heading('5. AI Startups Ecosystem', level=1)
            startup_intro = doc.add_paragraph()
            startup_intro.add_run("India's AI startup ecosystem has experienced remarkable growth, establishing the country as a hub for AI innovation. With over 520 tech incubators and accelerators, India now ranks as the third-largest startup ecosystem globally.")
            doc.add_paragraph()

            startup_growth = doc.add_heading('5.1 Growth and Funding Landscape', level=2)
            growth_para = doc.add_paragraph()
            growth_para.add_run("The Indian AI startup landscape shows impressive momentum:")
            doc.add_paragraph("• Current Status: Over 70 native generative AI startups in India, with the number doubling since 2021")
            doc.add_paragraph("• Funding: AI startups raised over $440-475 million since 2019, with significant investment rounds in 2023-2024")
            doc.add_paragraph("• Geographical Distribution: Bengaluru leads as the primary AI innovation hub, followed by Hyderabad, Mumbai, Chennai, and the National Capital Region")
            doc.add_paragraph("• Sector Focus: One-third of AI startups focus on code and data applications, with 81% of GenAI products being sector-agnostic")
            doc.add_paragraph("• Development Approach: 79% of startups prefer in-house product development, indicating confidence in leveraging AI for competitive advantage")
            doc.add_paragraph()

            notable_startups = doc.add_heading('5.2 Notable AI Startups', level=2)
            startups_para = doc.add_paragraph()
            startups_para.add_run("Several Indian AI startups have gained significant traction and investment:")
            doc.add_paragraph("• Uniphore: Secured $400 million in Series E funding for its conversational AI solutions")
            doc.add_paragraph("• Gupshup: Raised $240 million in Series F for AI-powered messaging platforms")
            doc.add_paragraph("• Sarvam AI: Obtained $41 million in Series A funding for specialized AI development")
            doc.add_paragraph("• Krutrim: Raised $50 million in Series B and aims to develop India's first AI silicon chips by 2026")
            doc.add_paragraph("• Dave.AI: Creates virtual avatars for immersive sales experiences using AI technology")
            doc.add_paragraph("• Rephrase.ai: Offers video dubbing through realistic generative AI technology")
            doc.add_paragraph("• CropIn: Develops AI solutions for agricultural productivity enhancement")
            doc.add_paragraph("• Niramai: Utilizes AI for early breast cancer detection through thermal imaging")
            doc.add_paragraph()

            startup_challenges = doc.add_heading('5.3 Challenges and Opportunities', level=2)
            challenges_para = doc.add_paragraph()
            challenges_para.add_run("Despite impressive growth, Indian AI startups face several challenges:")
            doc.add_paragraph("• Funding Disparities: Major hubs like Bengaluru attract more investment compared to smaller cities")
            doc.add_paragraph("• Technical Limitations: Lack of startups developing foundation models due to high infrastructure costs")
            doc.add_paragraph("• Skill Shortages: Limited access to specialized AI talent")
            doc.add_paragraph("• Data Quality Issues: Challenges in accessing high-quality training data")
            doc.add_paragraph("• Regulatory Uncertainties: Evolving regulatory landscape creating compliance challenges")
            doc.add_paragraph()

            opportunities_para = doc.add_paragraph()
            opportunities_para.add_run("However, significant opportunities exist for Indian AI startups:")
            doc.add_paragraph("• Global Expansion: The cost advantage of building technology in India enables competitive global offerings")
            doc.add_paragraph("• Industry-Specific Solutions: Developing specialized AI applications for sectors like healthcare and agriculture")
            doc.add_paragraph("• Vernacular AI: Creating solutions that address India's linguistic diversity")
            doc.add_paragraph("• AI for Social Impact: Solving uniquely Indian challenges in education, healthcare, and agriculture")
            doc.add_paragraph("• Hybrid Business Models: Operating from India while targeting international markets for growth")

            # Workforce and Skills Development
            doc.add_heading('6. Workforce and Skills Development', level=1)
            workforce_intro = doc.add_paragraph()
            workforce_intro.add_run("The development of AI skills and talent is critical for India's AI ambitions. While India possesses a large pool of tech talent, significant skills gaps remain in specialized AI roles, creating both challenges and opportunities for workforce development.")
            doc.add_paragraph()

            talent_landscape = doc.add_heading('6.1 Current Talent Landscape', level=2)
            talent_para = doc.add_paragraph()
            talent_para.add_run("India's AI talent ecosystem presents a mixed picture:")
            doc.add_paragraph("• Talent Pool: India has the third largest AI talent pool globally, with over 5.43 million tech professionals")
            doc.add_paragraph("• Skills Gap: Approximately 150,000 AI job openings exist against only 50,000 skilled professionals")
            doc.add_paragraph("• Academic Standing: India ranks 10th globally with 386 PhD researchers in AI and 13th in AI conference presentations")
            doc.add_paragraph("• AI Readiness: Only 3% of enterprises are fully AI-ready, indicating substantial room for growth through training and investments")
            doc.add_paragraph("• Regional Distribution: AI talent is concentrated in major tech hubs, with emerging talent clusters in Tier 2 cities")
            doc.add_paragraph()

            skills_demand = doc.add_heading('6.2 In-Demand AI Skills', level=2)
            skills_para = doc.add_paragraph()
            skills_para.add_run("The top 15 in-demand skills for AI roles in India include:")
            doc.add_paragraph("1. Machine Learning (42%)")
            doc.add_paragraph("2. Python (40%)")
            doc.add_paragraph("3. Artificial Intelligence Core skills (36%)")
            doc.add_paragraph("4. Communication skills (23%)")
            doc.add_paragraph("5. Natural Language Processing (20%)")
            doc.add_paragraph("6. TensorFlow (19%)")
            doc.add_paragraph("7. Data Science (17%)")
            doc.add_paragraph("8. AWS (14%)")
            doc.add_paragraph("9. Deep Learning (14%)")
            doc.add_paragraph("10. Java (11%)")
            doc.add_paragraph("11. Azure (11%)")
            doc.add_paragraph("12. Image Processing (10%)")
            doc.add_paragraph("13. SQL (10%)")
            doc.add_paragraph("14. PyTorch (9%)")
            doc.add_paragraph("15. Agile (8%)")
            doc.add_paragraph()

            education_initiatives = doc.add_heading('6.3 Education and Training Initiatives', level=2)
            education_para = doc.add_paragraph()
            education_para.add_run("Various initiatives are addressing the AI skills gap in India:")
            doc.add_paragraph("• Government Programs: The National AI Skilling Framework aims to introduce AI courses from 6th grade onwards and train over 1 million new data science professionals annually")
            doc.add_paragraph("• Academic Institutions: IITs, IISc, and other institutions are launching specialized AI programs and research centers")
            doc.add_paragraph("• AI-Focused Universities: New institutions like Universal AI University, Jio Institute, and Mahindra University emphasize AI integration in their curricula")
            doc.add_paragraph("• Industry Partnerships: Companies like Infosys and Wipro are promoting upskilling in AI and data science")
            doc.add_paragraph("• Online Learning Platforms: NPTEL, CDAC, and Future Skills Prime offer various AI courses targeting different demographics")
            doc.add_paragraph()

            job_market = doc.add_heading('6.4 Job Market Trends', level=2)
            job_para = doc.add_paragraph()
            job_para.add_run("The AI job market in India shows significant growth:")
            doc.add_paragraph("• Job Creation: AI is expected to create 2.73 million new tech jobs in India by 2028")
            doc.add_paragraph("• Sector Growth: Key sectors adding AI jobs include retail (+6.96 million), manufacturing (+1.50 million), education (+0.84 million), and healthcare (+0.80 million)")
            doc.add_paragraph("• High-Demand Roles: Software application developers (+109,700), systems software developers (+48,800), and data engineers (+48,500) are among the fastest-growing positions")
            doc.add_paragraph("• Salary Trends: AI professionals command 40-80% higher compensation compared to traditional tech roles")
            doc.add_paragraph("• Geographical Trends: 48% increase in IT hiring in Tier 2 cities in Q3 2024, indicating geographic diversification of the AI workforce")
            doc.add_paragraph("• Future Outlook: 85% of Indian employers expect AI to create new job opportunities within one to five years")

            # Challenges and Opportunities
            doc.add_heading('7. Challenges and Opportunities', level=1)
            challenges_intro = doc.add_paragraph()
            challenges_intro.add_run("While India's AI ecosystem presents tremendous opportunities, it also faces significant challenges that must be addressed to realize the full potential of AI technologies.")

            # Challenges section
            doc.add_heading('7.1 Key Challenges', level=2)
            challenges_list = doc.add_paragraph()
            challenges_list.add_run("Major challenges in India's AI landscape include:")
            doc.add_paragraph("• Data Privacy and Security: Companies must navigate complex data protection regulations and ensure user privacy")
            doc.add_paragraph("• Ethical Concerns: Issues of bias, transparency, and accountability in AI systems need addressing")
            doc.add_paragraph("• Infrastructure Limitations: Limited internet access and digital infrastructure in some areas hamper AI adoption")
            doc.add_paragraph("• Skill Shortage: The gap between demand and supply of AI talent restricts growth and implementation")
            doc.add_paragraph("• High Development Costs: Significant investment required for building AI models, particularly foundation models")
            doc.add_paragraph("• Data Quality and Accessibility: Much of India's data remains unstructured with inadequate classification")
            doc.add_paragraph("• Regulatory Uncertainty: Evolving regulatory landscape creates compliance challenges")
            doc.add_paragraph("• Digital Divide: Inequality in access to technology could lead to uneven AI benefits across the population")
            doc.add_paragraph("• Complex Implementation: Integration challenges with existing systems and processes")
            doc.add_paragraph()

            sector_challenges = doc.add_paragraph()
            sector_challenges.add_run("Sector-specific challenges include:")
            doc.add_paragraph("• Healthcare: Concerns about patient data privacy and algorithm bias")
            doc.add_paragraph("• Agriculture: Limited digital literacy among farmers and connectivity issues in rural areas")
            doc.add_paragraph("• Education: Resistance to technology adoption and concerns about replacing human teachers")
            doc.add_paragraph("• Finance: Regulatory compliance and algorithmic transparency issues")

            # Opportunities section
            doc.add_heading('7.2 Strategic Opportunities', level=2)
            opportunities_list = doc.add_paragraph()
            opportunities_list.add_run("Despite these challenges, India is well-positioned to capitalize on numerous AI opportunities:")
            doc.add_paragraph("• Global AI Hub: Potential to emerge as a global center for AI talent and innovation")
            doc.add_paragraph("• Sector Transformation: Opportunities to revolutionize traditional sectors like agriculture and healthcare")
            doc.add_paragraph("• AI for Social Good: Addressing societal challenges through AI applications")
            doc.add_paragraph("• Linguistic Solutions: Leveraging AI to bridge language barriers across India's diverse population")
            doc.add_paragraph("• Localized AI Development: Building AI models specifically designed for Indian contexts and problems")
            doc.add_paragraph("• Cost Advantage: Developing AI solutions at lower costs compared to global competitors")
            doc.add_paragraph("• Digital Public Infrastructure: Building on successful digital foundations like UPI for AI deployment")
            doc.add_paragraph("• Export Opportunities: Creating AI solutions for international markets, particularly emerging economies")
            doc.add_paragraph()

            policy_recommendations = doc.add_heading('7.3 Policy Recommendations', level=2)
            policy_para = doc.add_paragraph()
            policy_para.add_run("To address challenges and maximize opportunities, the following policy approaches are recommended:")
            doc.add_paragraph("• Establish transparent governance structures for AI initiatives")
            doc.add_paragraph("• Promote multi-stakeholder collaborations involving academia, industry, and government")
            doc.add_paragraph("• Pursue public-private partnerships to finance and guide AI projects")
            doc.add_paragraph("• Develop comprehensive guidelines for ethical AI development and deployment")
            doc.add_paragraph("• Invest in AI research infrastructure and computational resources")
            doc.add_paragraph("• Enhance data sharing mechanisms while ensuring privacy and security")
            doc.add_paragraph("• Create inclusive AI literacy programs to bridge the digital divide")
            doc.add_paragraph("• Streamline regulatory processes to foster innovation while ensuring oversight")
            doc.add_paragraph("• Incentivize AI applications that address social and environmental challenges")

            # Future Outlook
            doc.add_heading('8. Future Outlook (2025-2030)', level=1)
            future_intro = doc.add_paragraph()
            future_intro.add_run("India's AI trajectory over the next five years will be shaped by evolving technologies, market dynamics, policy frameworks, and global developments. This section explores key trends and projections for AI in India from 2025 to 2030.")

            economic_impact = doc.add_heading('8.1 Economic Impact Projections', level=2)
            economic_para = doc.add_paragraph()
            economic_para.add_run("AI is expected to have a transformative economic impact in India:")
            doc.add_paragraph("• GDP Contribution: AI could add US$957-967 billion to India's economy by 2035, representing 15% of GVA")
            doc.add_paragraph("• Growth Enhancement: Potential to increase India's annual growth rate by 1.3 percentage points by 2035")
            doc.add_paragraph("• Productivity Gains: 2.61% productivity increase in the organized sector and 2.82% in the unorganized sector due to AI by 2030")
            doc.add_paragraph("• Job Transformation: 38 million jobs expected to be reshaped by AI by 2030")
            doc.add_paragraph("• Automation Impact: 24% of tasks across industries are fully automatable; an additional 42% can be enhanced by AI")
            doc.add_paragraph("• Industry Growth: AI-driven data analytics market expected to grow at a CAGR of 33.1% between 2022-2027")
            doc.add_paragraph()

            technological_trends = doc.add_heading('8.2 Technological Trends', level=2)
            tech_para = doc.add_paragraph()
            tech_para.add_run("Key technological trends expected to shape India's AI landscape include:")
            doc.add_paragraph("• Specialized Open-Source Models: Smaller, purpose-built models designed for local contexts will emerge as viable alternatives to large global models")
            doc.add_paragraph("• AI Agents in Workflows: Adoption of agentic AI for task execution and collaboration with human workers")
            doc.add_paragraph("• Edge Computing: Growth in real-time processing capabilities, reducing dependency on cloud infrastructure")
            doc.add_paragraph("• AI-IoT Integration: Convergence of AI with Internet of Things for enhanced data collection and analysis")
            doc.add_paragraph("• Explainable AI: Greater focus on transparency and interpretability in AI decision-making")
            doc.add_paragraph("• Quantum Computing: Potential breakthroughs in quantum computing enhancing AI capabilities")
            doc.add_paragraph("• Federated Learning: Privacy-preserving approaches to AI model training gaining prominence")
            doc.add_paragraph("• Indigenous LLMs: Development of large language models specifically trained on Indian languages and contexts")
            doc.add_paragraph()

            sectoral_futures = doc.add_heading('8.3 Sector-Specific Futures', level=2)
            sectoral_para = doc.add_paragraph()
            sectoral_para.add_run("By 2030, various sectors in India are expected to witness transformative AI integration:")
            doc.add_paragraph("• Healthcare: AI-driven predictive diagnostics becoming standard in healthcare facilities nationwide")
            doc.add_paragraph("• Agriculture: Widespread adoption of precision farming techniques, with AI managing irrigation, fertilization, and pest control")
            doc.add_paragraph("• Education: Personalized learning paths for every student, with AI tutors complementing human teachers")
            doc.add_paragraph("• Manufacturing: Smart factories with AI-driven quality control and predictive maintenance")
            doc.add_paragraph("• Financial Services: AI-based risk assessment and fraud detection becoming industry standard")
            doc.add_paragraph("• Public Services: AI-powered citizen services and policy planning tools enhancing governance")
            doc.add_paragraph("• Transportation: Advanced autonomous vehicle technologies and intelligent traffic management systems")

            # References  
            doc.add_heading('11. References', level=1)  
            references = [  
                "Author A. (Year). Title of the research paper. Journal Name, Volume(Issue), Page numbers. Retrieved from https://www.example.com/research-paper",  
                "Author B. (Year). Title of the book. Publisher. Available at https://www.example.com/book",  
                "Author C. (Year). Title of the article. Retrieved from https://www.example.com/article",  
                "Author D. (Year). Title of the conference paper. Conference Name, Location. https://www.example.com/conference-paper"  
            ]  
            for ref in references:  
                doc.add_paragraph(ref, style='List Number')  
            
            # Save the document  
            doc.save('report.docx')  #Always save the document as report.docx

        ```

        Use the research summaries below to generate the content:

        {content_with_sources}

        Return ONLY the Python code within the triple backticks format shown above. Do not include any other text or explanations.
        """
        
        print("Sending request to LLM...")
        completion = client.chat.completions.create(
            model="mini-deployment",
            messages=[
                {"role": "system", "content": "You are an expert Python developer who generates clean, well-structured code for creating Word documents."},
                {"role": "user", "content": REPORT_PROMPT},
            ]
        )
        
        # Update token trackers
        input_token_tracker += completion.usage.prompt_tokens
        output_token_tracker += completion.usage.completion_tokens
        print(f"Tokens used - Input: {completion.usage.prompt_tokens}, Output: {completion.usage.completion_tokens}")
        
        response = completion.choices[0].message.content
        print("Python code generated from LLM")
        print(response)
        
        # Extract the Python code between triple backticks
        print("Extracting Python code from response...")
        if "```python" in response and "```" in response:
            start_idx = response.find("```python") + len("```python")
            end_idx = response.rfind("```")
            python_code = response[start_idx:end_idx].strip()
            print("✅ Python code extracted successfully")
            print(f"Code length: {len(python_code)} characters")
        else:
            python_code = ""
            print("❌ Could not extract Python code from LLM response")
        
        print("=== Report Generation Complete ===\n")
        return "", python_code, input_token_tracker, output_token_tracker
    
    except Exception as e:
        print(f"❌ Error generating report from JSON file: {e}")
        print("=== Report Generation Failed ===\n")
        return "", "", input_token_tracker, output_token_tracker


def save_report_to_word(python_code, user_query):
    """Execute the Python code to save the report as a Word document"""
    print("\n=== Starting Word Document Save Process ===")
    try:
        # Create a directory for reports if it doesn't exist
        print("Creating reports directory if it doesn't exist...")
        os.makedirs("reports", exist_ok=True)
        
        # Create a timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"Generated timestamp: {timestamp}")
        
        # Create a safe filename from the user query
        safe_query = "".join(c if c.isalnum() else "_" for c in user_query)[:50]
        print(f"Sanitized query for filename: {safe_query}")
        
        # Create the filename
        filename = f"reports/{safe_query}_{timestamp}.docx"
        print(f"Final filename: {filename}")
        
        # Modify the Python code to use our filename
        print("Modifying Python code with custom filename...")
        modified_code = python_code.replace("'report.docx'", f"'{filename}'")
        
        # Execute the Python code
        print("Executing Python code to generate Word document...")
        exec(modified_code)
        
        print(f"✅ Report successfully saved to {filename}")
        print(f"File size: {os.path.getsize(filename)} bytes")
        print("=== Word Document Save Process Complete ===\n")
        return filename
    
    except Exception as e:
        print(f"❌ Error saving report to Word document: {e}")
        print("=== Word Document Save Process Failed ===\n")
        return None


def main():
    """Main function to run the deep research process"""
    print("\n=== Starting Deep Research Process ===")
    
    # Record start time
    start_time = datetime.now()
    print(f"Analysis started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize token trackers
    print("Initializing process...")
    input_token_tracker, output_token_tracker = initialize_trackers()
    
    # Get user query
    print("\nWaiting for user input...")
    user_query = input("Enter the topic on which you want to do research on: ")
    print(f"Received user query: {user_query}")
    
    # Initialize the Azure OpenAI client
    print("\nInitializing Azure OpenAI client...")
    azure_client = Client()
    client = azure_client.get_azure_client()
    print("Azure OpenAI client initialized successfully")
    
    # Get search query
    print("\nGenerating search query...")
    search_query, input_token_tracker, output_token_tracker = get_search_query(
        client, user_query, input_token_tracker, output_token_tracker
    )
    
    if search_query:
        # Update and display metrics
        print("\nUpdating metrics after search query generation...")
        update_and_display_metrics(input_token_tracker, output_token_tracker, "mini")
        
        # Get research queries
        print("\nGenerating research queries...")
        research_queries, input_token_tracker, output_token_tracker = get_research_queries(
            client, search_query, input_token_tracker, output_token_tracker
        )
        
        if research_queries:
            # Final update and display metrics
            print("\nUpdating metrics after research queries generation...")
            update_and_display_metrics(input_token_tracker, output_token_tracker, "mini")

    # Create a single dictionary to store all summaries
    print("\nInitializing summaries storage...")
    all_summaries = {}
    
    #Iterate over the research queries and get the links
    if research_queries and research_queries.queries:
        print(f"\nProcessing {len(research_queries.queries)} research queries...")
        for research_query in research_queries.queries:
            print(f"\n--- Processing research query: {research_query} ---")
            try:
                # Get links for the research query
                print("Fetching search links...")
                links = get_search_links(research_query)
                print(f"Found {len(links)} links")
                
                # Extract content from the links
                print("Extracting content from links...")
                url_content_dict = extract_content_from_urls(links)
                print(f"Successfully extracted content from {len(url_content_dict)} URLs")
                
                # Process each URL and its content
                for url, content in url_content_dict.items():
                    print(f"\nProcessing URL: {url}")
                    if content:
                        print(f"Content length: {len(content)} characters")
                        summary, input_token_tracker, output_token_tracker = summarize_content(
                            client, url, content, input_token_tracker, output_token_tracker
                        )
                        all_summaries[url] = summary
                        print(f"Summary preview: {summary[:150]}...")
                    else:
                        print(f"❌ No content extracted from {url}")
                
                # Update metrics after processing each research query
                print("\nUpdating metrics after processing research query...")
                update_and_display_metrics(input_token_tracker, output_token_tracker, "mini")
                
            except Exception as e:
                print(f"❌ Error processing research query '{research_query}': {e}")
                continue
    
    # Save all summaries to a single JSON file
    if all_summaries:
        print(f"\nSaving {len(all_summaries)} summaries to JSON...")
        json_file = save_summaries_to_json(all_summaries, user_query)
        print(f"Summaries saved to: {json_file}")
        
        # Generate comprehensive report from the JSON file
        print("\nGenerating comprehensive report...")
        report, python_code, input_token_tracker, output_token_tracker = generate_report(
            client, json_file, input_token_tracker, output_token_tracker
        )
        
        # Update metrics after generating the report
        print("\nUpdating metrics after report generation...")
        update_and_display_metrics(input_token_tracker, output_token_tracker, "mini")
        
        # Save the report as a Word document
        if python_code:
            print("\nSaving report to Word document...")
            word_file = save_report_to_word(python_code, user_query)
            if word_file:
                print(f"✅ Research process completed successfully!")
                print(f"Word document saved at: {word_file}")
            else:
                print("❌ Failed to save report as Word document")
        else:
            print("❌ No Python code generated to save the report")
    else:
        print("❌ No summaries generated to create report")

    # Record end time and calculate duration
    end_time = datetime.now()
    duration = end_time - start_time
    print(f"\nAnalysis ended at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total analysis duration: {duration}")
    
    print("\n=== Deep Research Process Complete ===")


if __name__ == "__main__":
    main()
