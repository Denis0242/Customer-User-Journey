
SELECT segment,
       SUM(revenue) AS total_revenue
FROM customer_user_journey_data
GROUP BY segment
ORDER BY total_revenue DESC;
