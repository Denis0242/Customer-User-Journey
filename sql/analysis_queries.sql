-- Customer User Journey Dashboard SQL

-- 1. Executive KPI Summary
SELECT
    COUNT(DISTINCT customer_id) AS total_users,
    COUNT(DISTINCT CASE WHEN LOWER(funnel_stage) = 'purchase' THEN customer_id END) * 1.0 / COUNT(DISTINCT customer_id) AS conversion_rate,
    AVG(d1_retained) AS d1_retention,
    AVG(d7_retained) AS d7_retention,
    SUM(revenue) * 1.0 / COUNT(DISTINCT customer_id) AS revenue_per_user
FROM cleaned_user_journey;

-- 2. Funnel Stage Volume
SELECT
    funnel_stage_order,
    funnel_stage,
    COUNT(DISTINCT customer_id) AS users
FROM cleaned_user_journey
GROUP BY funnel_stage_order, funnel_stage
ORDER BY funnel_stage_order;

-- 3. Drop-off Analysis
WITH stage_counts AS (
    SELECT funnel_stage_order, funnel_stage, COUNT(DISTINCT customer_id) AS users
    FROM cleaned_user_journey
    GROUP BY funnel_stage_order, funnel_stage
), next_stage AS (
    SELECT
        funnel_stage_order,
        funnel_stage,
        users,
        LEAD(users) OVER (ORDER BY funnel_stage_order) AS next_stage_users
    FROM stage_counts
)
SELECT
    funnel_stage,
    users,
    next_stage_users,
    1 - (next_stage_users * 1.0 / users) AS dropoff_rate
FROM next_stage
WHERE next_stage_users IS NOT NULL;

-- 4. Retention Trend
SELECT
    journey_date,
    AVG(d1_retained) AS d1_retention,
    AVG(d7_retained) AS d7_retention
FROM cleaned_user_journey
GROUP BY journey_date
ORDER BY journey_date;

-- 5. Conversion by Channel
SELECT
    acquisition_channel,
    COUNT(DISTINCT CASE WHEN LOWER(funnel_stage) = 'purchase' THEN customer_id END) * 1.0 / COUNT(DISTINCT customer_id) AS conversion_rate
FROM cleaned_user_journey
GROUP BY acquisition_channel
ORDER BY conversion_rate DESC;

-- 6. Revenue by Segment
SELECT
    customer_segment,
    SUM(revenue) AS total_revenue,
    SUM(revenue) * 1.0 / COUNT(DISTINCT customer_id) AS revenue_per_user
FROM cleaned_user_journey
GROUP BY customer_segment
ORDER BY total_revenue DESC;

-- 7. Churn Risk Distribution
SELECT
    churn_risk_category,
    COUNT(DISTINCT customer_id) AS users,
    COUNT(DISTINCT customer_id) * 1.0 / SUM(COUNT(DISTINCT customer_id)) OVER () AS user_share
FROM cleaned_user_journey
GROUP BY churn_risk_category
ORDER BY users DESC;

-- 8. Customer Detail Table
SELECT
    customer_id,
    country,
    device_type,
    customer_segment,
    acquisition_channel,
    churn_risk_category,
    MAX(funnel_stage_order) AS latest_stage_order,
    SUM(revenue) AS total_revenue,
    MAX(d1_retained) AS d1_retained,
    MAX(d7_retained) AS d7_retained
FROM cleaned_user_journey
GROUP BY customer_id, country, device_type, customer_segment, acquisition_channel, churn_risk_category
ORDER BY total_revenue DESC;
