"""
generate_sample_data.py
------------------------
Creates a realistic, slightly messy raw sales dataset (like a real Excel export
from a store) so you have something to practice "Data Cleaning" on -
exactly like Step 1 (Excel -> SQL -> Power BI) in the workflow image.

Run:
    python src/generate_sample_data.py
Output:
    data/raw_sales_data.csv
"""

import random
import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

CATEGORIES = ["Technology", "Furniture", "Office Supplies", "Others"]
CATEGORY_WEIGHTS = [0.40, 0.30, 0.20, 0.10]  # matches the donut chart in the image

REGIONS = ["North America", "South America", "Europe", "Africa", "Asia", "Oceania"]
REGION_WEIGHTS = [0.35, 0.15, 0.20, 0.05, 0.20, 0.05]

PRODUCTS = {
    "Technology": ["Laptop", "Monitor", "Printer", "Router", "Webcam"],
    "Furniture": ["Office Chair", "Desk", "Bookshelf", "Cabinet"],
    "Office Supplies": ["Paper", "Stapler", "Pen Pack", "Notebook"],
    "Others": ["Misc Item", "Gift Card", "Sample Kit"],
}

START_DATE = pd.Timestamp("2024-01-01")
END_DATE = pd.Timestamp("2024-06-30")

n_rows = 4650  # matches "Total Orders: 4,650" in the image

rows = []
for i in range(n_rows):
    order_id = f"ORD-{10000 + i}"
    order_date = START_DATE + pd.Timedelta(
        days=np.random.randint(0, (END_DATE - START_DATE).days + 1)
    )
    category = np.random.choice(CATEGORIES, p=CATEGORY_WEIGHTS)
    product = np.random.choice(PRODUCTS[category])
    region = np.random.choice(REGIONS, p=REGION_WEIGHTS)

    quantity = np.random.randint(1, 6)
    unit_price = round(np.random.uniform(15, 500), 2)
    revenue = round(quantity * unit_price, 2)
    profit_margin = np.random.uniform(0.10, 0.25)
    profit = round(revenue * profit_margin, 2)

    rows.append(
        {
            "Order ID": order_id,
            "Order Date": order_date.strftime("%m/%d/%Y"),  # messy US string date
            "Category": category,
            "Product": product,
            "Region": region,
            "Quantity": quantity,
            "Unit Price": unit_price,
            "Revenue": revenue,
            "Profit": profit,
        }
    )

df = pd.DataFrame(rows)


dupes = df.sample(30, random_state=1)
df = pd.concat([df, dupes], ignore_index=True)


for col in ["Quantity", "Unit Price", "Region"]:
    idx = df.sample(frac=0.01, random_state=2).index
    df.loc[idx, col] = np.nan


messy_idx = df.sample(frac=0.02, random_state=3).index
df.loc[messy_idx, "Category"] = df.loc[messy_idx, "Category"].str.upper()


df = df.sample(frac=1, random_state=4).reset_index(drop=True)

df.to_csv("data/raw_sales_data.csv", index=False)
print(f"Created data/raw_sales_data.csv with {len(df)} rows (includes intentional mess).")
