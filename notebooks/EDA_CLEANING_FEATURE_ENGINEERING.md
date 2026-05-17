# EDA, Cleaning & Feature Engineering

## 1. Load Data
Loaded `data/user_realistic.csv` with **2,240 rows** and **13 columns**.

## 2. Dataset Overview
The dataset captures customer journey events, funnel stages, retention flags, churn-risk categories, revenue, country, device, segment, and acquisition channel.

## 3. Missing Values
Missing values should be checked before dashboarding.

```python
df.isna().sum()
```

## 4. Duplicates
Duplicates were removed to avoid inflated funnel counts and revenue totals.

```python
df = df.drop_duplicates()
```

## 5. Datatype Cleaning
`Journey Date` was converted into datetime format.

```python
df["Journey Date"] = pd.to_datetime(df["Journey Date"], errors="coerce")
```

## 6. Column Cleaning
Column names were standardized into lowercase snake_case for SQL/Python consistency.

## 7. Text Cleaning
Categorical fields such as country, device type, customer segment, acquisition channel, churn risk, and funnel stage were stripped of extra spaces.

## 8. Outlier Detection
Revenue was checked for negative values and extreme values.

## 9. Range Validation
Retention flags were validated to ensure values remain binary: 0 or 1.

## 10. KPI Validation
Validated core metrics:
- D1 retention: **74.0%**
- D7 retention: **45.8%**
- Overall conversion: **25.0%**
- Total revenue: **$20,467**

## 11. Feature Engineering
Created:
- `conversion_flag`
- `retention_gap`
- `revenue_band`

## 12. Business Logic Validation
Funnel stage order was validated so the dashboard follows the correct journey sequence:
Awareness → Consideration → Intent → Checkout → Purchase.

## 13. Summary Statistics
The project includes summary files for:
- Funnel performance
- Segment performance
- Churn-risk performance

## 14. Final Clean Dataset Export
Cleaned data was exported to:

```text
data/user_journey_clean.csv
```

## 15. Insight Summary
The data shows a clear product analytics story: customers enter the journey at awareness, some drop off at each stage, and the business needs to improve conversion while maintaining D7 retention and managing churn-risk exposure.
