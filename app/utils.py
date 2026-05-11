import pandas as pd

STAGE_ORDER = ["Awareness", "Consideration", "Intent", "Checkout", "Purchase"]

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["Journey Date"] = pd.to_datetime(df["Journey Date"])
    return df

def compute_kpis(df: pd.DataFrame) -> dict:
    users = df["Customer ID"].nunique()
    awareness = df.loc[df["Funnel Stage"].eq("Awareness"), "Customer ID"].nunique()
    purchase = df.loc[df["Funnel Stage"].eq("Purchase"), "Customer ID"].nunique()
    user_level = df.drop_duplicates("Customer ID")
    return {
        "Total Users": users,
        "Conversion Rate": purchase / awareness if awareness else 0,
        "D1 Retention": user_level["D1 Retained"].mean(),
        "D7 Retention": user_level["D7 Retained"].mean(),
        "Revenue per User": df["Revenue"].sum() / users if users else 0,
    }

def funnel_table(df: pd.DataFrame) -> pd.DataFrame:
    out = (df.groupby(["Funnel Stage", "Funnel Stage Order"])["Customer ID"]
             .nunique().reset_index(name="Users")
             .sort_values("Funnel Stage Order"))
    out["Previous Stage Users"] = out["Users"].shift(1)
    out["Drop-off Rate"] = 1 - (out["Users"] / out["Previous Stage Users"])
    return out
