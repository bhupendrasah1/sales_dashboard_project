"""
app.py
------
Interactive Sales Dashboard (Streamlit + Plotly).
Recreates the layout in the reference image:
  - KPI cards: Total Revenue, Total Profit, Total Orders (with % vs previous period)
  - Monthly sales trend line chart
  - Category-wise sales donut chart
  - Region-wise sales map

Run:
    streamlit run app.py
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.kpi_analysis import (
    load_clean_data,
    get_kpis,
    monthly_trend,
    category_breakdown,
    region_breakdown,
)

st.set_page_config(page_title="Sales Dashboard", layout="wide", page_icon="📊")


st.markdown(
    """
    <style>
    .kpi-card {
        background-color: #FFF8EE;
        border: 1px solid #F0E4CC;
        border-radius: 10px;
        padding: 16px 20px;
        text-align: left;
    }
    .kpi-label { font-size: 13px; color: #7A7266; margin-bottom: 4px; }
    .kpi-value { font-size: 28px; font-weight: 700; color: #1A1A1A; }
    .kpi-delta-up { color: #1E9E56; font-size: 13px; font-weight: 600; }
    .kpi-delta-down { color: #D64545; font-size: 13px; font-weight: 600; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Load data ----------
@st.cache_data
def get_data():
    return load_clean_data("data/clean_sales_data.csv")

df = get_data()

# ---------- Header + date filter ----------
left, right = st.columns([3, 1])
with left:
    st.title("📊 Sales Dashboard")
with right:
    date_range = st.date_input(
        "Date Range",
        value=(df["Order Date"].min().date(), df["Order Date"].max().date()),
    )

if len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    df = df[(df["Order Date"] >= start) & (df["Order Date"] <= end)]

# ---------- KPI cards ----------
kpis = get_kpis(df)

def kpi_card(col, label, value, change):
    arrow = "▲" if change >= 0 else "▼"
    cls = "kpi-delta-up" if change >= 0 else "kpi-delta-down"
    col.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="{cls}">{arrow} {abs(change)}% vs Previous Period</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

c1, c2, c3 = st.columns(3)
kpi_card(c1, "TOTAL REVENUE", f"${kpis['total_revenue']:,.0f}", kpis["revenue_change_pct"])
kpi_card(c2, "TOTAL PROFIT", f"${kpis['total_profit']:,.0f}", kpis["profit_change_pct"])
kpi_card(c3, "TOTAL ORDERS", f"{kpis['total_orders']:,}", kpis["orders_change_pct"])

st.write("")

# ---------- Monthly trend ----------
st.subheader("Sales Trend (Monthly)")
trend = monthly_trend(df)
fig_trend = px.line(trend, x="Month", y="Revenue", markers=True)
fig_trend.update_traces(line_color="#E0A93A", line_width=3, marker=dict(size=8, color="#E0A93A"))
fig_trend.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    yaxis_tickprefix="$",
    margin=dict(l=10, r=10, t=10, b=10),
)
st.plotly_chart(fig_trend, use_container_width=True)

# ---------- Category + Region ----------
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Category Wise Sales")
    cat = category_breakdown(df)
    fig_cat = go.Figure(
        data=[
            go.Pie(
                labels=cat["Category"],
                values=cat["Revenue"],
                hole=0.55,
                marker=dict(colors=["#3C3C3C", "#E0A93A", "#D8CBB0", "#111111"]),
            )
        ]
    )
    fig_cat.update_layout(margin=dict(l=10, r=10, t=10, b=10), showlegend=True)
    st.plotly_chart(fig_cat, use_container_width=True)

with col_b:
    st.subheader("Sales by Region")
    reg = region_breakdown(df)
    fig_map = px.choropleth(
        reg,
        locations="Region",
        locationmode="country names",  # fine for demo regions like "Europe" it'll just skip unmapped
        color="Revenue",
        color_continuous_scale="YlOrBr",
    )
    fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_map, use_container_width=True)
    st.caption("Note: sample data uses continents; swap in real country names for an accurate map.")

st.divider()
st.caption("Built with pandas + Streamlit + Plotly — see src/ for the cleaning & KPI logic.")
