import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

from tabpfn_client import TabPFNClassifier


# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")

print("Dataset loaded successfully!")
print("Original shape:", df.shape)


# ==========================================
# 2. BASIC PREPROCESSING
# ==========================================

df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
).fillna(0)


# ==========================================
# 3. SELECT FINAL MODEL FEATURES
# ==========================================

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


print("\nFinal model features:")
for feature in features:
    print("-", feature)

print("\nX shape:", X.shape)
print("y shape:", y.shape)


# ==========================================
# 4. TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\n==========================================")
print("TRAIN / TEST SPLIT")
print("==========================================")

print("Training rows:", len(X_train))
print("Testing rows :", len(X_test))


# ==========================================
# 5. TRAIN TABPFN
# ==========================================

print("\n==========================================")
print("TRAINING TABPFN")
print("==========================================")

model = TabPFNClassifier()

model.fit(X_train, y_train)

print("TabPFN training completed!")


# ==========================================
# 6. PREDICTIONS
# ==========================================

print("\nMaking predictions...")

y_pred = model.predict(X_test)

y_prob = model.predict_proba(X_test)[:, 1]


# ==========================================
# 7. PERFORMANCE METRICS
# ==========================================

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

roc_auc = roc_auc_score(
    y_test,
    y_prob
)


# ==========================================
# 8. DISPLAY RESULTS
# ==========================================

print("\n==========================================")
print("FINAL TABPFN PERFORMANCE")
print("==========================================")

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")
print(f"ROC-AUC  : {roc_auc:.4f}")


# ==========================================
# 9. CLASSIFICATION REPORT
# ==========================================

print("\n==========================================")
print("CLASSIFICATION REPORT")
print("==========================================")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=["No Churn", "Churn"],
        zero_division=0
    )
)


# ==========================================
# 10. CONFUSION MATRIX
# ==========================================

print("\n==========================================")
print("CONFUSION MATRIX")
print("==========================================")

cm = confusion_matrix(y_test, y_pred)

print(cm)

print("\nMatrix format:")
print("[[True Negative, False Positive]")
print(" [False Negative, True Positive]]")