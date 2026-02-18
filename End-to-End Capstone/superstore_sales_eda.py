

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (8, 5)

if not os.path.exists("outputs"):
    os.makedirs("outputs")


df = pd.read_csv("sales_data.csv", parse_dates=["Order Date", "Ship Date"])

print("Shape of dataset:", df.shape)
print("\nData Types:\n", df.dtypes)
print("\nMissing Values:\n", df.isnull().sum())



df["Revenue"] = df["Sales"]

total_revenue = df["Revenue"].sum()

order_totals = df.groupby("Order ID")["Revenue"].sum()
avg_order_value = order_totals.mean()

region_revenue = df.groupby("Region")["Revenue"].sum().sort_values(ascending=False)

top_products = df.groupby("Product Name")["Revenue"].sum().sort_values(ascending=False).head(10)

df["Order Year"] = df["Order Date"].dt.year
df["Order Month"] = df["Order Date"].dt.month

monthly_trend = df.groupby(["Order Year", "Order Month"])["Revenue"].sum().reset_index()


print("\nTotal Revenue:", total_revenue)
print("Average Order Value:", round(avg_order_value, 2))
print("Top Regions by Revenue:\n", region_revenue)
print("Top 10 Products by Revenue:\n", top_products)

plt.figure()
sns.barplot(x=region_revenue.values, y=region_revenue.index)
plt.title("Revenue by Region")
plt.xlabel("Revenue")
plt.ylabel("Region")
plt.tight_layout()
plt.savefig("outputs/revenue_by_region.png")
plt.show()

plt.figure(figsize=(10,6))
sns.barplot(x=top_products.values, y=top_products.index)
plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig("outputs/top_10_products.png")
plt.show()

plt.figure(figsize=(10,5))
sns.lineplot(
    data=monthly_trend,
    x=pd.to_datetime(monthly_trend["Order Year"].astype(str) + "-" + monthly_trend["Order Month"].astype(str)),
    y="Revenue"
)
plt.title("Monthly Revenue Trend")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig("outputs/monthly_trend.png")
plt.show()

plt.figure()
sns.histplot(order_totals, bins=30, kde=True)
plt.title("Distribution of Order Totals")
plt.xlabel("Order Revenue")
plt.tight_layout()
plt.savefig("outputs/order_value_distribution.png")
plt.show()

summary_text = f"""
SUPERSTORE SALES EDA – SUMMARY
==============================

1) Total Revenue: {total_revenue}

2) Average Order Value: {round(avg_order_value,2)}

3) Top Region: {region_revenue.index[0]} ({region_revenue.values[0]})

4) Most Profitable Product: {top_products.index[0]} ({top_products.values[0]})

5) Sales Seasonality:
   See monthly trend chart for patterns.

KEY INSIGHTS:
- Region {region_revenue.index[0]} generates the highest revenue.
- Top products contribute disproportionately to total revenue.
- Month-over-month trend shows seasonal patterns.

EXPORTS:
- All charts are saved in outputs/ folder.
"""

with open("outputs/superstore_sales_summary.txt", "w") as f:
    f.write(summary_text)

print("\nReport exported to outputs/ folder!")
print("\nProject Completed Successfully")
