import sys
import os
import pytest
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from processing.data_cleaner import clean_data
from processing.analytics import warehouse_performance, product_analysis, status_distribution

# Build a small cleaned-style DataFrame to feed into analytics functions
@pytest.fixture
def cleaned_df():
    raw = pd.DataFrame({
        'order_id': ['ORD-001', 'ORD-002', 'ORD-003', 'ORD-004', 'ORD-005'],
        'warehouse': ['WH-A', 'WH-B', 'WH-A', 'WH-C', 'WH-B'],
        'region': ['North', 'South', 'North', 'East', 'South'],
        'product': ['Laptop', 'Router', 'Server', 'Laptop', 'Switch'],
        'order_qty': [10, 5, 20, 8, 15],
        'order_date': ['2024-01-01', '2024-01-05', '2024-01-10', '2024-01-15', '2024-01-20'],
        'delivery_date': ['2024-01-08', '2024-01-12', '2024-01-20', '2024-01-22', '2024-01-28'],
        'delivery_time_days': [7.0, 7.0, 10.0, 7.0, 8.0],
        'status': ['Delivered', 'Pending', 'Delayed', 'Delivered', 'Delayed']
    })
    return clean_data(raw)

# warehouse_performance() must return a DataFrame that includes the delay_rate_pct column
def test_warehouse_performance_has_delay_rate_pct(cleaned_df):
    result = warehouse_performance(cleaned_df)
    assert isinstance(result, pd.DataFrame)
    assert 'delay_rate_pct' in result.columns

# warehouse_performance() must have one row per warehouse
def test_warehouse_performance_row_count(cleaned_df):
    result = warehouse_performance(cleaned_df)
    # Our sample has 3 unique warehouses
    assert len(result) == 3

# product_analysis() must return a pivot table with warehouse as the index
def test_product_analysis_has_warehouse_index(cleaned_df):
    result = product_analysis(cleaned_df)
    assert isinstance(result, pd.DataFrame)
    # The index name of the pivot table should be 'warehouse'
    assert result.index.name == 'warehouse'

# product_analysis() columns should be the product names
def test_product_analysis_columns_are_products(cleaned_df):
    result = product_analysis(cleaned_df)
    # All products in our sample should appear as columns
    for product in ['Laptop', 'Router', 'Server', 'Switch']:
        assert product in result.columns

# status_distribution() should return a Series with counts for each status
def test_status_distribution_returns_series(cleaned_df):
    result = status_distribution(cleaned_df)
    assert isinstance(result, pd.Series)
    # We have Delivered, Pending, and Delayed in our sample
    assert 'Delivered' in result.index
