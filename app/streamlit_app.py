import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Customer User Journey Dashboard", layout="wide")

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "user_journey_clean.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["journey_date"] = pd.to_datetime(df["journey_date"], errors="coerce")

    numeric_cols = [
        "funnel_stage_order", "revenue", "d1_retained", "d7_retained"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["customer_id", "journey_date"])
    return df


def pct(x):
    return f"{x:.1%}" if pd.notna(x) else "0.0%"


def money(x):
    return f"${x:,.0f}" if pd.notna(x) else "$0"


df = load_data()

# ---------------------------------------------------------
# Styling
# ---------------------------------------------------------
st.markdown("""
<style>
.block-container {padding-top: 1.5rem;}
.main-title {font-size:42px;font-weight:900;color:#111827;padding:8px 0 2px 0;}
.sub-title {font-size:18px;color:#4b5563;margin-bottom:20px;}
.metric-card {background:#f8fafc;border:1px solid #e5e7eb;border-radius:18px;padding:18px;box-shadow:0 1px 5px rgba(0,0,0,0.06);}
.metric-label {font-size:13px;color:#6b7280;font-weight:800;text-transform:uppercase;letter-spacing:.03em;}
.metric-value {font-size:28px;color:#111827;font-weight:900;margin-top:6px;}
.metric-note {font-size:12px;color:#6b7280;margin-top:4px;}
.insight {background:#e0f2fe;padding:16px;border-radius:14px;border-left:6px solid #0284c7;min-height:150px;}
.action {background:#fef9c3;padding:16px;border-radius:14px;border-left:6px solid #ca8a04;min-height:150px;}
.recommendation {background:#dcfce7;padding:16px;border-radius:14px;border-left:6px solid #16a34a;min-height:150px;}
.decision {background:#ffe4e6;padding:16px;border-radius:14px;border-left:6px solid #e11d48;min-height:150px;}
.exp-card {background:#f8fafc;border:1px solid #e5e7eb;border-radius:16px;padding:18px;min-height:145px;box-shadow:0 1px 4px rgba(0,0,0,0.05);}
.exp-title {font-weight:900;font-size:17px;color:#111827;margin-bottom:8px;}
.exp-body {font-size:15px;color:#374151;line-height:1.5;}
.small-caption {color:#6b7280;font-size:13px;margin-top:-10px;margin-bottom:10px;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.markdown('<div class="main-title">Customer User Journey Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Executive product analytics view of funnel conversion, retention, channel quality, churn risk, and revenue performance.</div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------------
with st.sidebar:
    st.header("Filters")

    segments = st.multiselect(
        "Customer Segment",
        sorted(df["customer_segment"].dropna().unique()),
        default=sorted(df["customer_segment"].dropna().unique()),
    )

    channels = st.multiselect(
        "Acquisition Channel",
        sorted(df["acquisition_channel"].dropna().unique()),
        default=sorted(df["acquisition_channel"].dropna().unique()),
    )

    risks = st.multiselect(
        "Churn Risk Category",
        sorted(df["churn_risk_category"].dropna().unique()),
        default=sorted(df["churn_risk_category"].dropna().unique()),
    )

    min_date = df["journey_date"].min().date()
    max_date = df["journey_date"].max().date()
    date_range = st.date_input("Journey Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
else:
    start_date, end_date = df["journey_date"].min(), df["journey_date"].max()

filtered = df[
    df["customer_segment"].isin(segments)
    & df["acquisition_channel"].isin(channels)
    & df["churn_risk_category"].isin(risks)
    & (df["journey_date"] >= start_date)
    & (df["journey_date"] <= end_date)
].copy()

if filtered.empty:
    st.warning("No records match the selected filters. Adjust the filters to view the dashboard.")
    st.stop()

# Customer-level table prevents retention/revenue distortion from repeated funnel rows.
customer_level = (
    filtered.sort_values("journey_date")
    .groupby("customer_id", as_index=False)
    .agg(
        first_date=("journey_date", "min"),
        customer_segment=("customer_segment", "first"),
        acquisition_channel=("acquisition_channel", "first"),
        churn_risk_category=("churn_risk_category", "first"),
        d1_retained=("d1_retained", "max"),
        d7_retained=("d7_retained", "max"),
        revenue=("revenue", "sum"),
    )
)

# ---------------------------------------------------------
# KPI Calculations
# ---------------------------------------------------------
awareness_users = filtered.loc[filtered["funnel_stage"].eq("Awareness"), "customer_id"].nunique()
purchase_users = filtered.loc[filtered["funnel_stage"].eq("Purchase"), "customer_id"].nunique()
overall_conversion = purchase_users / awareness_users if awareness_users else 0

customers = customer_level["customer_id"].nunique()
revenue = customer_level["revenue"].sum()
revenue_per_customer = revenue / customers if customers else 0
d1 = customer_level["d1_retained"].mean() if customers else 0
d7 = customer_level["d7_retained"].mean() if customers else 0
retention_gap = d1 - d7

high_risk_customers = customer_level.loc[
    customer_level["churn_risk_category"].str.lower().str.contains("high", na=False),
    "customer_id",
].nunique()
high_risk_rate = high_risk_customers / customers if customers else 0

# ---------------------------------------------------------
# KPI Cards
# ---------------------------------------------------------
c1, c2, c3, c4, c5 = st.columns(5)
cards = [
    ("Customers", f"{customers:,.0f}", "Unique customers"),
    ("Revenue", money(revenue), "Total attributed revenue"),
    ("Funnel Conversion", pct(overall_conversion), "Awareness → Purchase"),
    ("D7 Retention", pct(d7), f"D1 gap: {pct(retention_gap)}"),
    ("High-Risk Share", pct(high_risk_rate), f"{high_risk_customers:,.0f} customers"),
]

for col, (label, value, note) in zip([c1, c2, c3, c4, c5], cards):
    col.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# ---------------------------------------------------------
# Dynamic Executive Logic
# ---------------------------------------------------------
if overall_conversion < 0.25:
    insight_text = "The funnel is under-converting customers from awareness to purchase. The biggest issue is likely journey friction, not just acquisition volume."
    action_text = "Diagnose the largest funnel drop-off stage and review conversion by customer segment and channel."
    recommendation_text = "Run a focused activation or checkout improvement test before increasing acquisition spend."
    decision_text = "Fix funnel conversion first, then scale the strongest channels."
elif d7 < 0.35:
    insight_text = "D7 retention is weak, showing that customers are not returning strongly after early engagement."
    action_text = "Compare D1 vs D7 retention by segment and channel to identify where engagement drops fastest."
    recommendation_text = "Launch lifecycle messaging and onboarding improvements for low-retention groups."
    decision_text = "Prioritize retention before new growth investment."
elif high_risk_rate > 0.30:
    insight_text = "A meaningful share of customers are high churn risk, creating potential revenue leakage."
    action_text = "Segment high-risk customers by channel, revenue, and customer segment to identify preventable churn."
    recommendation_text = "Create targeted retention campaigns for high-risk, high-value customers."
    decision_text = "Protect existing revenue before scaling acquisition."
else:
    insight_text = "The journey shows healthy conversion, retention, and churn-risk signals."
    action_text = "Continue weekly monitoring of funnel conversion, channel quality, D7 retention, and high-risk share."
    recommendation_text = "Scale channels with strong revenue per customer and stable retention."
    decision_text = "Scale selectively with retention and revenue guardrails."

# ---------------------------------------------------------
# Visuals
# ---------------------------------------------------------
st.subheader("Product Analytics Dashboard Visuals")

# Funnel and stage conversion
funnel = (
    filtered.groupby(["funnel_stage_order", "funnel_stage"])["customer_id"]
    .nunique()
    .reset_index(name="users")
    .sort_values("funnel_stage_order")
)
funnel["stage_conversion"] = funnel["users"] / funnel["users"].shift(1)
funnel.loc[funnel.index[0], "stage_conversion"] = 1
funnel["dropoff_users"] = funnel["users"].shift(1) - funnel["users"]
funnel["dropoff_users"] = funnel["dropoff_users"].fillna(0).clip(lower=0)

fig_funnel = px.funnel(
    funnel,
    x="users",
    y="funnel_stage",
    title="Customer Journey Funnel",
    hover_data={"stage_conversion": ":.1%", "dropoff_users": ":,.0f"},
)
fig_funnel.update_traces(texttemplate="%{x:,.0f} customers")
fig_funnel.update_layout(showlegend=False, title_font_size=22, xaxis_title=None, yaxis_title=None)
fig_funnel.update_xaxes(showgrid=False)
fig_funnel.update_yaxes(showgrid=False)

fig_dropoff = px.bar(
    funnel.iloc[1:],
    x="funnel_stage",
    y="dropoff_users",
    text="dropoff_users",
    title="Where Customers Drop Off",
    hover_data={"stage_conversion": ":.1%"},
)
fig_dropoff.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
fig_dropoff.update_layout(title_font_size=22, xaxis_title=None, yaxis_title="Customers Lost")
fig_dropoff.update_xaxes(showgrid=False)
fig_dropoff.update_yaxes(showgrid=False)

left, right = st.columns(2)
left.plotly_chart(fig_funnel, use_container_width=True)
right.plotly_chart(fig_dropoff, use_container_width=True)

# Retention trend based on customer-level first date
retention_daily = (
    customer_level.groupby("first_date")
    .agg(
        customers=("customer_id", "nunique"),
        d1_retention=("d1_retained", "mean"),
        d7_retention=("d7_retained", "mean"),
    )
    .reset_index()
    .sort_values("first_date")
)

fig_ret = px.line(
    retention_daily,
    x="first_date",
    y=["d1_retention", "d7_retention"],
    title="Retention Trend by Customer Start Date",
)
fig_ret.update_layout(title_font_size=22, xaxis_title=None, yaxis_title="Retention Rate", legend_title_text="")
fig_ret.update_xaxes(showgrid=False)
fig_ret.update_yaxes(showgrid=False, tickformat=".0%")

# Proper cohort: month 0, month 1, month 2... not calendar month vs calendar month.
cohort_events = filtered[["customer_id", "journey_date"]].drop_duplicates().copy()
cohort_events["cohort_month"] = cohort_events.groupby("customer_id")["journey_date"].transform("min").dt.to_period("M")
cohort_events["activity_month"] = cohort_events["journey_date"].dt.to_period("M")
cohort_events["month_number"] = (
    (cohort_events["activity_month"].dt.year - cohort_events["cohort_month"].dt.year) * 12
    + (cohort_events["activity_month"].dt.month - cohort_events["cohort_month"].dt.month)
)
cohort_events = cohort_events[cohort_events["month_number"] >= 0]

cohort_counts = (
    cohort_events.groupby(["cohort_month", "month_number"])["customer_id"]
    .nunique()
    .reset_index(name="active_customers")
)
cohort_sizes = cohort_counts.loc[cohort_counts["month_number"].eq(0), ["cohort_month", "active_customers"]].rename(
    columns={"active_customers": "cohort_size"}
)
cohort_counts = cohort_counts.merge(cohort_sizes, on="cohort_month", how="left")
cohort_counts["retention_rate"] = cohort_counts["active_customers"] / cohort_counts["cohort_size"]
cohort_counts["cohort_month"] = cohort_counts["cohort_month"].astype(str)

cohort_matrix = cohort_counts.pivot(index="cohort_month", columns="month_number", values="retention_rate").sort_index()
text_matrix = cohort_matrix.apply(
    lambda col: col.map(lambda x: f"{x:.0%}" if pd.notna(x) else "")
)

fig_cohort = go.Figure(
    data=go.Heatmap(
        z=cohort_matrix.values,
        x=[f"Month {int(c)}" for c in cohort_matrix.columns],
        y=cohort_matrix.index,
        text=text_matrix.values,
        texttemplate="%{text}",
        hovertemplate="Cohort: %{y}<br>Period: %{x}<br>Retention: %{z:.1%}<extra></extra>",
        colorbar=dict(title="Retention"),
        zmin=0,
        zmax=1,
    )
)
fig_cohort.update_layout(
    title="Retention by Customer Cohort — Month 0, Month 1, Month 2",
    title_font_size=22,
    xaxis_title="Months Since First Activity",
    yaxis_title="Customer Cohort Month",
)

left2, right2 = st.columns([1, 1])
left2.plotly_chart(fig_ret, use_container_width=True)
right2.plotly_chart(fig_cohort, use_container_width=True)

st.markdown(
    '<div class="small-caption">Cohort view is now calculated correctly: each customer is assigned to their first activity month, then retention is measured by months since that first activity.</div>',
    unsafe_allow_html=True,
)

# Revenue, channel quality, segment performance
seg = (
    customer_level.groupby("customer_segment")
    .agg(customers=("customer_id", "nunique"), revenue=("revenue", "sum"), d7_retention=("d7_retained", "mean"))
    .reset_index()
)
seg["revenue_per_customer"] = seg["revenue"] / seg["customers"]

fig_seg = px.bar(
    seg.sort_values("revenue", ascending=False),
    x="customer_segment",
    y="revenue",
    text="revenue",
    title="Revenue by Customer Segment",
    hover_data={"customers": ":,.0f", "revenue_per_customer": ":$,.2f", "d7_retention": ":.1%"},
)
fig_seg.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
fig_seg.update_layout(showlegend=False, title_font_size=22, xaxis_title=None, yaxis_title="Revenue")
fig_seg.update_xaxes(showgrid=False)
fig_seg.update_yaxes(showgrid=False)

channel = (
    customer_level.groupby("acquisition_channel")
    .agg(customers=("customer_id", "nunique"), revenue=("revenue", "sum"), d7_retention=("d7_retained", "mean"))
    .reset_index()
)
channel["revenue_per_customer"] = channel["revenue"] / channel["customers"]
channel["channel_quality_score"] = channel["revenue_per_customer"] * channel["d7_retention"]

fig_channel = px.bar(
    channel.sort_values("revenue_per_customer", ascending=False),
    x="acquisition_channel",
    y="revenue_per_customer",
    text="revenue_per_customer",
    title="Channel Quality: Revenue per Customer",
    hover_data={"customers": ":,.0f", "revenue": ":$,.0f", "d7_retention": ":.1%", "channel_quality_score": ":$,.2f"},
)
fig_channel.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
fig_channel.update_layout(showlegend=False, title_font_size=22, xaxis_title=None, yaxis_title="Revenue per Customer")
fig_channel.update_xaxes(showgrid=False)
fig_channel.update_yaxes(showgrid=False)

left3, right3 = st.columns(2)
left3.plotly_chart(fig_seg, use_container_width=True)
right3.plotly_chart(fig_channel, use_container_width=True)

# Additional visual 1: retention by segment
retention_segment = (
    customer_level.groupby("customer_segment")
    .agg(d1_retention=("d1_retained", "mean"), d7_retention=("d7_retained", "mean"), customers=("customer_id", "nunique"))
    .reset_index()
)
retention_long = retention_segment.melt(
    id_vars=["customer_segment", "customers"],
    value_vars=["d1_retention", "d7_retention"],
    var_name="metric",
    value_name="retention_rate",
)
retention_long["metric"] = retention_long["metric"].replace({"d1_retention": "D1 Retention", "d7_retention": "D7 Retention"})

fig_ret_segment = px.bar(
    retention_long,
    x="customer_segment",
    y="retention_rate",
    color="metric",
    barmode="group",
    text="retention_rate",
    title="D1 vs D7 Retention by Customer Segment",
    hover_data={"customers": ":,.0f"},
)
fig_ret_segment.update_traces(texttemplate="%{text:.0%}", textposition="outside")
fig_ret_segment.update_layout(title_font_size=22, xaxis_title=None, yaxis_title="Retention Rate", legend_title_text="")
fig_ret_segment.update_yaxes(tickformat=".0%", range=[0, 1])
fig_ret_segment.update_xaxes(showgrid=False)

# Additional visual 2: churn risk revenue exposure
risk = (
    customer_level.groupby("churn_risk_category")
    .agg(customers=("customer_id", "nunique"), revenue=("revenue", "sum"), d7_retention=("d7_retained", "mean"))
    .reset_index()
)
risk["revenue_per_customer"] = risk["revenue"] / risk["customers"]

fig_risk = px.bar(
    risk.sort_values("revenue", ascending=False),
    x="churn_risk_category",
    y="revenue",
    text="revenue",
    title="Revenue Exposure by Churn Risk Category",
    hover_data={"customers": ":,.0f", "revenue_per_customer": ":$,.2f", "d7_retention": ":.1%"},
)
fig_risk.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
fig_risk.update_layout(showlegend=False, title_font_size=22, xaxis_title=None, yaxis_title="Revenue at Risk")
fig_risk.update_xaxes(showgrid=False)
fig_risk.update_yaxes(showgrid=False)

left4, right4 = st.columns(2)
left4.plotly_chart(fig_ret_segment, use_container_width=True)
right4.plotly_chart(fig_risk, use_container_width=True)

st.divider()

# ---------------------------------------------------------
# Tables
# ---------------------------------------------------------
st.subheader("Channel and Segment Performance Tables")

t1, t2 = st.tabs(["Channel Scorecard", "Segment Detail"])

with t1:
    channel_table = channel.copy()
    channel_table["revenue"] = channel_table["revenue"].round(0)
    channel_table["revenue_per_customer"] = channel_table["revenue_per_customer"].round(2)
    channel_table["d7_retention"] = (channel_table["d7_retention"] * 100).round(1).astype(str) + "%"
    channel_table["channel_quality_score"] = channel_table["channel_quality_score"].round(2)
    st.dataframe(
        channel_table.sort_values("channel_quality_score", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

with t2:
    segment_table = (
        customer_level.groupby(["customer_segment", "acquisition_channel", "churn_risk_category"])
        .agg(
            customers=("customer_id", "nunique"),
            revenue=("revenue", "sum"),
            avg_revenue_per_customer=("revenue", "mean"),
            d1_retention=("d1_retained", "mean"),
            d7_retention=("d7_retained", "mean"),
        )
        .reset_index()
    )
    segment_table["d1_retention"] = (segment_table["d1_retention"] * 100).round(1).astype(str) + "%"
    segment_table["d7_retention"] = (segment_table["d7_retention"] * 100).round(1).astype(str) + "%"
    segment_table["revenue"] = segment_table["revenue"].round(0)
    segment_table["avg_revenue_per_customer"] = segment_table["avg_revenue_per_customer"].round(2)
    st.dataframe(
        segment_table.sort_values(["revenue", "customers"], ascending=False),
        use_container_width=True,
        hide_index=True,
    )

st.divider()

# ---------------------------------------------------------
# Experiment Recommendation Layer
# ---------------------------------------------------------
st.subheader("Experiment Recommendation")

e1, e2, e3, e4 = st.columns(4)
e1.markdown("""
<div class="exp-card"><div class="exp-title">Hypothesis</div><div class="exp-body">
Reducing friction in the largest drop-off stage will increase purchase conversion.</div></div>
""", unsafe_allow_html=True)
e2.markdown("""
<div class="exp-card"><div class="exp-title">Success Metric</div><div class="exp-body">
Awareness-to-purchase conversion rate, measured at the customer level.</div></div>
""", unsafe_allow_html=True)
e3.markdown("""
<div class="exp-card"><div class="exp-title">Guardrail Metric</div><div class="exp-body">
D7 retention and revenue per customer must remain stable.</div></div>
""", unsafe_allow_html=True)
e4.markdown("""
<div class="exp-card"><div class="exp-title">Decision Rule</div><div class="exp-body">
Ship if conversion improves 5%+ without hurting D7 retention or revenue quality.</div></div>
""", unsafe_allow_html=True)

st.divider()

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
- Reduce high-risk concentration by **5–8%** through proactive retention actions.
- Protect revenue by prioritizing high-value segments and high-quality acquisition channels.
""")

st.divider()

# ---------------------------------------------------------
# Executive Decision Summary
# ---------------------------------------------------------
st.subheader("Executive Decision Summary")
i1, i2, i3, i4 = st.columns(4)
i1.markdown(f"<div class='insight'><b>Insight</b><br>{insight_text}</div>", unsafe_allow_html=True)
i2.markdown(f"<div class='action'><b>Action</b><br>{action_text}</div>", unsafe_allow_html=True)
i3.markdown(f"<div class='recommendation'><b>Recommendation</b><br>{recommendation_text}</div>", unsafe_allow_html=True)
i4.markdown(f"<div class='decision'><b>Decision</b><br>{decision_text}</div>", unsafe_allow_html=True)
