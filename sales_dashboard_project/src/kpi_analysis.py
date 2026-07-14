"""
kpi_analysis.py
----------------
Computes the KPIs and breakdowns used by the dashboard:
- Total Revenue, Total Profit, Total Orders (+ vs previous period)
- Monthly sales trend
- Category-wise sales share
- Region-wise sales
"""

import pandas as pd


def load_clean_data(path: str = "data/clean_sales_data.csv") -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["Order Date"])
    return df


def get_kpis(df: pd.DataFrame, split_date: str = None) -> dict:
    """Total revenue/profit/orders, plus % change vs the previous period
    (first half of the date range vs second half)."""
    df = df.sort_values("Order Date")
    if split_date is None:
        mid_point = df["Order Date"].min() + (
            df["Order Date"].max() - df["Order Date"].min()
        ) / 2
    else:
        mid_point = pd.Timestamp(split_date)

    prev = df[df["Order Date"] < mid_point]
    curr = df[df["Order Date"] >= mid_point]

    def pct_change(curr_val, prev_val):
        if prev_val == 0:
            return 0.0
        return round((curr_val - prev_val) / prev_val * 100, 1)

    kpis = {
        "total_revenue": round(df["Revenue"].sum(), 2),
        "total_profit": round(df["Profit"].sum(), 2),
        "total_orders": len(df),
        "revenue_change_pct": pct_change(curr["Revenue"].sum(), prev["Revenue"].sum()),
        "profit_change_pct": pct_change(curr["Profit"].sum(), prev["Profit"].sum()),
        "orders_change_pct": pct_change(len(curr), len(prev)),
    }
    return kpis


def monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        df.set_index("Order Date")
        .resample("ME")["Revenue"]
        .sum()
        .reset_index()
    )
    monthly["Month"] = monthly["Order Date"].dt.strftime("%b")
    return monthly[["Month", "Revenue"]]


def category_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    cat = (
        df.groupby("Category")["Revenue"]
        .sum()
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )
    cat["Share %"] = round(cat["Revenue"] / cat["Revenue"].sum() * 100, 1)
    return cat


def region_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    reg = (
        df.groupby("Region")["Revenue"]
        .sum()
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )
    return reg


if __name__ == "__main__":
    df = load_clean_data()
    print("KPIs:", get_kpis(df))
    print("\nMonthly Trend:\n", monthly_trend(df))
    print("\nCategory Breakdown:\n", category_breakdown(df))
    print("\nRegion Breakdown:\n", region_breakdown(df))
