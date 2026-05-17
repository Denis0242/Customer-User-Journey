# Customer User Journey Analytics Dashboard

## Executive Summary

This project analyzes customer journey behavior to help product, growth, and leadership teams improve funnel conversion, retention, and revenue outcomes.

The dashboard evaluates funnel stage movement, D1/D7 retention, churn risk, acquisition channels, customer segments, and revenue performance to identify where users drop off and which groups create the strongest business value.

Insights from this analysis support decisions around funnel optimization, retention monitoring, acquisition investment, and churn-risk prioritization.

Expected impact includes improving funnel conversion by **5–10%**, increasing D7 retention by **3–7%**, and helping teams prioritize customer segments and channels with stronger revenue-per-user potential.

Built using **Tableau-style analytics, SQL, Python, Streamlit, and EDA**.

---

## Business Problem

Product and growth teams need to understand where customers drop off across the journey and which segments, devices, channels, and churn-risk groups are most important for business performance.

This project answers:

- Where are users dropping off in the funnel?
- Which customer segments generate the most revenue?
- Which acquisition channels produce the strongest retention?
- Which churn-risk groups require action?
- What decision should leadership make to improve product health?

---

## KPI Goals

| KPI | Business Purpose |
|---|---|
| Funnel Conversion Rate | Measures movement from awareness to purchase |
| Drop-Off Rate | Identifies journey friction points |
| D1 Retention | Measures immediate product stickiness |
| D7 Retention | Measures short-term customer value |
| Revenue | Measures monetization performance |
| Revenue Per User | Compares channel and segment value |
| Churn Risk Category | Prioritizes retention actions |

---

## Dataset Overview

| Item | Value |
|---|---:|
| Dataset | `user_realistic.csv` |
| Rows | 2,240 |
| Columns | 16 |
| Unique Customers | 800 |
| Date Range | 2024-01-01 to 2024-02-29 |
| Total Revenue | $20,467 |
| D1 Retention | 74.0% |
| D7 Retention | 45.8% |
| Overall Funnel Conversion | 25.0% |

---

## EDA + Cleaning + Feature Engineering

The EDA workflow is documented in:

```text
notebooks/EDA_CLEANING_FEATURE_ENGINEERING.md
notebooks/eda_cleaning_feature_engineering.ipynb
```

Cleaning steps include:

1. Loaded customer journey data
2. Standardized column names
3. Converted journey date to datetime
4. Checked missing values
5. Removed duplicates
6. Validated funnel stage order
7. Validated retention flags
8. Engineered conversion flag
9. Engineered retention gap
10. Created revenue band
11. Exported final clean dataset

---

## Representative SQL Queries

SQL file:

```text
sql/customer_user_journey_queries.sql
```

### 1. Funnel Conversion and Drop-Off

```sql
SELECT
    funnel_stage_order,
    funnel_stage,
    COUNT(DISTINCT customer_id) AS users,
    ROUND(
        COUNT(DISTINCT customer_id) * 1.0 /
        LAG(COUNT(DISTINCT customer_id)) OVER (ORDER BY funnel_stage_order),
        3
    ) AS conversion_from_previous
FROM user_journey
GROUP BY funnel_stage_order, funnel_stage
ORDER BY funnel_stage_order;
```

### 2. Retention and Revenue by Segment

```sql
SELECT
    customer_segment,
    COUNT(DISTINCT customer_id) AS users,
    SUM(revenue) AS total_revenue,
    ROUND(AVG(d1_retained), 3) AS d1_retention_rate,
    ROUND(AVG(d7_retained), 3) AS d7_retention_rate
FROM user_journey
GROUP BY customer_segment
ORDER BY total_revenue DESC;
```

### 3. Acquisition Channel Performance

```sql
SELECT
    acquisition_channel,
    COUNT(DISTINCT customer_id) AS acquired_users,
    SUM(revenue) AS total_revenue,
    ROUND(SUM(revenue) * 1.0 / COUNT(DISTINCT customer_id), 2) AS revenue_per_user,
    ROUND(AVG(d7_retained), 3) AS d7_retention_rate
FROM user_journey
GROUP BY acquisition_channel
ORDER BY revenue_per_user DESC;
```

### 4. Churn Risk Decision Signal

```sql
SELECT
    churn_risk_category,
    COUNT(DISTINCT customer_id) AS customers,
    SUM(revenue) AS revenue_exposure,
    ROUND(AVG(d1_retained), 3) AS d1_retention_rate,
    ROUND(AVG(d7_retained), 3) AS d7_retention_rate
FROM user_journey
GROUP BY churn_risk_category
ORDER BY revenue_exposure DESC;
```

---

## Metrics Engineering

| Metric | Formula |
|---|---|
| Overall Conversion | Purchase Users / Awareness Users |
| Stage Conversion | Current Stage Users / Previous Stage Users |
| Drop-Off Rate | 1 - Stage Conversion |
| D1 Retention | D1 Retained Users / Total Records |
| D7 Retention | D7 Retained Users / Total Records |
| Revenue Per User | Total Revenue / Unique Customers |
| Retention Gap | D1 Retention - D7 Retention |

---

## Analytics Workflow

```text
Business Problem
        ↓
EDA + Cleaning
        ↓
Feature Engineering
        ↓
SQL Transformations
        ↓
Metrics Engineering
        ↓
Dashboard Build
        ↓
Insights
        ↓
Decision Support
        ↓
Business Impact
```

---

## Dashboard Preview

Dashboard screenshot files are included in:

```text
screenshots/
├── dashboard_preview.png
├── kpi_overview.png
├── funnel_view.png
└── segment_channel_view.png
```

---

## Product Insights

### Insight 1 — Funnel Drop-Off
The journey starts with **800 awareness users** and ends with **200 purchase users**, producing an overall funnel conversion rate of **25.0%**.

### Insight 2 — Retention Gap
D1 retention is **74.0%**, while D7 retention drops to **45.8%**, showing a short-term retention gap that should be monitored.

### Insight 3 — Segment Value
Customer segments show different revenue and retention patterns, making segmentation important for acquisition and retention decisions.

### Insight 4 — Risk Prioritization
Churn-risk groups should be monitored because revenue exposure and D7 retention vary across risk categories.

---

## Insight → Action → Recommendation → Decision

### Insight
Customers are moving through the funnel, but the largest business issue is the drop from awareness to purchase and the gap between D1 and D7 retention.

### Action
Monitor funnel stage conversion, D7 retention, revenue per user, and churn-risk category weekly.

### Recommendation
Prioritize product improvements around the highest drop-off funnel stages and create retention campaigns for medium/high churn-risk users.

### Decision
**Improve and Monitor** — continue product optimization before scaling acquisition aggressively.

---

## Decision Framework

| Decision | Rule |
|---|---|
| Ship / Scale | Strong conversion + healthy retention |
| Improve | Funnel drop-off exists but revenue signal is positive |
| Monitor | Mixed performance or unstable retention |
| Review | High churn risk or weak conversion |
| Do Not Scale | Weak funnel performance + poor retention |

---

## Measurable Business Impact

This project could help the business:

- Improve funnel conversion by **5–10%** through drop-off identification
- Increase D7 retention by **3–7%** through targeted retention actions
- Improve revenue per user by prioritizing stronger channels and segments
- Reduce churn-risk exposure by focusing on high-risk customer groups
- Shorten decision-making time by giving leadership one dashboard for product health

---

## Streamlit App

Run locally:

```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

---

## Repo Architecture

```text
customer-user-journey/
├── data/
│   ├── user_realistic.csv
│   ├── user_journey_clean.csv
│   ├── funnel_summary.csv
│   ├── segment_summary.csv
│   └── risk_summary.csv
├── sql/
│   └── customer_user_journey_queries.sql
├── notebooks/
│   ├── EDA_CLEANING_FEATURE_ENGINEERING.md
│   └── eda_cleaning_feature_engineering.ipynb
├── dashboard/
│   └── dashboard_notes.md
├── screenshots/
│   ├── dashboard_preview.png
│   ├── kpi_overview.png
│   ├── funnel_view.png
│   └── segment_channel_view.png
├── app/
│   └── streamlit_app.py
├── docs/
│   └── business_decision_summary.md
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Automation Awareness

Future automation options:

- Schedule SQL refreshes for weekly KPI monitoring
- Add Python data validation checks
- Use Prefect for automated data pipeline orchestration
- Connect dashboard to Snowflake, Redshift, or PostgreSQL
- Deploy Streamlit app for recruiter and stakeholder review

---

## Future Improvements

- Add cohort retention analysis
- Add A/B testing readout for funnel changes
- Add predictive churn model
- Add live database connection
- Add Tableau packaged workbook when available

---

## Final Positioning

This repository demonstrates that I can clean data, analyze KPIs, write SQL, build dashboards, recreate analytics in Streamlit, explain insights, recommend actions, and support business/product decisions.
