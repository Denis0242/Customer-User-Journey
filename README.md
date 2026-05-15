# Customer User Journey Dashboard

![Dashboard Preview](screenshots/dashboard_preview.png)

## 1. Executive Summary

This project analyzes the customer product journey from **Awareness → Consideration → Intent → Checkout → Purchase**. It converts a Tableau-style product analytics dashboard into a complete recruiter-ready analytics repo with SQL, Python EDA, KPI definitions, Streamlit dashboard recreation, and executive decision support.

The dashboard helps leadership identify funnel drop-off, retention weakness, revenue contribution, and churn risk by segment, device, country, channel, and funnel stage.

## 2. Business Problem

Customers successfully move through early journey stages, but there is a visible drop-off at checkout and weaker D7 retention compared with D1 retention. This creates a product-growth problem because acquisition alone is not enough if users abandon before purchase or fail to return after the first week.

## 3. KPI Goals

- Total Users: **800**
- Conversion Rate: **25.00%**
- D1 Retention: **66.62%**
- D7 Retention: **36.62%**
- Revenue per User: **$25.58**
- Funnel Stage Volume
- Drop-off Rate by Stage
- Conversion by Channel
- Revenue by Segment
- Churn Risk Distribution

## 4. Dataset Overview

The dataset contains **2,240 rows** and **17 cleaned columns** representing customer journey events, funnel stages, retention behavior, revenue, acquisition channel, segment, country, device type, and churn risk category.

Key fields include `customer_id`, `journey_date`, `funnel_stage`, `funnel_stage_order`, `revenue`, `d1_retained`, `d7_retained`, `customer_segment`, `acquisition_channel`, and `churn_risk_category`.

## 5. Data Cleaning & EDA

Cleaning work included:

- Standardized column names to snake_case
- Converted `journey_date` into datetime format
- Converted revenue, retention flags, and funnel order fields into numeric types
- Checked missing values and duplicates
- Removed duplicate rows
- Validated funnel stage categories and stage ordering
- Validated retention flags as binary indicators
- Created `converted_flag`
- Created `revenue_user_flag`
- Created `retention_status`
- Created `revenue_band`
- Validated KPI calculations against dashboard-level metrics

## 6. SQL Transformations

The `sql/analysis_queries.sql` file includes queries for:

- Executive KPI summary
- Funnel volume by stage
- Drop-off analysis
- Retention trend
- Conversion by channel
- Revenue by segment
- Churn risk distribution
- Customer journey detail table

## 7. Metrics Engineering

```text
Total Users = COUNT(DISTINCT customer_id)
Conversion Rate = Purchase Users / Total Users
D1 Retention = D1 Retained Users / Total Users
D7 Retention = D7 Retained Users / Total Users
Revenue per User = Total Revenue / Total Users
Drop-off Rate = 1 - Next Stage Users / Current Stage Users
Converted Flag = 1 when funnel_stage = Purchase
```

## 8. Tableau Dashboard Preview

The dashboard shows funnel progression, drop-off analysis, retention trend, churn risk distribution, conversion by channel, revenue by segment, and an executive Insight → Action → Recommendation → Decision panel.

## 9. Streamlit Dashboard Recreation

The Streamlit app in `app/streamlit_app.py` recreates the dashboard with:

- Sidebar filters
- KPI cards
- Funnel chart
- Drop-off analysis
- Retention trend
- Churn risk distribution
- Conversion by channel
- Revenue by segment
- Customer detail table
- Executive decision summary

## 10. Product Insights

- Users progress strongly through early stages, but checkout creates a noticeable conversion bottleneck.
- D1 retention is stronger than D7 retention, showing that short-term engagement does not fully translate into long-term retention.
- Revenue is concentrated in higher-value customer segments.
- Risk category distribution helps prioritize users for targeted retention and conversion support.

## 11. Insight, Action, Recommendation, Decision

### Insight
Users successfully progress through early funnel stages, but checkout abandonment and weaker D7 retention create growth leakage.

### Action
Analyze checkout friction points, monitor D7 retention by segment, and identify users who are likely to drop before purchase.

### Recommendation
Optimize checkout experience, improve trust signals, reduce purchase friction, and launch targeted retention campaigns for early-stage users.

### Decision
Proceed with checkout-stage optimization before scaling acquisition spend, while prioritizing D7 retention improvements for sustainable user growth.

## 12. Business Impact

This project supports executive product decisions by connecting funnel behavior, retention, revenue, and risk into one analytics system. It helps reduce abandonment, improve conversion, protect revenue, and guide retention investment.

## Repo Architecture

```text
customer-user-journey-dashboard-repo/
├── data/
│   └── customer_user_journey.csv
├── sql/
│   ├── 01_funnel_analysis.sql
│   ├── 02_retention_analysis.sql
│   ├── 03_channel_segment_analysis.sql
│   └── 04_churn_risk_analysis.sql
├── notebooks/
│   └── eda.ipynb
├── dashboard/
│   └── tableau_dashboard_placeholder.md
├── screenshots/
│   └── customer_user_journey_dashboard.png
├── app/
│   ├── streamlit_app.py
│   ├── components.py
│   └── utils.py
├── docs/
│   ├── business_case.md
│   ├── dashboard_guide.md
│   └── kpi_definitions.md
├── requirements.txt
├── .gitignore
└── README.md
```



## 13. Future Improvements

- Add cohort retention analysis
- Add A/B testing layer for checkout experiments
- Add predictive churn model
- Connect to a live product database
- Automate refresh with scheduled SQL or Prefect

