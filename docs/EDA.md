# EDA Cleaning Report — Customer User Journey

## Cleaning Steps Included

```python
import pandas as pd
import numpy as np

raw_path = "../data/raw_user_journey.csv"
df = pd.read_csv(raw_path)

df.head()
df.shape
df.info()
df.describe()
df.isnull().sum()
df.duplicated().sum()
df.columns
```

## Column Standardization

```python
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
)
```

## Date Conversion

```python
df["journey_date"] = pd.to_datetime(df["journey_date"], errors="coerce")
```

## Numeric Validation

```python
numeric_cols = ["revenue", "d1_retained", "d7_retained", "funnel_stage_order"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")
```

## Missing Values and Duplicates

```python
missing_summary = df.isnull().sum()
duplicate_count = df.duplicated().sum()
df = df.drop_duplicates()
```

## Categorical Validation

```python
for col in ["country", "device_type", "customer_segment", "acquisition_channel", "churn_risk_category", "funnel_stage"]:
    print(col, df[col].value_counts())
```

## Feature Engineering

```python
df["converted_flag"] = (df["funnel_stage"].str.lower() == "purchase").astype(int)
df["revenue_user_flag"] = (df["revenue"] > 0).astype(int)
df["retention_status"] = np.where(
    df["d7_retained"] == 1, "D7 Retained",
    np.where(df["d1_retained"] == 1, "D1 Only", "Not Retained")
)
df["revenue_band"] = pd.cut(
    df["revenue"],
    bins=[-1, 0, 50, 150, 100000],
    labels=["No Revenue", "$1-$50", "$51-$150", "$150+"]
)
```

## KPI Validation

```python
total_users = df["customer_id"].nunique()
purchase_users = df.loc[df["funnel_stage"].str.lower() == "purchase", "customer_id"].nunique()
conversion_rate = purchase_users / total_users
user_level = df.drop_duplicates("customer_id")
d1_retention = user_level["d1_retained"].mean()
d7_retention = user_level["d7_retained"].mean()
revenue_per_user = df["revenue"].sum() / total_users
```

## Export Cleaned Dataset

```python
df.to_csv("../data/cleaned_user_journey.csv", index=False)
```
