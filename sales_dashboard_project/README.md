# Sales Dashboard Analysis (Python version)

Recreates the "Excel → SQL → Power BI" workflow using free, open-source Python
tools: **pandas** (cleaning + analysis) and **Streamlit + Plotly** (the dashboard).

## Folder structure
```
sales_dashboard_project/
├── data/
│   ├── raw_sales_data.csv       # generated messy "raw export"
│   └── clean_sales_data.csv     # produced by data_cleaning.py
├── src/
│   ├── generate_sample_data.py  # makes fake raw data (skip if you have real data)
│   ├── data_cleaning.py         # cleans dates, dupes, missing values
│   └── kpi_analysis.py          # computes KPIs, monthly trend, category/region breakdown
├── app.py                       # the Streamlit dashboard
├── requirements.txt
└── README.md
```

## How to run it on your machine

1. **Install Python 3.9+** if you don't have it already.

2. **Open a terminal in this folder** and create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: .\venv\Scripts\activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **(Optional) Generate sample data** — skip this step and drop your own CSV
   into `data/raw_sales_data.csv` if you already have real sales data with columns:
   `Order ID, Order Date, Category, Product, Region, Quantity, Unit Price, Revenue, Profit`
   ```bash
   python src/generate_sample_data.py
   ```

5. **Clean the data:**
   ```bash
   python src/data_cleaning.py
   ```

6. **Launch the dashboard:**
   ```bash
   streamlit run app.py
   ```
   This opens the dashboard in your browser at `http://localhost:8501`.

## What each script teaches (matches the "You'll Learn" list in your reference image)

| Skill              | Where it happens                          |
|---------------------|--------------------------------------------|
| Data Cleaning       | `src/data_cleaning.py`                     |
| KPI Creation        | `src/kpi_analysis.py` → `get_kpis()`       |
| Dashboard Design     | `app.py`                                    |
| Business Insights   | Monthly trend, category %, region breakdown |

## Using your own real data instead
Replace `data/raw_sales_data.csv` with your actual export (Excel → save as CSV
works fine), keeping the same column names, then re-run steps 5 and 6 above.
If your column names differ, just adjust the column names referenced in
`data_cleaning.py` and `kpi_analysis.py`.

## Swapping SQL in (optional, for the "SQL" step in the workflow)
Instead of reading straight from CSV, you can load `clean_sales_data.csv` into
a local SQLite database and query it with pandas:
```python
import sqlite3, pandas as pd
conn = sqlite3.connect("sales.db")
df.to_sql("sales", conn, if_exists="replace", index=False)
result = pd.read_sql("SELECT Category, SUM(Revenue) FROM sales GROUP BY Category", conn)
```
