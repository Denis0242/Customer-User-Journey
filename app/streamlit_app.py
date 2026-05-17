import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Customer User Journey Dashboard", layout="wide")

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "user_journey_clean.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["journey_date"] = pd.to_datetime(df["journey_date"], errors="coerce")
    return df

df = load_data()

st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 900;
    color: #111827;
    padding: 10px 0 4px 0;
}
.sub-title {
    font-size: 18px;
    color: #374151;
    margin-bottom: 20px;
}
.metric-card {
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.metric-label {
    font-size: 14px;
    color: #6b7280;
    font-weight: 700;
}
.metric-value {
    font-size: 28px;
    color: #111827;
    font-weight: 900;
}
.insight {background:#e0f2fe;padding:16px;border-radius:14px;border-left:6px solid #0284c7;}
.action {background:#fef9c3;padding:16px;border-radius:14px;border-left:6px solid #ca8a04;}
.recommendation {background:#dcfce7;padding:16px;border-radius:14px;border-left:6px solid #16a34a;}
.decision {background:#ffe4e6;padding:16px;border-radius:14px;border-left:6px solid #e11d48;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Customer User Journey Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Product analytics view of funnel conversion, retention, churn risk, revenue, and acquisition performance.</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Filters")
    segments = st.multiselect("Customer Segment", sorted(df["customer_segment"].dropna().unique()), default=sorted(df["customer_segment"].dropna().unique()))
    channels = st.multiselect("Acquisition Channel", sorted(df["acquisition_channel"].dropna().unique()), default=sorted(df["acquisition_channel"].dropna().unique()))
    risks = st.multiselect("Churn Risk Category", sorted(df["churn_risk_category"].dropna().unique()), default=sorted(df["churn_risk_category"].dropna().unique()))

filtered = df[
    df["customer_segment"].isin(segments)
    & df["acquisition_channel"].isin(channels)
    & df["churn_risk_category"].isin(risks)
].copy()

awareness_users = filtered.loc[filtered["funnel_stage"] == "Awareness", "customer_id"].nunique()
purchase_users = filtered.loc[filtered["funnel_stage"] == "Purchase", "customer_id"].nunique()
overall_conversion = purchase_users / awareness_users if awareness_users else 0
d1 = filtered["d1_retained"].mean() if len(filtered) else 0
d7 = filtered["d7_retained"].mean() if len(filtered) else 0
revenue = filtered["revenue"].sum()
customers = filtered["customer_id"].nunique()

c1, c2, c3, c4, c5 = st.columns(5)
cards = [
    ("Customers", f"{customers:,.0f}"),
    ("Revenue", f"${revenue:,.0f}"),
    ("Overall Conversion", f"{overall_conversion:.1%}"),
    ("D1 Retention", f"{d1:.1%}"),
    ("D7 Retention", f"{d7:.1%}"),
]
for col, (label, value) in zip([c1,c2,c3,c4,c5], cards):
    col.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>', unsafe_allow_html=True)

st.divider()

funnel = filtered.groupby(["funnel_stage_order", "funnel_stage"])["customer_id"].nunique().reset_index(name="users").sort_values("funnel_stage_order")
fig_funnel = px.funnel(funnel, x="users", y="funnel_stage", title="Customer Journey Funnel")
fig_funnel.update_layout(showlegend=False, title_font_size=22, xaxis_title=None, yaxis_title=None)
fig_funnel.update_xaxes(showgrid=False)
fig_funnel.update_yaxes(showgrid=False)

daily = filtered.groupby("journey_date").agg(
    revenue=("revenue", "sum"),
    d1_retention=("d1_retained", "mean"),
    d7_retention=("d7_retained", "mean")
).reset_index()
fig_ret = px.line(daily, x="journey_date", y=["d1_retention", "d7_retention"], title="Retention Trend")
fig_ret.update_layout(title_font_size=22, xaxis_title=None, yaxis_title="Retention Rate", legend_title_text="")
fig_ret.update_xaxes(showgrid=False)
fig_ret.update_yaxes(showgrid=False, tickformat=".0%")

left, right = st.columns(2)
left.plotly_chart(fig_funnel, use_container_width=True)
right.plotly_chart(fig_ret, use_container_width=True)

seg = filtered.groupby("customer_segment").agg(
    revenue=("revenue", "sum"),
    users=("customer_id", "nunique"),
    d7_retention=("d7_retained", "mean")
).reset_index()
fig_seg = px.bar(seg, x="customer_segment", y="revenue", text_auto=True, title="Revenue by Customer Segment")
fig_seg.update_layout(showlegend=False, title_font_size=22, xaxis_title=None, yaxis_title=None)
fig_seg.update_xaxes(showgrid=False)
fig_seg.update_yaxes(showgrid=False)

channel = filtered.groupby("acquisition_channel").agg(
    revenue=("revenue", "sum"),
    users=("customer_id", "nunique"),
    d7_retention=("d7_retained", "mean")
).reset_index()
fig_channel = px.scatter(channel, x="users", y="revenue", size="d7_retention", hover_name="acquisition_channel", title="Channel Value: Users vs Revenue")
fig_channel.update_layout(showlegend=False, title_font_size=22, xaxis_title="Users", yaxis_title="Revenue")
fig_channel.update_xaxes(showgrid=False)
fig_channel.update_yaxes(showgrid=False)

left2, right2 = st.columns(2)
left2.plotly_chart(fig_seg, use_container_width=True)
right2.plotly_chart(fig_channel, use_container_width=True)

risk = filtered.groupby("churn_risk_category").agg(
    customers=("customer_id", "nunique"),
    revenue=("revenue", "sum"),
    d7_retention=("d7_retained", "mean")
).reset_index()
fig_risk = px.bar(risk, x="churn_risk_category", y="customers", text_auto=True, title="Customers by Churn Risk Category")
fig_risk.update_layout(showlegend=False, title_font_size=22, xaxis_title=None, yaxis_title=None)
fig_risk.update_xaxes(showgrid=False)
fig_risk.update_yaxes(showgrid=False)
st.plotly_chart(fig_risk, use_container_width=True)

st.subheader("Executive Decision Summary")
i1, i2, i3, i4 = st.columns(4)
i1.markdown("<div class='insight'><b>Insight</b><br>The funnel converts a smaller share of users into purchase, and D7 retention trails D1 retention.</div>", unsafe_allow_html=True)
i2.markdown("<div class='action'><b>Action</b><br>Monitor funnel drop-off, D7 retention, revenue per user, and churn-risk categories weekly.</div>", unsafe_allow_html=True)
i3.markdown("<div class='recommendation'><b>Recommendation</b><br>Improve high-drop-off stages and target retention campaigns to medium/high-risk groups.</div>", unsafe_allow_html=True)
i4.markdown("<div class='decision'><b>Decision</b><br>Improve and Monitor before scaling acquisition aggressively.</div>", unsafe_allow_html=True)

st.subheader("Filtered Data Preview")
st.dataframe(filtered.head(100), use_container_width=True)
