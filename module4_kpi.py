"""
Module 4: Delivery Performance & KPI Module
Delivery Performance, Delay Risk, and Logistics Efficiency Analysis
Input:  featured_logistics.csv (output of Module 2)
Output: kpi_summary.txt + kpi_by_*.csv tables in ./kpi_tables/
"""

import pandas as pd
import numpy as np
import os

IN_PATH = "featured_logistics.csv"
df = pd.read_csv(IN_PATH)

OUT_DIR = "kpi_tables"
os.makedirs(OUT_DIR, exist_ok=True)

summary_lines = []

def log(msg):
    print(msg)
    summary_lines.append(str(msg))

log(f"Dataset shape: {df.shape}")

# ------------------------------------------------------------------
# 1. OTIF - On Time In Full
# ------------------------------------------------------------------
# "In Full" proxy: order was not cancelled/suspected fraud/on-hold (i.e. actually fulfilled)
in_full_statuses = ["COMPLETE", "CLOSED", "PROCESSING", "PENDING", "PENDING_PAYMENT"]
df["In Full Flag"] = df["Order Status"].isin(in_full_statuses).astype(int)
df["OTIF Flag"] = ((df["On Time Flag"] == 1) & (df["In Full Flag"] == 1)).astype(int)

otif_rate = df["OTIF Flag"].mean()
log(f"\nOverall OTIF Rate: {otif_rate:.2%}")

# ------------------------------------------------------------------
# 2. Perfect Order Rate
#    Perfect = on time + in full + no discount issues (proxy: not cancelled/fraud) + delivered as Complete/Closed
# ------------------------------------------------------------------
perfect_statuses = ["COMPLETE", "CLOSED"]
df["Perfect Order Flag"] = (
    (df["On Time Flag"] == 1) & (df["Order Status"].isin(perfect_statuses))
).astype(int)

perfect_order_rate = df["Perfect Order Flag"].mean()
log(f"Perfect Order Rate: {perfect_order_rate:.2%}")

# ------------------------------------------------------------------
# 3. Average Delay & Late Delivery Risk
# ------------------------------------------------------------------
avg_delay = df["Delay Days"].mean()
late_risk_rate = df["Late_delivery_risk"].mean()
log(f"Average Delay (days): {avg_delay:.2f}")
log(f"Overall Late Delivery Risk Rate: {late_risk_rate:.2%}")

# ------------------------------------------------------------------
# 4. Cost / Efficiency KPIs
# ------------------------------------------------------------------
avg_profit_margin = df["Profit Margin Ratio"].mean()
avg_discount_rate = df["Order Item Discount Rate"].mean()
avg_sales_per_order = df["Sales"].mean()

log(f"Average Profit Margin Ratio: {avg_profit_margin:.2%}")
log(f"Average Discount Rate: {avg_discount_rate:.2%}")
log(f"Average Sales per Order: {avg_sales_per_order:.2f}")

# ------------------------------------------------------------------
# 5. KPI breakdown tables by key dimensions
# ------------------------------------------------------------------
def kpi_by(dim):
    g = df.groupby(dim).agg(
        Orders=("OTIF Flag", "count"),
        OTIF_Rate=("OTIF Flag", "mean"),
        Perfect_Order_Rate=("Perfect Order Flag", "mean"),
        Avg_Delay_Days=("Delay Days", "mean"),
        Late_Risk_Rate=("Late_delivery_risk", "mean"),
        Avg_Profit_Margin=("Profit Margin Ratio", "mean"),
        Avg_Sales=("Sales", "mean"),
    ).sort_values("OTIF_Rate")
    return g

for dim in ["Shipping Mode", "Market", "Order Region", "Customer Segment", "Category Name"]:
    table = kpi_by(dim)
    fname = f"{OUT_DIR}/kpi_by_{dim.replace(' ', '_').lower()}.csv"
    table.to_csv(fname)
    log(f"\n--- KPI by {dim} (saved to {fname}) ---")
    log(table.round(3).to_string())

# ------------------------------------------------------------------
# 6. Overall KPI scorecard
# ------------------------------------------------------------------
scorecard = pd.DataFrame({
    "KPI": [
        "OTIF Rate", "Perfect Order Rate", "Average Delay (days)",
        "Late Delivery Risk Rate", "Average Profit Margin", "Average Discount Rate",
        "Average Sales per Order"
    ],
    "Value": [
        otif_rate, perfect_order_rate, avg_delay,
        late_risk_rate, avg_profit_margin, avg_discount_rate,
        avg_sales_per_order
    ]
})
scorecard.to_csv(f"{OUT_DIR}/kpi_scorecard.csv", index=False)
log(f"\nOverall scorecard saved to {OUT_DIR}/kpi_scorecard.csv")

# ------------------------------------------------------------------
# Save summary
# ------------------------------------------------------------------
with open("kpi_summary.txt", "w") as f:
    f.write("\n".join(summary_lines))

print(f"\nKPI tables saved to ./{OUT_DIR}/  |  Summary saved to kpi_summary.txt")
