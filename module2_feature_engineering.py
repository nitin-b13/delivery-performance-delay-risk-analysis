"""
Module 2: Feature Engineering
Delivery Performance, Delay Risk, and Logistics Efficiency Analysis
Input:  cleaned_logistics.csv (output of Module 1)
Output: featured_logistics.csv
"""

import pandas as pd
import numpy as np

# ------------------------------------------------------------------
# 1. Load cleaned data
# ------------------------------------------------------------------
IN_PATH = "cleaned_logistics.csv"
df = pd.read_csv(IN_PATH)
print(f"Loaded shape: {df.shape}")

# ------------------------------------------------------------------
# 2. Delay & on-time features
# ------------------------------------------------------------------
# Positive = shipped later than scheduled (late), negative/zero = on-time or early
df["Delay Days"] = df["Days for shipping (real)"] - df["Days for shipment (scheduled)"]

df["On Time Flag"] = np.where(df["Delay Days"] <= 0, 1, 0)

def delay_bucket(x):
    if x < 0:
        return "Early"
    elif x == 0:
        return "On Time"
    elif x <= 2:
        return "Slightly Late (1-2 days)"
    else:
        return "Very Late (3+ days)"

df["Delay Category"] = df["Delay Days"].apply(delay_bucket)

# ------------------------------------------------------------------
# 3. Profitability / cost efficiency features
# ------------------------------------------------------------------
df["Profit Margin Ratio"] = np.where(
    df["Sales"] != 0, df["Order Profit Per Order"] / df["Sales"], np.nan
)

df["Discounted Price"] = df["Order Item Product Price"] * (1 - df["Order Item Discount Rate"])

df["Revenue per Unit"] = np.where(
    df["Order Item Quantity"] != 0,
    df["Order Item Total"] / df["Order Item Quantity"],
    np.nan,
)

# ------------------------------------------------------------------
# 4. Logistics efficiency features
# ------------------------------------------------------------------
# Scheduled speed vs actual speed — ratio > 1 means took longer than planned
df["Shipping Time Ratio"] = np.where(
    df["Days for shipment (scheduled)"] != 0,
    df["Days for shipping (real)"] / df["Days for shipment (scheduled)"],
    np.nan,
)

# ------------------------------------------------------------------
# 5. Encode key categoricals (label encoding for modeling use later)
# ------------------------------------------------------------------
cat_cols_to_encode = ["Shipping Mode", "Market", "Customer Segment", "Order Region"]
for col in cat_cols_to_encode:
    df[col + " Code"] = df[col].astype("category").cat.codes

# ------------------------------------------------------------------
# 6. Quick sanity summary
# ------------------------------------------------------------------
print("\nOn-time rate overall: {:.2%}".format(df["On Time Flag"].mean()))
print("\nDelay Category distribution:")
print(df["Delay Category"].value_counts())
print("\nAvg Delay Days by Shipping Mode:")
print(df.groupby("Shipping Mode")["Delay Days"].mean().sort_values())

# ------------------------------------------------------------------
# 7. Save
# ------------------------------------------------------------------
OUT_PATH = "featured_logistics.csv"
df.to_csv(OUT_PATH, index=False)
print(f"\nSaved feature-engineered dataset to {OUT_PATH}  |  shape={df.shape}")
