"""
Module 5: Delay Risk Prediction Model
Delivery Performance, Delay Risk, and Logistics Efficiency Analysis
Input:  featured_logistics.csv (output of Module 2)
Output: model_summary.txt + feature_importance.csv + confusion_matrix.png + roc_curve.png

IMPORTANT: We predict Late_delivery_risk using only features that would be
KNOWN AT ORDER TIME (before the shipment actually happens). Columns like
"Delay Days", "Days for shipping (real)", "On Time Flag", "OTIF Flag",
"Perfect Order Flag", "Delivery Status" are all outcomes of the delivery
itself -> using them would be data leakage (the model would "cheat").
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report, roc_curve
)

IN_PATH = "featured_logistics.csv"
df = pd.read_csv(IN_PATH)

summary_lines = []
def log(msg):
    print(msg)
    summary_lines.append(str(msg))

log(f"Dataset shape: {df.shape}")

# ------------------------------------------------------------------
# 1. Feature selection (order-time only -> avoid leakage)
# ------------------------------------------------------------------
target = "Late_delivery_risk"

categorical_features = [
    "Shipping Mode", "Market", "Order Region", "Order Country",
    "Category Name", "Customer Segment", "Department Name",
]
numeric_features = [
    "Days for shipment (scheduled)",  # known at order time (promised lead time)
    "Order Item Quantity",
    "Order Item Discount Rate",
    "Order Item Product Price",
    "Sales",
    "Order Item Profit Ratio",
]

model_df = df[categorical_features + numeric_features + [target]].copy()
model_df = model_df.dropna()

# Encode categoricals
encoders = {}
for col in categorical_features:
    le = LabelEncoder()
    model_df[col] = le.fit_transform(model_df[col].astype(str))
    encoders[col] = le

X = model_df[categorical_features + numeric_features]
y = model_df[target]

log(f"\nFeatures used: {list(X.columns)}")
log(f"Target distribution:\n{y.value_counts(normalize=True).to_string()}")

# ------------------------------------------------------------------
# 2. Train/test split
# ------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
log(f"\nTrain shape: {X_train.shape}  Test shape: {X_test.shape}")

# ------------------------------------------------------------------
# 3. Train Random Forest
# ------------------------------------------------------------------
model = RandomForestClassifier(
    n_estimators=200, max_depth=12, random_state=42, n_jobs=-1, class_weight="balanced"
)
model.fit(X_train, y_train)

# ------------------------------------------------------------------
# 4. Evaluate
# ------------------------------------------------------------------
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_proba)

log(f"\n--- Model Performance (Random Forest) ---")
log(f"Accuracy:  {acc:.3f}")
log(f"Precision: {prec:.3f}")
log(f"Recall:    {rec:.3f}")
log(f"F1 Score:  {f1:.3f}")
log(f"ROC-AUC:   {auc:.3f}")
log("\nClassification Report:\n" + classification_report(y_test, y_pred))

# ------------------------------------------------------------------
# 5. Confusion matrix
# ------------------------------------------------------------------
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["On Time", "Late"], yticklabels=["On Time", "Late"])
plt.title("Confusion Matrix - Late Delivery Risk")
plt.ylabel("Actual")
plt.xlabel("Predicted")
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.close()

# ------------------------------------------------------------------
# 6. ROC curve
# ------------------------------------------------------------------
fpr, tpr, _ = roc_curve(y_test, y_proba)
plt.figure(figsize=(6, 5))
plt.plot(fpr, tpr, label=f"ROC-AUC = {auc:.3f}")
plt.plot([0, 1], [0, 1], "k--", alpha=0.5)
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve - Late Delivery Risk Model")
plt.legend()
plt.tight_layout()
plt.savefig("roc_curve.png")
plt.close()

# ------------------------------------------------------------------
# 7. Feature importance
# ------------------------------------------------------------------
importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
}).sort_values("Importance", ascending=False)

log("\nFeature Importance:\n" + importance.to_string(index=False))
importance.to_csv("feature_importance.csv", index=False)

plt.figure(figsize=(8, 6))
sns.barplot(data=importance, x="Importance", y="Feature", color="teal")
plt.title("Feature Importance - Late Delivery Risk Model")
plt.tight_layout()
plt.savefig("feature_importance.png")
plt.close()

# ------------------------------------------------------------------
# Save summary
# ------------------------------------------------------------------
with open("model_summary.txt", "w") as f:
    f.write("\n".join(summary_lines))

print("\nSaved: model_summary.txt, feature_importance.csv/png, confusion_matrix.png, roc_curve.png")
