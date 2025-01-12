# Diabetes Prediction Model for AXY Corporation

## Project Description

Developed a machine learning model for AXY Corporation, a healthtech firm, to predict the likelihood of an individual developing diabetes.

## Methodology

**Project Title:** Diabetes Prediction Model for AXY Corporation

**Phase 1: Model Development**

1. A neural network (ANN) model was designed for predicting the likelihood of an individual developing diabetes.

**Phase 2: Infrastructure Setup**

2. An Azure Virtual Machine (VM) was provisioned to host the model and its dependencies.

**Phase 3: Model Training and Deployment**

3. The ANN model was trained using unspecified data. Details on data preprocessing, feature engineering, and model evaluation metrics are not provided.
4. The trained ANN model was deployed on the Azure VM using FastAPI, creating a RESTful API for internal use within AXY Corporation.

**Phase 4: Deployment and Access**

5. The FastAPI application allows AXY Corporation employees to access and utilize the diabetes prediction model.


## Tech Stack

| Technology | Description |
|---|---|
| PyTorch | Used for building the neural network model. |
| Azure VM | Used for training and deploying the model. |
| FastAPI | Used for creating the API for accessing the model. |
| Pandas | Used for data manipulation and preprocessing. |


## Other Notes

Developed a diabetes prediction model using a PyTorch neural network (ANN). The model was trained and deployed on an Azure VM using FastAPI for internal AXY Corporation use. Data preprocessing was handled with Pandas. Client communication was maintained throughout the development process.

## Mermaid Chart (Architecture)

```mermaid
graph LR
A[Project: Diabetes Prediction Model for AXY] --> B[Data Collection/Preprocessing];
B --> C[Neural Network (ANN) Design];
C --> D[Neural Network Training with PyTorch];
D --> E[Deployment on Azure VM via FastAPI];
E --> F[Model Usage by AXY Personnel];
F --> G[Client Communication];
G --> A;
subgraph "Tech Stack"
    D[PyTorch]
    E[Azure VM]
    E[FastAPI]
    B[Pandas]
end
```

## URLs

No URL was used in this project.

## Learning

Developed a machine learning model for AXY Corporation, a healthtech firm, to predict the likelihood of an individual developing diabetes. Key learnings included the effectiveness of Artificial Neural Networks (ANNs) when sufficient data is available. Data skewness was identified as a crucial factor impacting model performance.