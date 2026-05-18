import pandas as pd

# status_distribution tells us how many orders are in each status bucket
# Useful for understanding the overall health of the supply chain at a glance
def status_distribution(df: pd.DataFrame) -> pd.Series:
    # value_counts counts occurrences of each unique status value
    return df['status'].value_counts()


# warehouse_performance aggregates key metrics per warehouse
# Helps identify which warehouses are efficient and which are causing delays
def warehouse_performance(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby('warehouse').agg(
        # Total number of orders handled by each warehouse
        total_orders=('order_id', 'count'),
        # Total units shipped — higher means more throughput
        total_qty=('order_qty', 'sum'),
        # Average delivery time — lower is better for customer satisfaction
        avg_delivery_days=('delivery_time_days', 'mean'),
        # Count of orders explicitly marked as Delayed
        delay_count=('is_delayed', 'sum')
    ).reset_index()

    # delay_rate_pct shows what percentage of orders from each warehouse were delayed
    # This normalizes delay_count against volume so large warehouses aren't unfairly penalized
    grouped['delay_rate_pct'] = (grouped['delay_count'] / grouped['total_orders'] * 100).round(2)

    return grouped


# regional_demand shows which regions are ordering the most
# Useful for inventory planning — high-demand regions need more stock nearby
def regional_demand(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby('region').agg(
        total_qty=('order_qty', 'sum'),
        order_count=('order_id', 'count')
    ).reset_index()


# delivery_variance extracts delivery_time_days as a Series for histogram plotting
# A wide spread means inconsistent delivery performance; narrow spread is more reliable
def delivery_variance(df: pd.DataFrame) -> pd.Series:
    # Dropping NaN values before returning ensures the histogram has no gaps
    return df['delivery_time_days'].dropna()


# delay_tracking returns order-level data for scatter plot analysis
# Comparing order_qty vs delivery_time and coloring by status reveals patterns
# e.g., large orders might consistently get delayed
def delay_tracking(df: pd.DataFrame) -> pd.DataFrame:
    return df[['order_qty', 'delivery_time_days', 'status', 'is_delayed']].copy()


# product_analysis creates a pivot table to compare product sales across warehouses
# A pivot table reshapes the data from rows into a grid (warehouse x product)
def product_analysis(df: pd.DataFrame) -> pd.DataFrame:
    # aggfunc='sum' means each cell shows total order_qty for that warehouse/product combo
    # fill_value=0 ensures empty cells show 0 instead of NaN
    pivot = pd.pivot_table(
        df,
        values='order_qty',
        index='warehouse',
        columns='product',
        aggfunc='sum',
        fill_value=0
    )
    return pivot
