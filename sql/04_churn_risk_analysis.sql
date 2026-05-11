-- Churn risk distribution and retention profile
SELECT
    churn_risk_category,
    COUNT(DISTINCT customer_id) AS users,
    AVG(d1_retained) AS d1_retention_rate,
    AVG(d7_retained) AS d7_retention_rate,
    SUM(revenue) AS total_revenue
FROM customer_user_journey
GROUP BY churn_risk_category
ORDER BY users DESC;
