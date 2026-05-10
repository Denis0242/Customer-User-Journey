
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Customer Journey Analytics", layout="wide")

df = pd.read_csv("../data/customer_user_journey_data.csv")

st.title("Customer User Journey Analytics Dashboard")

st.subheader("Dataset Preview")
st.dataframe(df.head())

st.subheader("KPI Summary")

col1, col2, col3 = st.columns(3)

if 'revenue' in df.columns:
    col1.metric("Total Revenue", f"${df['revenue'].sum():,.2f}")

if 'user_id' in df.columns:
    col2.metric("Total Users", df['user_id'].nunique())

if 'conversion_rate' in df.columns:
    col3.metric("Avg Conversion Rate", f"{df['conversion_rate'].mean():.2f}%")

st.subheader("Revenue Distribution")

if 'segment' in df.columns and 'revenue' in df.columns:
    st.bar_chart(df.groupby('segment')['revenue'].sum())

st.subheader("Risk Category Distribution")

if 'risk_category' in df.columns:
    st.bar_chart(df['risk_category'].value_counts())
