"""
Module 1: Data Ingestion & Cleaning
Delivery Performance, Delay Risk, and Logistics Efficiency Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn

print("All good!")

# ------------------------------------------------------------------
# 1. Load
# ------------------------------------------------------------------
RAW_PATH = "APL_Logistics.csv"
df = pd.read_csv(RAW_PATH, encoding="ISO-8859-1")

print(f"Raw shape: {df.shape}")

# ------------------------------------------------------------------
# 2. Handle missing values
# ------------------------------------------------------------------
# Only Customer Lname (8) and Customer Zipcode (3) have nulls - negligible, drop them
df = df.dropna(subset=["Customer Lname", "Customer Zipcode"])

# ------------------------------------------------------------------
# 3. Drop exact duplicate rows (none found, but keep this for safety)
# ------------------------------------------------------------------
before = len(df)
df = df.drop_duplicates()
print(f"Dropped {before - len(df)} duplicate rows")

# -----------------------------------------------------------------
# \
   # 4. Standardize dtype
# ------------------------------------------------------------------
categorical_cols = [
    "Type", "Delivery Status", "Category Name", "Customer Country",
    "Customer Segment", "Customer State", "Department Name", "Market",
    "Order Country", "Order Region", "Order State", "Order Status",
    "Shipping Mode",
]
for col in categorical_cols:
    df[col] = df[col].astype("category")

# ------------------------------------------------------------------
# 5. Drop columns not needed for analysis (raw PII)
#    Keep commented out if you want customer-level drill-down later
# ------------------------------------------------------------------
pii_cols = ["Customer Fname", "Customer Lname", "Customer Street"]
df = df.drop(columns=pii_cols)

# ------------------------------------------------------------------
# 6. Sanity checks
# ------------------------------------------------------------------
assert df["Days for shipping (real)"].ge(0).all(), "Negative shipping days found"
assert df["Days for shipment (scheduled)"].ge(0).all(), "Negative scheduled days found"

print(f"Clean shape: {df.shape}")
print(df.dtypes)

# ------------------------------------------------------------------
# 7. Save cleaned dataset
# ------------------------------------------------------------------
OUT_PATH = "cleaned_logistics.csv"
df.to_csv(OUT_PATH, index=False)
print(f"Saved cleaned dataset to {OUT_PATH}")
