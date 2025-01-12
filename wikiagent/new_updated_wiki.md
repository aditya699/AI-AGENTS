# ABC Corporation Gamma Soap Sales Forecasting

## Project Description

This project assisted ABC Corporation in forecasting 2025 sales for their Gamma Soap product.


## Methodology

**Project Title:** ABC Corporation Gamma Soap Sales Forecasting

**Project Goal:** Forecast 2025 sales for ABC Corporation's Gamma Soap product.

**Phase 1: Data Acquisition and ETL**

* **Description:** Historical Gamma Soap sales data was extracted from a blob storage location. An ETL pipeline was developed using Azure Synapse Analytics to process this data.
* **Steps:**
    * Data Extraction from Blob Storage.
    * Data Transformation within Azure Synapse Analytics.
    * Data Loading into SQL Server.

**Phase 2: Model Development and Training**

* **Description:** A Random Forest model was developed using the prepared data in SQL Server.
* **Steps:**
    * Random Forest model training using data from SQL Server.

**Deliverables:**

* ETL Pipeline (Azure Synapse Analytics).
* SQL Server database containing transformed data.
* Trained Random Forest model for Gamma Soap sales forecasting.
* 2025 Sales Forecast.


## Tech Stack

Python, Azure Synapse, sklearn, pandas, SQL Server, Blob Storage


## Other Notes

Forecasted 2025 sales for ABC Corporation's Gamma Soap product using a Random Forest model (R2 = 90%). Data was sourced from blob storage, transformed via an ETL pipeline in Azure Synapse, and loaded into SQL Server for model training. Python, Azure Synapse, scikit-learn, and pandas were utilized. The resulting model provided insights to support improved business decision-making.


## Mermaid Chart (Architecture)

```mermaid
graph LR
A[Project: Forecast 2025 Gamma Soap Sales for ABC Corp] --> B[Historical Data in Blob Storage];
B --> C[ETL Pipeline Synapse];
C --> D[Data Transformation Pandas];
D --> E[Data in SQL Server];
E --> F[Random Forest Model sklearn];
F --> G[Sales Forecast];
G --> A;
subgraph "Tech Stack"
C[Synapse]
F[Python]
D[Pandas]
E[SQL Server]
F[sklearn]
end
style A fill:#f9f,stroke:#333,stroke-width:2px
style G fill:#ccf,stroke:#333,stroke-width:2px
note right of G
R2=90%
Created a story to help the business take great decisions
end
```

## Urls

No URL was used in this project.


## Learning

1. Thoroughly tested ETL pipelines.
2. Focused on creating robust test cases using pytest.
3. Prioritized the selection of interpretable models.