import pandas as pd

# parse_dates converts date columns from string to datetime if not already converted
# This is a safety utility — it ensures date math won't fail due to string types
def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # pd.to_datetime handles many date formats automatically (ISO, US, EU, etc.)
    # errors='coerce' turns unparseable dates into NaT (Not a Time) instead of crashing
    for col in ['order_date', 'delivery_date']:
        if df[col].dtype == object:
            # Only convert if the column is still a string (object dtype)
            df[col] = pd.to_datetime(df[col], errors='coerce')

    return df


# compute_lead_time calculates how long each order took from placement to delivery
# In supply chain, "lead time" is a key performance metric — shorter is better
# It answers: how many days did the customer wait for their order?
def compute_lead_time(df: pd.DataFrame) -> pd.Series:
    # Subtracting two datetime columns gives a Timedelta; .dt.days extracts the integer
    lead_time = (df['delivery_date'] - df['order_date']).dt.days

    # Name the Series so it's easy to identify when used in DataFrames
    lead_time.name = 'lead_time'
    return lead_time
