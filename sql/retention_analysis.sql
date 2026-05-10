
SELECT date,
       AVG(d1_retention) AS avg_d1_retention,
       AVG(d7_retention) AS avg_d7_retention
FROM customer_user_journey_data
GROUP BY date
ORDER BY date;
