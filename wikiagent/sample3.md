# Conversational Chatbot for Internal Documentation Navigation

## Project Description

This project involves developing a conversational chatbot to assist the internal team in navigating company documentation.

## Methodology

Development of a conversational chatbot for internal team documentation navigation.

**Phase 1: Development**

* **Step 1: Chatbot Creation**
    * Description: A conversational chatbot was developed to interact with users and retrieve information from company documentation.
    * Tools/Technologies: Unspecified chatbot development framework.

* **Step 2: RAG Architecture Implementation**
    * Description: A Retrieval Augmented Generation (RAG) architecture was implemented to enable the chatbot to access and process information from the company documentation.
    * Details: The RAG architecture likely involved retrieving relevant documents based on user queries, processing these documents, and generating responses using the retrieved information.

* **Step 3: Vector Database Integration**
    * Description: A FAISS in-memory vector database was used to store and efficiently search through embeddings of the company documentation.
    * Details: FAISS was employed for fast similarity search to retrieve the most relevant documents for a given user query.

**Phase 2: Deployment**

* **Step 1: Azure Web Deployment**
    * Description: The developed chatbot was deployed to Azure Web Services for accessibility by the internal team.
    * Details: This involved configuring the chatbot application to run on Azure's infrastructure.


## Tech Stack

* **Architecture:** RAG
* **Vector Database:** FAISS (in-memory)
* **LLM:** Gemini (Python)
* **Chatbot Framework:** Streamlit
* **Deployment:** Azure Web App
* **CI/CD:** Azure DevOps
* **Storage:** Azure Blob Storage
* **Programming Language:** Python


## Other Notes

**Retrieval Stage Optimization:** The project focused on creating a chatbot, but the notes emphasize a need for more thorough testing of the retrieval step before deployment. This suggests potential issues with accuracy, speed, or efficiency in how the chatbot accesses and processes information from the company documentation stored in Azure Blob storage. Further investigation into the FAISS vector database implementation is recommended, including analysis of indexing strategies, query optimization, and potential bottlenecks. Consider A/B testing different retrieval methods or parameters to identify areas for improvement.

**Safety and Security Considerations:** Before deployment, a comprehensive safety review is crucial. This should include testing for vulnerabilities that could lead to the chatbot revealing sensitive company information or producing harmful or inappropriate responses. Specific attention should be paid to the handling of user inputs and the potential for adversarial attacks.

**Azure DevOps Integration:** The project utilizes Azure DevOps for code management. Ensure that the CI/CD pipeline includes robust testing stages to catch errors before deployment to the Azure Web App. This should incorporate automated tests for both the chatbot functionality and the retrieval process.

**Streamlit Deployment:** The use of Streamlit for the chatbot interface should be reviewed for scalability and performance, especially considering the potential increase in usage by the internal team.


## Mermaid Chart (Architecture)

```mermaid
graph LR
A[Project: Conversational Chatbot for Internal Documentation] --> B{Develop Chatbot};
B --> C[Python, Gemini (LLM), Streamlit];
C --> D(FAISS In-Memory Vector DB);
D --> E[Retrieval Step];
E --> F{Deployment to Azure Web App};
F --> G[Azure DevOps, Blob Storage];
G --> H[Testing & Safety Checks];
H --> I[Azure Web App Deployment];

subgraph "Focus: Retrieval"
    E
end

style E fill:#f9f,stroke:#333,stroke-width:2px
```

## URLs

No URL was used in this project.

## Learning

Choosing the right chunking strategy is important for effective conversational chatbot development. Chunk overlap is also a critical consideration.