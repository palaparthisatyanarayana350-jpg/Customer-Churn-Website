# ChurnGuard – Customer Churn Prediction

ChurnGuard is a machine learning-based web application that predicts the probability of customer churn using the TabPFN classification model.

The project uses the IBM Telco Customer Churn dataset and provides an interactive interface where users can enter customer information and receive a churn probability and risk category.

---

## Project Overview

Customer churn is an important problem for businesses because losing existing customers can affect revenue and long-term growth.

ChurnGuard aims to provide a simple prediction system that:

- Predicts the probability of customer churn
- Classifies customers into Low, Medium, or High Churn Risk
- Provides what-if sensitivity analysis
- Presents important model insights through a web interface

---

## Objectives

- Develop a customer churn prediction system using TabPFN.
- Identify customer attributes associated with churn prediction.
- Provide probability-based churn risk classification.
- Build an easy-to-use web interface for prediction.
- Provide sensitivity analysis for selected customer attributes.
- Evaluate the performance of the developed model.

---

## Dataset

The project uses the **IBM Telco Customer Churn Dataset**.

### Dataset Details

- Total records: 7,043
- Total original features: 20
- Target variable: `Churn`
- Churn classes:
  - No
  - Yes

The original dataset contains customer demographic, service, contract, payment, and billing information.

For the deployed prediction system, six features are used:

- Tenure
- Monthly Charges
- Contract
- Internet Service
- Payment Method
- Tech Support

---

## Data Preprocessing

The following preprocessing steps were performed:

- Converted `TotalCharges` from text to numeric format.
- Identified 11 missing `TotalCharges` values.
- Replaced these missing values with 0 because they corresponded to customers with zero tenure.
- Checked for duplicate records.
- Verified customer ID uniqueness.
- Converted the target variable:
  - `No → 0`
  - `Yes → 1`

---

## Machine Learning Model

### TabPFN

The project uses **TabPFN (Tabular Prior-Data Fitted Network)** for binary classification.

TabPFN is designed for tabular machine learning problems and can perform classification without requiring a traditional long training process for every new dataset.

The final deployment model uses:

1. Tenure
2. Monthly Charges
3. Contract
4. Internet Service
5. Payment Method
6. Tech Support

---

## Model Evaluation

The model was evaluated using an 80/20 stratified train-test split with a fixed random state of 42.

### Performance

| Metric | Score |
|---|---:|
| Accuracy | 80.34% |
| Precision | 66.22% |
| Recall | 52.94% |
| F1-Score | 58.84% |
| ROC-AUC | 84.63% |

### Confusion Matrix

| | Predicted No Churn | Predicted Churn |
|---|---:|---:|
| Actual No Churn | 934 | 101 |
| Actual Churn | 176 | 198 |

The ROC-AUC score indicates good ability of the model to distinguish between churn and non-churn customers.

---

## Explainability and Sensitivity Analysis

ChurnGuard provides a what-if sensitivity analysis.

The system changes one selected feature at a time while keeping the other customer attributes unchanged and observes the resulting change in predicted churn probability.

The evaluated feature importance using permutation importance was:

| Feature | Importance |
|---|---:|
| Contract | 0.0932 |
| Tenure | 0.0761 |
| Internet Service | 0.0274 |
| Tech Support | 0.0130 |
| Monthly Charges | 0.0108 |
| Payment Method | 0.0045 |

These values represent model-based feature importance and should not be interpreted as causal effects.

---

## Web Application

ChurnGuard provides a single-page web interface containing:

- Home section
- Customer prediction form
- Churn probability
- Risk classification
- Risk meter
- What-if sensitivity analysis
- Dataset insights
- Model information
- Project information

### Risk Classification

| Churn Probability | Risk Level |
|---|---|
| Below 35% | Low Risk |
| 35% – 59.99% | Medium Risk |
| 60% and above | High Risk |

---

## Technology Stack

### Machine Learning
- Python
- Pandas
- Scikit-learn
- TabPFN

### Backend
- Flask
- Flask-CORS
- Python

### Frontend
- HTML
- CSS
- JavaScript

### Deployment and Version Control
- Git
- GitHub
- Render

---

## Project Structure

```text
Customer-Churn-Website/
│
├── backend/
│   ├── app.py
│   ├── evaluate_model.py
│   ├── explainability.py
│   ├── requirements.txt
│   └── WA_Fn-UseC_-Telco-Customer-Churn.csv
│
├── index.html
├── style.css
├── script.js
└── README.md
