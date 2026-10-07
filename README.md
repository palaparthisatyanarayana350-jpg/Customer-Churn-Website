# ChurnGuard – Customer Churn Prediction

ChurnGuard is a web-based customer churn prediction system that uses **TabPFN** to estimate the probability of customer churn from selected customer attributes.

The project combines machine learning, explainability, and a simple web interface to provide an easy-to-use churn prediction experience.

## Project Overview

Customer churn prediction helps organizations identify customers who may be likely to leave a service. ChurnGuard provides a prediction interface where users can enter customer information and receive:

- Churn probability
- Low, Medium, or High churn risk
- What-if sensitivity analysis
- Feature-based insights

The system uses the **IBM Telco Customer Churn dataset** for model development.

## Objectives

- Develop a customer churn prediction system using TabPFN.
- Identify important factors associated with churn prediction.
- Provide probability-based churn risk classification.
- Add explainability through what-if analysis.
- Build a user-friendly web application.
- Deploy the machine learning backend and frontend online.

## Machine Learning Model

The project uses **TabPFN (Tabular Prior-Data Fitted Networks)** for tabular classification.

The final prediction model uses six features:

1. Tenure
2. Monthly Charges
3. Contract
4. Internet Service
5. Payment Method
6. Tech Support

The model predicts whether a customer is likely to churn and produces a churn probability.

## Dataset

The project uses the **IBM Telco Customer Churn dataset**.

Dataset characteristics:

- 7,043 customer records
- 21 original columns
- Target variable: `Churn`
- Churn = Yes / No

### Preprocessing

The dataset was processed before model development:

- `TotalCharges` was converted from text to numeric format.
- Missing `TotalCharges` values were handled.
- Customer ID was excluded from modeling.
- The final model uses six selected features.
- Categorical features are handled by the TabPFN client.

## Model Evaluation

The model was evaluated using a stratified 80/20 train-test split with `random_state = 42`.

| Metric | Score |
|---|---:|
| Accuracy | 80.34% |
| Precision | 66.22% |
| Recall | 52.94% |
| F1 Score | 58.84% |
| ROC-AUC | 84.63% |

The evaluation results are based on the holdout test set.

## Explainability

ChurnGuard includes a what-if sensitivity analysis.

For selected categorical features, the system changes the feature value while keeping the other customer inputs unchanged and obtains the resulting churn probability.

This allows users to compare how different possible customer profiles affect the model's prediction.

### Global Feature Importance

Permutation importance was used to estimate the relative importance of the six selected features.

| Feature | Permutation Importance |
|---|---:|
| Contract | 0.0932 |
| Tenure | 0.0761 |
| Internet Service | 0.0274 |
| Tech Support | 0.0130 |
| Monthly Charges | 0.0108 |
| Payment Method | 0.0045 |

These values represent model-based feature importance and should not be interpreted as causal effects.

## Web Application

The project provides a single-page web application with the following sections:

- Home
- Customer Prediction
- Prediction Result
- What-if Analysis
- Dataset Insights
- Explainability
- About

The prediction interface accepts customer information and communicates with the deployed TabPFN backend through an API.

## Technologies Used

### Machine Learning

- Python
- Pandas
- Scikit-learn
- TabPFN

### Backend

- Flask
- Flask-CORS
- Gunicorn

### Frontend

- HTML
- CSS
- JavaScript

### Deployment and Version Control

- Git
- GitHub
- Render

## Project Structure

```text
Customer-Churn-Website/
│
├── index.html
├── script.js
├── style.css
│
└── backend/
    ├── app.py
    ├── evaluate_model.py
    ├── explainability.py
    ├── requirements.txt
    └── WA_Fn-UseC_-Telco-Customer-Churn.csv
