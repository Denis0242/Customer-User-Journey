-- D1 and D7 retention trend by journey date
SELECT
    journey_date,
    AVG(d1_retained) AS d1_retention_rate,
    AVG(d7_retained) AS d7_retention_rate,
    COUNT(DISTINCT customer_id) AS active_users
FROM customer_user_journey
GROUP BY journey_date
ORDER BY journey_date;
