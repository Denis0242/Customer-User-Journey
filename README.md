# Customer User Journey Analytics Dashboard

![Dashboard Preview](screenshots/dashboard_preview.png)

# Executive Summary

This project analyzes customer behavior across the full user journey to help product, growth, and leadership teams improve conversion, retention, and revenue outcomes.

The analysis evaluates customer funnel progression, acquisition channels, customer segments, retention performance, churn-risk behavior, and revenue contribution to identify where customers drop off, which groups create the strongest business value, and what actions should be prioritized to improve product health.

The dashboard supports product analytics and business decision-making by helping stakeholders:

* Identify high-friction funnel stages
* Improve customer retention performance
* Prioritize higher-value acquisition channels
* Reduce churn-risk exposure
* Optimize customer segments with stronger revenue potential

Expected business value includes:

* 5–10% improvement in funnel conversion
* 3–7% increase in customer retention
* Improved revenue-per-user optimization
* Reduced churn-risk exposure
* Faster data-driven decision-making

This repository demonstrates end-to-end analytics capability through SQL, Python, Tableau-style analytics, Streamlit, KPI engineering, and business-focused product analytics.

---

# Business Problem

Product and growth teams often struggle to understand:

* Where customers drop off throughout the journey
* Which customer segments create the most value
* Which acquisition channels drive stronger retention
* Which customers present the highest churn risk
* Which actions should be prioritized to improve product performance

Without visibility into the customer journey, organizations risk:

* Losing customers during funnel progression
* Investing in low-performing acquisition channels
* Missing retention opportunities
* Increasing churn exposure
* Making slower business decisions

---

# Decision Support Use Case

This dashboard helps product, growth, and business stakeholders analyze customer behavior across key touchpoints, identify conversion bottlenecks, evaluate engagement patterns, and support decisions that improve customer experience, conversion performance, retention, and revenue outcomes.

---

# KPIs

| KPI                             | Business Purpose                             |
| ------------------------------- | -------------------------------------------- |
| Funnel Conversion Rate          | Measures movement from awareness to purchase |
| Stage Drop-Off Rate             | Identifies customer journey friction         |
| D1 Retention                    | Measures immediate product stickiness        |
| D7 Retention                    | Measures short-term customer value           |
| Revenue                         | Measures monetization performance            |
| Revenue Per User (RPU)          | Measures customer value                      |
| Customer Segment Performance    | Identifies high-value customer groups        |
| Churn Risk Category             | Prioritizes retention intervention           |
| Acquisition Channel Performance | Evaluates channel effectiveness              |

---

# Dashboard Overview

The dashboard provides a comprehensive view of customer journey performance across acquisition, conversion, retention, revenue, and churn-risk monitoring.

Core reporting areas include:

* Funnel Conversion Analysis
* Customer Retention Monitoring
* Revenue Performance Tracking
* Customer Segment Analysis
* Acquisition Channel Performance
* Churn-Risk Prioritization

The dashboard supports product, growth, and leadership teams by providing visibility into customer behavior and business performance.

---

# Dashboard Screenshots

## Main Dashboard

![Customer User Journey Dashboard](screenshots/dashboard_preview.png)

## KPI Overview

![KPI Overview](screenshots/kpi_overview.png)

## Funnel Performance View

![Funnel View](screenshots/funnel_view.png)

## Segment & Channel Analysis

![Segment Channel View](screenshots/segment_channel_view.png)

---

# Key Insight

The largest business opportunity exists between the Awareness and Purchase stages, where customer drop-off significantly reduces overall funnel conversion and contributes to weaker downstream retention performance.

Additionally, the gap between D1 Retention (74.0%) and D7 Retention (45.8%) suggests opportunities to improve early customer engagement and long-term product adoption.

---

# Business Impact

This dashboard helps organizations:

* Improve funnel conversion by an estimated 5–10%
* Increase customer retention by an estimated 3–7%
* Improve revenue-per-user through stronger channel prioritization
* Reduce churn-risk exposure through earlier intervention
* Improve decision-making through centralized KPI monitoring
* Support product optimization efforts using customer journey insights

---

# Recommendation

Prioritize improvements at the highest drop-off funnel stages and implement targeted retention initiatives for medium- and high-risk customer groups to improve conversion, retention, and overall customer value.

---

# Data Dictionary

| Field               | Description                   |
| ------------------- | ----------------------------- |
| customer_id         | Unique customer identifier    |
| customer_segment    | Customer classification group |
| acquisition_channel | Customer acquisition source   |
| funnel_stage        | Customer journey stage        |
| d1_retained         | Day 1 retention indicator     |
| d7_retained         | Day 7 retention indicator     |
| revenue             | Revenue generated             |
| churn_risk_category | Customer churn classification |
| device_type         | Customer device type          |
| signup_date         | Customer registration date    |

---

# Representative SQL Queries

SQL queries used for KPI calculations and business analysis are included in:

```text
sql/customer_user_journey_queries.sql
```

### Funnel Conversion Analysis

```sql
SELECT
    funnel_stage_order,
    funnel_stage,
    COUNT(DISTINCT customer_id) AS users
FROM user_journey
GROUP BY funnel_stage_order, funnel_stage
ORDER BY funnel_stage_order;
```

### Customer Segment Performance

```sql
SELECT
    customer_segment,
    SUM(revenue) AS total_revenue,
    AVG(d7_retained) AS d7_retention_rate
FROM user_journey
GROUP BY customer_segment;
```

### Acquisition Channel Performance

```sql
SELECT
    acquisition_channel,
    SUM(revenue) AS total_revenue,
    AVG(d7_retained) AS d7_retention_rate
FROM user_journey
GROUP BY acquisition_channel;
```

---

# Metrics Engineering

| Metric             | Formula                                    |
| ------------------ | ------------------------------------------ |
| Overall Conversion | Purchase Users / Awareness Users           |
| Stage Conversion   | Current Stage Users / Previous Stage Users |
| Drop-Off Rate      | 1 − Stage Conversion                       |
| D1 Retention       | D1 Retained Users / Total Users            |
| D7 Retention       | D7 Retained Users / Total Users            |
| Revenue Per User   | Total Revenue / Unique Customers           |
| Retention Gap      | D1 Retention − D7 Retention                |

This project emphasizes:

* Funnel analytics
* Retention monitoring
* Revenue optimization
* Customer segmentation
* Churn-risk prioritization
* Product health measurement

---

# Executive Decision Summary

### Insight

The largest business opportunity exists between Awareness and Purchase stages, where funnel drop-off and retention decline reduce customer value and overall product performance.

### Action

Monitor funnel conversion, D7 retention, revenue-per-user, and churn-risk indicators on a recurring basis.

### Recommendation

Improve customer onboarding, optimize high-friction funnel stages, and strengthen retention initiatives for at-risk customers.

### Decision

Improve and monitor product performance before aggressively scaling acquisition investment.

---

# Tools Used

* SQL
* Python
* Pandas
* Tableau
* Streamlit
* GitHub

---

# Repository Structure

```text
customer-user-journey/
├── data/
├── sql/
├── notebooks/
├── screenshots/
├── app/
├── docs/
├── requirements.txt
├── README.md
└── .gitignore
```

---

# How to Run the Project

```bash
git clone <repository-url>

pip install -r requirements.txt

streamlit run app/streamlit_app.py
```

---

# Future Improvements

* Add cohort retention analysis
* Add A/B testing readouts
* Add predictive churn modeling
* Add live database integration
* Add automated reporting workflows

---

# Disclaimer

* Dataset is synthetic and created for portfolio purposes.
* No real customer information is included.
* Project developed for educational and demonstration purposes.
* Business impact estimates are illustrative and intended to demonstrate analytical decision-making.


------------------------------------------------------------
=====================================================================
