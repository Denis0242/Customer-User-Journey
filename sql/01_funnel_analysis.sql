-- Customer journey funnel analysis
WITH stage_users AS (
    SELECT
        funnel_stage,
        funnel_stage_order,
        COUNT(DISTINCT customer_id) AS users
    FROM customer_user_journey
    GROUP BY funnel_stage, funnel_stage_order
),
ordered_stages AS (
    SELECT
        funnel_stage,
        funnel_stage_order,
        users,
        LAG(users) OVER (ORDER BY funnel_stage_order) AS previous_stage_users
    FROM stage_users
)
SELECT
    funnel_stage,
    funnel_stage_order,
    users,
    previous_stage_users,
    users * 1.0 / NULLIF(previous_stage_users, 0) AS stage_conversion_rate,
    1 - (users * 1.0 / NULLIF(previous_stage_users, 0)) AS dropoff_rate
FROM ordered_stages
ORDER BY funnel_stage_order;
