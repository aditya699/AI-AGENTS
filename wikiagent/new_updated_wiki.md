# ABC Corporation Gamma Soap Sales Forecasting for 2025

## Project Description

This project assisted ABC Corporation in forecasting 2025 sales for their Gamma Soap product.


## Methodology

**Project Goal:** Forecast 2025 sales for ABC Corporation's Gamma Soap product.

**Data Acquisition:**

* **Source:** Historical Gamma Soap sales data stored in blob storage.
* **Process:** Data was extracted from blob storage.

**Data Transformation:**

* **Platform:** Azure Synapse Analytics ETL pipeline.
* **Steps:**
    * Data was transformed within the Azure Synapse Analytics ETL pipeline.
    * Transformed data was loaded into SQL Server.

**Model Development:**

* **Algorithm:** Random Forest Regression.
* **Implementation:** A Random Forest model was created using the transformed data in SQL Server.

**Forecasting:**

* **Method:** The developed Random Forest model was used to forecast 2025 sales.


## Tech Stack

Python, Azure Synapse, SQL Server, scikit-learn (sklearn), pandas


## Other Notes

Project assisted ABC Corporation in forecasting 2025 sales for their Gamma Soap product.  ETL pipeline developed on Azure Synapse, moving historical data from Blob storage, transforming it, and loading it into SQL Server.  A Random Forest model (using scikit-learn and pandas in Python) was created.  The resulting model provided a strong forecast (R-squared = 90%), enabling data-driven business decisions.


## Mermaid Chart (Architecture)

```mermaid
graph LR
A[Project: Forecast 2025 Gamma Soap Sales for ABC Corp] --> B[Historical Data in Blob Storage];
B --> C[ETL Pipeline (Synapse)];
C --> D[Data in SQL Server];
D --> E[Random Forest Model];
E --> F[Model Training (Python, sklearn)];
F --> G[Sales Forecast];
G --> A;
subgraph "Tech Stack"
    C[Azure Synapse]
    F[Python, sklearn, pandas]
end
subgraph "Metrics"
    G[R2=90%]
end
```

## URLs

No URL was used in this project.


## Learning

1. Thoroughly tested ETL pipelines.
2. Focused on creating robust test cases using pytest.
3. Prioritized the selection of interpretable models.