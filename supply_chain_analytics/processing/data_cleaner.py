import pandas as pd

# clean_data takes the raw DataFrame and returns a cleaned, analysis-ready version
# Each step below handles a specific real-world data quality issue
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Work on a copy so the original raw data is never modified
    # This is important for reproducibility — we can always re-run from raw
    df = df.copy()

    # Fill missing delivery_time_days with the column median (not mean)
    # Median is preferred because it's resistant to outliers like unusually long deliveries
    median_days = df['delivery_time_days'].median()
    df['delivery_time_days'] = df['delivery_time_days'].fillna(median_days)

    # Fill missing region values with 'Unknown' so groupby operations still include them
    # Dropping these rows would silently lose orders and skew regional totals
    df['region'] = df['region'].fillna('Unknown')

    # Convert date columns from strings to datetime objects
    # This enables date arithmetic like calculating how many days between two dates
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['delivery_date'] = pd.to_datetime(df['delivery_date'])

    # Remove exact duplicate rows — duplicates can skew counts and totals
    # keep='first' means we retain the first occurrence of each duplicate
    df = df.drop_duplicates()

    # Convert status to category dtype to save memory and speed up groupby
    # Category dtype tells pandas the column has a fixed set of possible values
    df['status'] = df['status'].astype('category')

    # is_delayed flags rows where the order was officially marked as Delayed
    # This boolean column makes it easy to filter or count delayed orders later
    df['is_delayed'] = df['status'] == 'Delayed'

    # actual_days computes how many calendar days elapsed between order and delivery
    # This is the real delivery duration, regardless of what delivery_time_days says
    df['actual_days'] = (df['delivery_date'] - df['order_date']).dt.days

    # delivery_gap measures how far off the recorded delivery_time_days was
    # A positive gap means it took longer than expected; negative means it was faster
    df['delivery_gap'] = df['actual_days'] - df['delivery_time_days']

    print(f"[data_cleaner] Cleaned data: {df.shape[0]} rows, {df.shape[1]} columns")
    return df
