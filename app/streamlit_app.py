import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Customer User Journey Dashboard", layout="wide")

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "cleaned_user_journey.csv"
df = pd.read_csv(DATA_PATH)
df["journey_date"] = pd.to_datetime(df["journey_date"], errors="coerce")

st.title("Customer User Journey Dashboard")
st.caption("Product Analytics | Funnel, Retention, Revenue, Churn Risk, and Executive Decision Support")

with st.sidebar:
    st.header("Filters")
    countries = st.multiselect("Country", sorted(df["country"].dropna().unique()), default=sorted(df["country"].dropna().unique()))
    devices = st.multiselect("Device", sorted(df["device_type"].dropna().unique()), default=sorted(df["device_type"].dropna().unique()))
    segments = st.multiselect("Segment", sorted(df["customer_segment"].dropna().unique()), default=sorted(df["customer_segment"].dropna().unique()))
    channels = st.multiselect("Acquisition Channel", sorted(df["acquisition_channel"].dropna().unique()), default=sorted(df["acquisition_channel"].dropna().unique()))
    risks = st.multiselect("Risk Category", sorted(df["churn_risk_category"].dropna().unique()), default=sorted(df["churn_risk_category"].dropna().unique()))

filtered = df[
    df["country"].isin(countries) &
    df["device_type"].isin(devices) &
    df["customer_segment"].isin(segments) &
    df["acquisition_channel"].isin(channels) &
    df["churn_risk_category"].isin(risks)
]

user_level = filtered.sort_values("journey_date").drop_duplicates("customer_id")
total_users = filtered["customer_id"].nunique()
purchase_users = filtered.loc[filtered["funnel_stage"].str.lower() == "purchase", "customer_id"].nunique()
conversion_rate = purchase_users / total_users if total_users else 0
d1_retention = user_level["d1_retained"].mean() if len(user_level) else 0
d7_retention = user_level["d7_retained"].mean() if len(user_level) else 0
revenue_per_user = filtered["revenue"].sum() / total_users if total_users else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Users", f"{total_users:,}")
c2.metric("Conversion Rate", f"{conversion_rate:.2%}")
c3.metric("D1 Retention", f"{d1_retention:.2%}")
c4.metric("D7 Retention", f"{d7_retention:.2%}")
c5.metric("Revenue per User", f"${revenue_per_user:,.2f}")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Funnel Chart")
    funnel = filtered.groupby(["funnel_stage_order", "funnel_stage"], as_index=False)["customer_id"].nunique().sort_values("funnel_stage_order")
    fig = px.funnel(funnel, x="customer_id", y="funnel_stage", text="customer_id")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Drop-off Analysis")
    f = funnel.copy()
    f["next_users"] = f["customer_id"].shift(-1)
    f["dropoff_rate"] = 1 - (f["next_users"] / f["customer_id"])
    f = f.dropna(subset=["dropoff_rate"])
    f["stage_pair"] = f["funnel_stage"] + " → Next"
    fig = px.bar(f, x="stage_pair", y="dropoff_rate", text=f["dropoff_rate"].map(lambda x: f"{x:.2%}"))
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

with col3:
    st.subheader("Retention Trend")
    trend = filtered.groupby("journey_date", as_index=False).agg(d1_retention=("d1_retained", "mean"), d7_retention=("d7_retained", "mean"))
    trend_long = trend.melt(id_vars="journey_date", value_vars=["d1_retention", "d7_retention"], var_name="metric", value_name="rate")
    fig = px.line(trend_long, x="journey_date", y="rate", color="metric", markers=True)
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

col4, col5, col6 = st.columns(3)
with col4:
    st.subheader("Churn Risk Distribution")
    risk = user_level.groupby("churn_risk_category", as_index=False)["customer_id"].nunique()
    fig = px.pie(risk, names="churn_risk_category", values="customer_id", hole=0.45)
    st.plotly_chart(fig, use_container_width=True)

with col5:
    st.subheader("Conversion by Channel")
    channel = filtered.groupby("acquisition_channel").agg(total_users=("customer_id", "nunique"), purchase_users=("converted_flag", "sum")).reset_index()
    channel["conversion_rate"] = channel["purchase_users"] / channel["total_users"]
    fig = px.bar(channel, x="acquisition_channel", y="conversion_rate", text=channel["conversion_rate"].map(lambda x: f"{x:.2%}"))
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

with col6:
    st.subheader("Revenue by Segment")
    revenue = filtered.groupby("customer_segment", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    fig = px.bar(revenue, x="customer_segment", y="revenue", text="revenue")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Customer Journey Detail Table")
detail = filtered.groupby(["customer_id", "country", "device_type", "customer_segment", "acquisition_channel", "churn_risk_category"], as_index=False).agg(
    latest_stage_order=("funnel_stage_order", "max"),
    total_revenue=("revenue", "sum"),
    d1_retained=("d1_retained", "max"),
    d7_retained=("d7_retained", "max"),
)
st.dataframe(detail.sort_values("total_revenue", ascending=False), use_container_width=True)

st.divider()

st.markdown("## Executive Decision Summary")

st.markdown("""
<style>
.summary-container {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
    margin-top: 20px;
}
.summary-title {
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 18px;
    color: #303342;
}
.summary-card {
    padding: 24px;
    border-radius: 10px;
    font-size: 18px;
    line-height: 1.6;
    min-height: 210px;
}
.insight-card {
    background-color: #E8F2FF;
    color: #0057B8;
}
.action-card {
    background-color: #FFFDE7;
    color: #8A6500;
}
.recommendation-card {
    background-color: #E6F7EC;
    color: #087B32;
}
.decision-card {
    background-color: #FDE7E9;
    color: #B3262E;
}
</style>

<div class="summary-container">

<div>
    <div class="summary-title">🔎 Insight</div>
    <div class="summary-card insight-card">
        Users progress through early funnel stages, but checkout abandonment and lower <b>D7 retention</b> create growth leakage.
    </div>
</div>

<div>
    <div class="summary-title">⚙️ Action</div>
    <div class="summary-card action-card">
        Analyze checkout friction, monitor <b>D7 retention</b>, and identify high-risk users before they drop from the funnel.
    </div>
</div>

<div>
    <div class="summary-title">✅ Recommendation</div>
    <div class="summary-card recommendation-card">
        Optimize checkout UX, improve trust signals, and run targeted retention campaigns for early-stage users.
    </div>
</div>

<div>
    <div class="summary-title">⭐ Decision</div>
    <div class="summary-card decision-card">
        Prioritize checkout-stage optimization and D7 retention improvement before scaling acquisition spend.
    </div>
</div>

</div>
""", unsafe_allow_html=True)