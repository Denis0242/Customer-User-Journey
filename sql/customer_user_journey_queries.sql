-- Customer User Journey Analytics SQL
-- Purpose: representative SQL queries that match the dashboard KPIs.

-- 1. Funnel conversion and drop-off by journey stage
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

-- 2. Retention and revenue by customer segment
SELECT
    customer_segment,
    COUNT(DISTINCT customer_id) AS users,
    SUM(revenue) AS total_revenue,
    ROUND(AVG(d1_retained), 3) AS d1_retention_rate,
    ROUND(AVG(d7_retained), 3) AS d7_retention_rate
FROM user_journey
GROUP BY customer_segment
ORDER BY total_revenue DESC;

-- 3. Channel performance for acquisition decisions
SELECT
    acquisition_channel,
    COUNT(DISTINCT customer_id) AS acquired_users,
    SUM(revenue) AS total_revenue,
    ROUND(SUM(revenue) * 1.0 / COUNT(DISTINCT customer_id), 2) AS revenue_per_user,
    ROUND(AVG(d7_retained), 3) AS d7_retention_rate
FROM user_journey
GROUP BY acquisition_channel
ORDER BY revenue_per_user DESC;

-- 4. Churn risk decision signal
SELECT
    churn_risk_category,
    COUNT(DISTINCT customer_id) AS customers,
    SUM(revenue) AS revenue_exposure,
    ROUND(AVG(d1_retained), 3) AS d1_retention_rate,
    ROUND(AVG(d7_retained), 3) AS d7_retention_rate
FROM user_journey
GROUP BY churn_risk_category
ORDER BY revenue_exposure DESC;
