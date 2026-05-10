
SELECT risk_category,
       COUNT(*) AS users
FROM customer_user_journey_data
GROUP BY risk_category;
