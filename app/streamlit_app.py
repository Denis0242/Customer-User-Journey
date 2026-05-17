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

# ---------------------------------------------------------
# Custom Styling
# ---------------------------------------------------------
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
.insight {background:#e0f2fe;padding:16px;border-radius:14px;border-left:6px solid #0284c7; min-height:150px;}
.action {background:#fef9c3;padding:16px;border-radius:14px;border-left:6px solid #ca8a04; min-height:150px;}
.recommendation {background:#dcfce7;padding:16px;border-radius:14px;border-left:6px solid #16a34a; min-height:150px;}
.decision {background:#ffe4e6;padding:16px;border-radius:14px;border-left:6px solid #e11d48; min-height:150px;}
.exp-card {
    background:#f8fafc;
    border:1px solid #e5e7eb;
    border-radius:16px;
    padding:18px;
    min-height:145px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.exp-title {
    font-weight:900;
    font-size:17px;
    color:#111827;
    margin-bottom:8px;
}
.exp-body {
    font-size:15px;
    color:#374151;
    line-height:1.5;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Customer User Journey Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Product analytics view of funnel conversion, retention, churn risk, revenue, acquisition performance, and executive decision support.</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------------
with st.sidebar:
    st.header("Filters")
    segments = st.multiselect(
        "Customer Segment",
        sorted(df["customer_segment"].dropna().unique()),
        default=sorted(df["customer_segment"].dropna().unique())
    )
    channels = st.multiselect(
        "Acquisition Channel",
        sorted(df["acquisition_channel"].dropna().unique()),
        default=sorted(df["acquisition_channel"].dropna().unique())
    )
    risks = st.multiselect(
        "Churn Risk Category",
        sorted(df["churn_risk_category"].dropna().unique()),
        default=sorted(df["churn_risk_category"].dropna().unique())
    )

filtered = df[
    df["customer_segment"].isin(segments)
    & df["acquisition_channel"].isin(channels)
    & df["churn_risk_category"].isin(risks)
].copy()

# ---------------------------------------------------------
# KPI Calculations
# ---------------------------------------------------------
awareness_users = filtered.loc[filtered["funnel_stage"] == "Awareness", "customer_id"].nunique()
purchase_users = filtered.loc[filtered["funnel_stage"] == "Purchase", "customer_id"].nunique()
overall_conversion = purchase_users / awareness_users if awareness_users else 0

d1 = filtered["d1_retained"].mean() if len(filtered) else 0
d7 = filtered["d7_retained"].mean() if len(filtered) else 0
retention_gap = d1 - d7

revenue = filtered["revenue"].sum()
customers = filtered["customer_id"].nunique()
revenue_per_customer = revenue / customers if customers else 0

high_risk_customers = filtered.loc[
    filtered["churn_risk_category"].str.lower().str.contains("high", na=False),
    "customer_id"
].nunique()
high_risk_rate = high_risk_customers / customers if customers else 0

# ---------------------------------------------------------
# KPI Cards
# ---------------------------------------------------------
c1, c2, c3, c4, c5 = st.columns(5)

cards = [
    ("Customers", f"{customers:,.0f}"),
    ("Revenue", f"${revenue:,.0f}"),
    ("Overall Conversion", f"{overall_conversion:.1%}"),
    ("D7 Retention", f"{d7:.1%}"),
    ("High-Risk Customers", f"{high_risk_rate:.1%}"),
]

for col, (label, value) in zip([c1, c2, c3, c4, c5], cards):
    col.markdown(
        f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>',
        unsafe_allow_html=True
    )

st.divider()

# ---------------------------------------------------------
# Dynamic Executive Decision Summary
# ---------------------------------------------------------
if overall_conversion < 0.25:
    insight_text = "The funnel is under-converting users into purchases, showing potential friction between awareness and purchase."
    action_text = "Prioritize funnel-stage diagnosis and identify the largest drop-off point before increasing acquisition spend."
    recommendation_text = "Run a checkout or activation improvement test focused on reducing friction and improving completion."
    decision_text = "Improve funnel conversion before scaling acquisition aggressively."
elif d7 < 0.35:
    insight_text = "D7 retention is weaker than expected, which means users are not returning strongly after early engagement."
    action_text = "Monitor D1-to-D7 retention decay and isolate segments with the fastest drop in repeat engagement."
    recommendation_text = "Launch targeted lifecycle messaging and onboarding improvements for low-retention segments."
    decision_text = "Prioritize retention improvement before focusing on new growth channels."
elif high_risk_rate > 0.30:
    insight_text = "A meaningful share of users are classified as high churn risk, creating potential revenue leakage."
    action_text = "Segment high-risk customers by channel and customer segment to identify preventable churn patterns."
    recommendation_text = "Create targeted retention campaigns for high-risk, high-value customers."
    decision_text = "Focus on churn-risk reduction to protect existing revenue."
else:
    insight_text = "The journey shows healthy product performance across conversion, retention, and churn-risk signals."
    action_text = "Continue monitoring funnel conversion, D7 retention, revenue per customer, and risk distribution weekly."
    recommendation_text = "Scale the strongest channels while maintaining retention and revenue guardrails."
    decision_text = "Scale selectively while continuing product-health monitoring."

st.subheader("Executive Decision Summary")
i1, i2, i3, i4 = st.columns(4)
i1.markdown(f"<div class='insight'><b>Insight</b><br>{insight_text}</div>", unsafe_allow_html=True)
i2.markdown(f"<div class='action'><b>Action</b><br>{action_text}</div>", unsafe_allow_html=True)
i3.markdown(f"<div class='recommendation'><b>Recommendation</b><br>{recommendation_text}</div>", unsafe_allow_html=True)
i4.markdown(f"<div class='decision'><b>Decision</b><br>{decision_text}</div>", unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------
# Funnel + Retention Trend
# ---------------------------------------------------------
funnel = (
    filtered.groupby(["funnel_stage_order", "funnel_stage"])["customer_id"]
    .nunique()
    .reset_index(name="users")
    .sort_values("funnel_stage_order")
)

fig_funnel = px.funnel(
    funnel,
    x="users",
    y="funnel_stage",
    title="Customer Journey Funnel"
)
fig_funnel.update_layout(showlegend=False, title_font_size=22, xaxis_title=None, yaxis_title=None)
fig_funnel.update_xaxes(showgrid=False)
fig_funnel.update_yaxes(showgrid=False)

daily = (
    filtered.groupby("journey_date")
    .agg(
        revenue=("revenue", "sum"),
        d1_retention=("d1_retained", "mean"),
        d7_retention=("d7_retained", "mean")
    )
    .reset_index()
)

fig_ret = px.line(
    daily,
    x="journey_date",
    y=["d1_retention", "d7_retention"],
    title="Retention Trend"
)
fig_ret.update_layout(title_font_size=22, xaxis_title=None, yaxis_title="Retention Rate", legend_title_text="")
fig_ret.update_xaxes(showgrid=False)
fig_ret.update_yaxes(showgrid=False, tickformat=".0%")

left, right = st.columns(2)
left.plotly_chart(fig_funnel, use_container_width=True)
right.plotly_chart(fig_ret, use_container_width=True)

# ---------------------------------------------------------
# Retention Cohort Heatmap
# ---------------------------------------------------------
st.subheader("Retention Cohort Heatmap")

cohort = filtered.copy()
cohort["cohort_month"] = cohort.groupby("customer_id")["journey_date"].transform("min").dt.to_period("M").astype(str)
cohort["activity_month"] = cohort["journey_date"].dt.to_period("M").astype(str)

cohort_table = (
    cohort.groupby(["cohort_month", "activity_month"])["customer_id"]
    .nunique()
    .reset_index(name="active_users")
)

cohort_sizes = (
    cohort.groupby("cohort_month")["customer_id"]
    .nunique()
    .reset_index(name="cohort_size")
)

cohort_table = cohort_table.merge(cohort_sizes, on="cohort_month", how="left")
cohort_table["retention_rate"] = cohort_table["active_users"] / cohort_table["cohort_size"]

fig_cohort = px.density_heatmap(
    cohort_table,
    x="activity_month",
    y="cohort_month",
    z="retention_rate",
    text_auto=".0%",
    title="Monthly Retention by Customer Cohort"
)
fig_cohort.update_layout(title_font_size=22, xaxis_title="Activity Month", yaxis_title="Cohort Month")
fig_cohort.update_xaxes(showgrid=False)
fig_cohort.update_yaxes(showgrid=False)
st.plotly_chart(fig_cohort, use_container_width=True)

# ---------------------------------------------------------
# Revenue + Channel Performance
# ---------------------------------------------------------
seg = (
    filtered.groupby("customer_segment")
    .agg(
        revenue=("revenue", "sum"),
        users=("customer_id", "nunique"),
        d7_retention=("d7_retained", "mean")
    )
    .reset_index()
)

fig_seg = px.bar(
    seg,
    x="customer_segment",
    y="revenue",
    text_auto=True,
    title="Revenue by Customer Segment"
)
fig_seg.update_layout(showlegend=False, title_font_size=22, xaxis_title=None, yaxis_title=None)
fig_seg.update_xaxes(showgrid=False)
fig_seg.update_yaxes(showgrid=False)

channel = (
    filtered.groupby("acquisition_channel")
    .agg(
        revenue=("revenue", "sum"),
        users=("customer_id", "nunique"),
        d7_retention=("d7_retained", "mean")
    )
    .reset_index()
)

fig_channel = px.scatter(
    channel,
    x="users",
    y="revenue",
    size="d7_retention",
    hover_name="acquisition_channel",
    title="Channel Value: Users vs Revenue"
)
fig_channel.update_layout(showlegend=False, title_font_size=22, xaxis_title="Users", yaxis_title="Revenue")
fig_channel.update_xaxes(showgrid=False)
fig_channel.update_yaxes(showgrid=False)

left2, right2 = st.columns(2)
left2.plotly_chart(fig_seg, use_container_width=True)
right2.plotly_chart(fig_channel, use_container_width=True)

# ---------------------------------------------------------
# Churn Risk
# ---------------------------------------------------------
risk = (
    filtered.groupby("churn_risk_category")
    .agg(
        customers=("customer_id", "nunique"),
        revenue=("revenue", "sum"),
        d7_retention=("d7_retained", "mean")
    )
    .reset_index()
)

fig_risk = px.bar(
    risk,
    x="churn_risk_category",
    y="customers",
    text_auto=True,
    title="Customers by Churn Risk Category"
)
fig_risk.update_layout(showlegend=False, title_font_size=22, xaxis_title=None, yaxis_title=None)
fig_risk.update_xaxes(showgrid=False)
fig_risk.update_yaxes(showgrid=False)
st.plotly_chart(fig_risk, use_container_width=True)

# ---------------------------------------------------------
# Business-Facing Segment Performance Table
# ---------------------------------------------------------
st.subheader("Customer Segment Performance Table")

segment_table = (
    filtered.groupby(["customer_segment", "acquisition_channel", "churn_risk_category"])
    .agg(
        customers=("customer_id", "nunique"),
        revenue=("revenue", "sum"),
        avg_revenue_per_customer=("revenue", "mean"),
        d1_retention=("d1_retained", "mean"),
        d7_retention=("d7_retained", "mean")
    )
    .reset_index()
)

segment_table["d1_retention"] = (segment_table["d1_retention"] * 100).round(1).astype(str) + "%"
segment_table["d7_retention"] = (segment_table["d7_retention"] * 100).round(1).astype(str) + "%"
segment_table["revenue"] = segment_table["revenue"].round(0)
segment_table["avg_revenue_per_customer"] = segment_table["avg_revenue_per_customer"].round(2)

st.dataframe(
    segment_table.sort_values(["revenue", "customers"], ascending=False),
    use_container_width=True
)

# ---------------------------------------------------------
# Experimentation Recommendation Layer
# ---------------------------------------------------------
st.subheader("Experiment Recommendation")

e1, e2, e3, e4 = st.columns(4)

e1.markdown("""
<div class="exp-card">
    <div class="exp-title">Hypothesis</div>
    <div class="exp-body">
        Reducing friction in the highest drop-off funnel stage will improve purchase conversion.
    </div>
</div>
""", unsafe_allow_html=True)

e2.markdown("""
<div class="exp-card">
    <div class="exp-title">Success Metric</div>
    <div class="exp-body">
        Purchase conversion rate from Awareness to Purchase.
    </div>
</div>
""", unsafe_allow_html=True)

e3.markdown("""
<div class="exp-card">
    <div class="exp-title">Guardrail Metric</div>
    <div class="exp-body">
        Revenue per customer and D7 retention must not decline after the change.
    </div>
</div>
""", unsafe_allow_html=True)

e4.markdown("""
<div class="exp-card">
    <div class="exp-title">Decision Rule</div>
    <div class="exp-body">
        Ship if conversion improves by at least 5% while revenue and retention remain stable.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Measurable Business Impact
# ---------------------------------------------------------
st.subheader("Measurable Business Impact")

st.markdown(f"""
- **Current conversion rate:** {overall_conversion:.1%}
- **Current D7 retention:** {d7:.1%}
- **Revenue per customer:** ${revenue_per_customer:,.2f}
- **High-risk customer share:** {high_risk_rate:.1%}

**Expected impact from recommended actions:**
- Improve purchase conversion by **5–10%** through funnel optimization.
- Improve D7 retention by **3–7%** through targeted lifecycle campaigns.
- Reduce high-risk customer concentration by **5–8%** through proactive retention actions.
- Protect revenue by prioritizing high-value segments before scaling acquisition spend.
""")
