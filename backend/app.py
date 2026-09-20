from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from tabpfn_client import TabPFNClassifier

app = Flask(__name__)
CORS(app)


# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)


# ============================================================
# PREPROCESSING
# ============================================================

df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
).fillna(0)


# ============================================================
# FINAL FEATURES USED BY THE MODEL
# ============================================================

features = [
    "tenure",
    "MonthlyCharges",
    "Contract",
    "InternetService",
    "PaymentMethod",
    "TechSupport"
]

X = df[features].copy()

y = df["Churn"].map({
    "No": 0,
    "Yes": 1
})


print("\nFeatures used by TabPFN:")

for feature in features:
    print("-", feature)


# ============================================================
# TRAIN TABPFN
# ============================================================

print("\nLoading TabPFN model...")

model = TabPFNClassifier()

print("Training TabPFN on final six features...")

model.fit(X, y)

print("TabPFN training completed!")


# ============================================================
# CREATE CUSTOMER INPUT
# ============================================================

def create_customer(data):

    customer = {
        "tenure": float(data["tenure"]),

        "MonthlyCharges": float(
            data["monthlyCharges"]
        ),

        "Contract": data["contract"],

        "InternetService": data["internet"],

        "PaymentMethod": data["payment"],

        "TechSupport": data["support"]
    }

    return customer


# ============================================================
# RISK CLASSIFICATION
# ============================================================

def get_risk(probability):

    if probability >= 0.60:
        return "High Churn Risk"

    elif probability >= 0.35:
        return "Medium Churn Risk"

    else:
        return "Low Churn Risk"


# ============================================================
# WHAT-IF EXPLAINABILITY
# ============================================================

def generate_explanations(customer):

    explanations = []

    base_df = pd.DataFrame([customer])

    base_probability = model.predict_proba(
        base_df
    )[0][1] * 100


    # --------------------------------------------------------
    # Contract
    # --------------------------------------------------------

    contract_values = [
        "Month-to-month",
        "One year",
        "Two year"
    ]

    for value in contract_values:

        test_customer = customer.copy()

        test_customer["Contract"] = value

        test_df = pd.DataFrame([test_customer])

        probability = model.predict_proba(
            test_df
        )[0][1] * 100

        explanations.append({
            "feature": "Contract",
            "value": value,
            "probability": round(probability, 2)
        })


    # --------------------------------------------------------
    # Internet Service
    # --------------------------------------------------------

    internet_values = [
        "DSL",
        "Fiber optic",
        "No"
    ]

    for value in internet_values:

        test_customer = customer.copy()

        test_customer["InternetService"] = value

        test_df = pd.DataFrame([test_customer])

        probability = model.predict_proba(
            test_df
        )[0][1] * 100

        explanations.append({
            "feature": "Internet Service",
            "value": value,
            "probability": round(probability, 2)
        })


    # --------------------------------------------------------
    # Payment Method
    # --------------------------------------------------------

    payment_values = [
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    ]

    for value in payment_values:

        test_customer = customer.copy()

        test_customer["PaymentMethod"] = value

        test_df = pd.DataFrame([test_customer])

        probability = model.predict_proba(
            test_df
        )[0][1] * 100

        explanations.append({
            "feature": "Payment Method",
            "value": value,
            "probability": round(probability, 2)
        })


    # --------------------------------------------------------
    # Tech Support
    # --------------------------------------------------------

    support_values = [
        "Yes",
        "No"
    ]

    for value in support_values:

        test_customer = customer.copy()

        test_customer["TechSupport"] = value

        test_df = pd.DataFrame([test_customer])

        probability = model.predict_proba(
            test_df
        )[0][1] * 100

        explanations.append({
            "feature": "Tech Support",
            "value": value,
            "probability": round(probability, 2)
        })


    return explanations


# ============================================================
# PREDICTION API
# ============================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.json

        # ----------------------------------------------------
        # Validate input
        # ----------------------------------------------------

        required_fields = [
            "tenure",
            "monthlyCharges",
            "contract",
            "internet",
            "payment",
            "support"
        ]

        for field in required_fields:

            if field not in data:
                return jsonify({
                    "error": f"Missing field: {field}"
                }), 400


        # ----------------------------------------------------
        # Create customer
        # ----------------------------------------------------

        customer = create_customer(data)

        customer_df = pd.DataFrame(
            [customer],
            columns=features
        )


        # ----------------------------------------------------
        # Prediction
        # ----------------------------------------------------

        probability = model.predict_proba(
            customer_df
        )[0][1]

        probability_percent = round(
            probability * 100,
            2
        )


        # ----------------------------------------------------
        # Risk
        # ----------------------------------------------------

        risk = get_risk(probability)


        # ----------------------------------------------------
        # What-if explainability
        # ----------------------------------------------------

        explanations = generate_explanations(
            customer
        )


        # ----------------------------------------------------
        # Response
        # ----------------------------------------------------

        return jsonify({

            "prediction": risk,

            "probability": probability_percent,

            "explanations": explanations

        })


    except Exception as error:

        print("Prediction error:", error)

        return jsonify({
            "error": str(error)
        }), 500


# ============================================================
# HOME ROUTE
# ============================================================

@app.route("/")
def home():

    return "ChurnGuard backend is running with TabPFN!"


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    print("\n======================================")
    print("       CHURNGUARD BACKEND")
    print("======================================")
    print("Model: TabPFN")
    print("Features: 6")
    print("Server: http://127.0.0.1:5000")
    print("======================================\n")

    app.run(
        debug=False,
        port=5000
    )