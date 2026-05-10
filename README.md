
# Customer User Journey Analytics Platform

## Executive Summary

This project presents a complete Product Analytics and Customer Journey Intelligence platform designed to monitor user behavior, retention, funnel conversion, revenue performance, and churn risk across a digital product ecosystem.

The dashboard simulates how product and business teams use analytics to improve:
- Funnel conversion
- Customer retention
- Revenue optimization
- User engagement
- Product growth decisions

This repository demonstrates:
- Product Analytics thinking
- Funnel & Retention Analysis
- KPI Monitoring
- Experimentation Readiness
- Executive Decision Support
- Modern Analytics Workflow maturity

---

# Business Problem

A digital commerce platform needed visibility into:
- User journey drop-offs
- Funnel abandonment
- Low D7 retention
- Revenue performance by segment
- Churn risk distribution
- Channel conversion efficiency

The company wanted a centralized analytics solution to:
1. Identify friction points in the user journey
2. Improve conversion rates
3. Increase long-term retention
4. Reduce churn risk
5. Optimize acquisition channels
6. Improve revenue generation

---

# KPI Goals

| KPI | Goal |
|---|---|
| Conversion Rate | Increase purchase completion |
| D1 Retention | Improve onboarding engagement |
| D7 Retention | Improve long-term retention |
| Revenue Per User | Increase monetization |
| Funnel Drop-off | Reduce abandonment |
| Churn Risk | Reduce high-risk users |

---

# Dataset

The dataset contains:
- User journey stages
- Device segmentation
- Country segmentation
- Customer segments
- Retention metrics
- Revenue metrics
- Risk categories
- Funnel activity

---

# SQL Transformations

The project includes SQL workflows for:
- Funnel conversion calculations
- Retention analysis
- Revenue segmentation
- Churn risk distribution
- Channel conversion analysis
- KPI aggregation

---

# Metrics Engineering

Metrics engineered:
- Conversion Rate
- D1 Retention
- D7 Retention
- Revenue Per User
- Funnel Drop-off %
- Risk Distribution %
- Segment Revenue Contribution

---

# Analytics Workflow

```text
Raw Data
   ↓
SQL Cleaning & Aggregation
   ↓
Metrics Engineering
   ↓
Exploratory Analysis
   ↓
Dashboard Visualization
   ↓
Insights & Recommendations
   ↓
Decision Support
```

---

# Dashboard Preview

Dashboard Components:
- Funnel Chart
- Drop-off Analysis
- Retention Trend
- Churn Risk Distribution
- Conversion by Channel
- Revenue by Segment
- KPI Scorecards
- Executive Insight Panel

---

# Product Insights

## Insight 1
Users successfully move through the early funnel stages but there is noticeable drop-off between Checkout and Purchase.

## Insight 2
D1 retention remains strong while D7 retention shows long-term engagement decline.

## Insight 3
Certain acquisition channels outperform others in conversion efficiency.

## Insight 4
High-risk users represent a significant percentage of the customer base.

---

# Experimentation Thinking

Potential A/B Tests:
1. Checkout UX redesign
2. Incentive optimization
3. Personalized onboarding
4. Email retention campaigns
5. Pricing strategy experiments

Primary Metrics:
- Conversion Rate
- Checkout Completion
- D7 Retention
- Revenue Per User

Guardrail Metrics:
- Bounce Rate
- Refund Rate
- Churn Rate

---

# Recommendations

1. Optimize checkout flow to reduce abandonment
2. Improve onboarding experience
3. Launch retention-focused campaigns
4. Personalize engagement for high-risk users
5. Invest more heavily in high-converting channels

---

# Decision Framework

| Observation | Decision |
|---|---|
| Checkout abandonment is high | Prioritize checkout optimization |
| D7 retention is weak | Improve long-term engagement strategy |
| Certain channels outperform | Scale top-performing channels |
| High-risk users increasing | Launch churn mitigation programs |

---

# Business Impact

Potential business outcomes:
- Increased conversion rate
- Improved retention
- Reduced churn
- Higher revenue per user
- Improved product adoption
- Better acquisition efficiency

---

# Streamlit App

The Streamlit app provides:
- Interactive KPI monitoring
- Dynamic filtering
- Funnel analysis
- Retention visualization
- Revenue segmentation
- Executive reporting

Run locally:

```bash
streamlit run app/streamlit_app.py
```

---

# Repo Architecture

```text
customer-user-journey-analytics-platform/
│
├── data/
├── sql/
├── notebooks/
├── dashboard/
├── screenshots/
├── app/
├── docs/
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Automation Awareness

This repository follows a modern analytics workflow:
- SQL transformations
- KPI engineering
- Dashboard automation
- Reusable analytics pipelines
- Streamlit deployment readiness

---

# Future Improvements

Future upgrades may include:
- Predictive churn modeling
- Real-time KPI pipelines
- A/B testing framework integration
- ML-powered customer segmentation
- Recommendation systems
- Cloud deployment

