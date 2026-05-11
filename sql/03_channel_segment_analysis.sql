-- Channel conversion and segment revenue analysis
WITH user_stage AS (
    SELECT
        customer_id,
        acquisition_channel,
        customer_segment,
        MAX(CASE WHEN funnel_stage = 'Awareness' THEN 1 ELSE 0 END) AS reached_awareness,
        MAX(CASE WHEN funnel_stage = 'Purchase' THEN 1 ELSE 0 END) AS reached_purchase,
        SUM(revenue) AS revenue
    FROM customer_user_journey
    GROUP BY customer_id, acquisition_channel, customer_segment
)
SELECT
    acquisition_channel,
    customer_segment,
    COUNT(DISTINCT customer_id) AS users,
    SUM(reached_purchase) * 1.0 / NULLIF(SUM(reached_awareness), 0) AS conversion_rate,
    SUM(revenue) AS total_revenue,
    SUM(revenue) * 1.0 / NULLIF(COUNT(DISTINCT customer_id), 0) AS revenue_per_user
FROM user_stage
GROUP BY acquisition_channel, customer_segment
ORDER BY total_revenue DESC;
