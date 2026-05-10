
SELECT funnel_stage,
       COUNT(DISTINCT user_id) AS users
FROM customer_user_journey_data
GROUP BY funnel_stage
ORDER BY users DESC;
