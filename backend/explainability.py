import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.inspection import permutation_importance

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
# 3. FINAL MODEL FEATURES
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


print("\nFeatures used for explainability:")

for feature in features:
    print("-", feature)


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

print("\nTraining rows:", len(X_train))
print("Testing rows :", len(X_test))


# ==========================================
# 5. TRAIN TABPFN
# ==========================================

print("\nTraining TabPFN...")

model = TabPFNClassifier()

model.fit(X_train, y_train)

print("Training completed!")


# ==========================================
# 6. PERMUTATION IMPORTANCE
# ==========================================

print("\nCalculating feature importance...")

result = permutation_importance(
    model,
    X_test,
    y_test,
    n_repeats=5,
    random_state=42,
    scoring="roc_auc"
)


# ==========================================
# 7. CREATE IMPORTANCE TABLE
# ==========================================

importance_df = pd.DataFrame({
    "Feature": X_test.columns,
    "Importance": result.importances_mean
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)


# ==========================================
# 8. DISPLAY RESULTS
# ==========================================

print("\n==========================================")
print("TABPFN FEATURE IMPORTANCE")
print("==========================================")

for _, row in importance_df.iterrows():

    print(
        f"{row['Feature']:<20} "
        f"{row['Importance']:.4f}"
    )


# ==========================================
# 9. TOP FEATURES
# ==========================================

print("\n==========================================")
print("TOP FEATURES")
print("==========================================")

for _, row in importance_df.head(6).iterrows():

    print(
        f"{row['Feature']:<20} "
        f"{row['Importance']:.4f}"
    )