"""
Module 3: Exploratory Data Analysis (EDA)
Delivery Performance, Delay Risk, and Logistics Efficiency Analysis
Input:  featured_logistics.csv (output of Module 2)
Output: eda_summary.txt + PNG charts in ./eda_charts/
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 110

IN_PATH = "featured_logistics.csv"
df = pd.read_csv(IN_PATH)

OUT_DIR = "eda_charts"
os.makedirs(OUT_DIR, exist_ok=True)

summary_lines = []

def log(msg):
    print(msg)
    summary_lines.append(str(msg))

log(f"Dataset shape: {df.shape}")

# ------------------------------------------------------------------
# 1. Delay distribution
# ------------------------------------------------------------------
plt.figure(figsize=(8, 5))
sns.histplot(df["Delay Days"], bins=range(int(df["Delay Days"].min()), int(df["Delay Days"].max()) + 2), kde=False)
plt.title("Distribution of Delivery Delay (Days)")
plt.xlabel("Delay Days (negative = early)")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/01_delay_distribution.png")
plt.close()

# ------------------------------------------------------------------
# 2. On-time rate by Shipping Mode
# ------------------------------------------------------------------
otr_mode = df.groupby("Shipping Mode")["On Time Flag"].mean().sort_values()
log("\nOn-time rate by Shipping Mode:\n" + otr_mode.to_string())

plt.figure(figsize=(7, 5))
otr_mode.plot(kind="barh", color="steelblue")
plt.title("On-Time Rate by Shipping Mode")
plt.xlabel("On-Time Rate")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/02_ontime_by_shipping_mode.png")
plt.close()

# ------------------------------------------------------------------
# 3. On-time rate by Market / Region
# ------------------------------------------------------------------
otr_market = df.groupby("Market")["On Time Flag"].mean().sort_values()
log("\nOn-time rate by Market:\n" + otr_market.to_string())

plt.figure(figsize=(7, 5))
otr_market.plot(kind="barh", color="darkorange")
plt.title("On-Time Rate by Market")
plt.xlabel("On-Time Rate")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/03_ontime_by_market.png")
plt.close()

# ------------------------------------------------------------------
# 4. Average delay by Order Region (top/bottom 10)
# ------------------------------------------------------------------
delay_region = df.groupby("Order Region")["Delay Days"].mean().sort_values()
log("\nWorst 10 regions by avg delay:\n" + delay_region.tail(10).to_string())
log("\nBest 10 regions by avg delay:\n" + delay_region.head(10).to_string())

plt.figure(figsize=(8, 6))
pd.concat([delay_region.head(5), delay_region.tail(5)]).plot(kind="barh", color="seagreen")
plt.title("Avg Delay Days: Best 5 vs Worst 5 Order Regions")
plt.xlabel("Avg Delay Days")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/04_delay_by_region_best_worst.png")
plt.close()

# ------------------------------------------------------------------
# 5. Late delivery risk by Category
# ------------------------------------------------------------------
risk_category = df.groupby("Category Name")["Late_delivery_risk"].mean().sort_values(ascending=False).head(10)
log("\nTop 10 product categories by late delivery risk:\n" + risk_category.to_string())

plt.figure(figsize=(8, 6))
risk_category.plot(kind="barh", color="firebrick")
plt.title("Top 10 Categories by Late Delivery Risk")
plt.xlabel("Late Delivery Risk (rate)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/05_risk_by_category.png")
plt.close()

# ------------------------------------------------------------------
# 6. Correlation heatmap of numeric features
# ------------------------------------------------------------------
numeric_cols = [
    "Days for shipping (real)", "Days for shipment (scheduled)", "Delay Days",
    "On Time Flag", "Late_delivery_risk", "Benefit per order", "Sales",
    "Order Item Quantity", "Order Item Discount Rate", "Order Item Profit Ratio",
    "Profit Margin Ratio", "Shipping Time Ratio"
]
corr = df[numeric_cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0)
plt.title("Correlation Heatmap - Key Numeric Features")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/06_correlation_heatmap.png")
plt.close()

# ------------------------------------------------------------------
# 7. Sales vs Profit Margin scatter, colored by delay
# ------------------------------------------------------------------
sample = df.sample(min(5000, len(df)), random_state=42)
plt.figure(figsize=(8, 6))
sns.scatterplot(
    data=sample, x="Sales", y="Profit Margin Ratio",
    hue="Delay Category", alpha=0.5, s=15
)
plt.title("Sales vs Profit Margin Ratio (sampled), by Delay Category")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/07_sales_vs_margin_by_delay.png")
plt.close()

# ------------------------------------------------------------------
# 8. Order Status breakdown
# ------------------------------------------------------------------
status_counts = df["Order Status"].value_counts()
log("\nOrder Status breakdown:\n" + status_counts.to_string())

# ------------------------------------------------------------------
# Save summary text
# ------------------------------------------------------------------
with open("eda_summary.txt", "w") as f:
    f.write("\n".join(summary_lines))

print(f"\nCharts saved to ./{OUT_DIR}/  |  Summary saved to eda_summary.txt")
