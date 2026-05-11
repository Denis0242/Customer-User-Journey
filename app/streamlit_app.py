import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent))
from utils import load_data, compute_kpis, funnel_table
from components import decision_panel

st.set_page_config(page_title="Customer User Journey Dashboard", layout="wide")
st.title("Customer User Journey Dashboard")
st.caption("Product analytics case study: funnel conversion, retention, churn risk, and segment revenue")

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "customer_user_journey.csv"
df = load_data(DATA_PATH)

with st.sidebar:
    st.header("Filters")
    country = st.multiselect("Country", sorted(df["Country"].unique()), default=sorted(df["Country"].unique()))
    segment = st.multiselect("Segment", sorted(df["Customer Segment"].unique()), default=sorted(df["Customer Segment"].unique()))
    device = st.multiselect("Device", sorted(df["Device Type"].unique()), default=sorted(df["Device Type"].unique()))
    risk = st.multiselect("Risk Category", sorted(df["Churn Risk Category"].unique()), default=sorted(df["Churn Risk Category"].unique()))

filtered = df[df["Country"].isin(country) & df["Customer Segment"].isin(segment) & df["Device Type"].isin(device) & df["Churn Risk Category"].isin(risk)]
kpis = compute_kpis(filtered)

cols = st.columns(5)
cols[0].metric("Total Users", f"{kpis['Total Users']:,}")
cols[1].metric("Conversion Rate", f"{kpis['Conversion Rate']:.2%}")
cols[2].metric("D1 Retention", f"{kpis['D1 Retention']:.2%}")
cols[3].metric("D7 Retention", f"{kpis['D7 Retention']:.2%}")
cols[4].metric("Revenue per User", f"${kpis['Revenue per User']:,.2f}")

st.divider()
left, right = st.columns(2)
with left:
    st.subheader("Funnel Stage Users")
    ft = funnel_table(filtered)
    st.bar_chart(ft.set_index("Funnel Stage")["Users"])
with right:
    st.subheader("Retention Trend")
    trend = filtered.groupby("Journey Date")[["D1 Retained", "D7 Retained"]].mean().sort_index()
    st.line_chart(trend)

left, mid, right = st.columns(3)
with left:
    st.subheader("Churn Risk Distribution")
    st.bar_chart(filtered.groupby("Churn Risk Category")["Customer ID"].nunique())
with mid:
    st.subheader("Conversion by Channel")
    channel = filtered.groupby("Acquisition Channel")["Customer ID"].nunique()
    st.bar_chart(channel)
with right:
    st.subheader("Revenue by Segment")
    st.bar_chart(filtered.groupby("Customer Segment")["Revenue"].sum())

decision_panel()

st.subheader("Dataset Preview")
st.dataframe(filtered.head(50), use_container_width=True)
