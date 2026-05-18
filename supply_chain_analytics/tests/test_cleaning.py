import sys
import os
import pytest
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from processing.data_cleaner import clean_data

# Build a small sample DataFrame that mimics the real CSV structure
# Including NaN values in delivery_time_days and region to test null-filling
@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'order_id': ['ORD-001', 'ORD-002', 'ORD-003', 'ORD-004'],
        'warehouse': ['WH-A', 'WH-B', 'WH-A', 'WH-C'],
        'region': ['North', None, 'South', None],
        'product': ['Laptop', 'Router', 'Server', 'Laptop'],
        'order_qty': [10, 5, 20, 8],
        'order_date': ['2024-01-01', '2024-01-05', '2024-01-10', '2024-01-15'],
        'delivery_date': ['2024-01-08', '2024-01-12', '2024-01-20', '2024-01-22'],
        'delivery_time_days': [7.0, np.nan, 10.0, np.nan],
        'status': ['Delivered', 'Pending', 'Delayed', 'Delivered']
    })

# After cleaning, delivery_time_days should have no null values
def test_no_nulls_in_delivery_time_days(sample_df):
    cleaned = clean_data(sample_df)
    # isnull().sum() == 0 confirms every row has a value in this column
    assert cleaned['delivery_time_days'].isnull().sum() == 0

# After cleaning, region nulls should be filled with 'Unknown', not NaN
def test_region_nulls_filled(sample_df):
    cleaned = clean_data(sample_df)
    assert cleaned['region'].isnull().sum() == 0
    assert 'Unknown' in cleaned['region'].values

# is_delayed column must exist and contain only True/False values (boolean dtype)
def test_is_delayed_column_exists_and_is_boolean(sample_df):
    cleaned = clean_data(sample_df)
    assert 'is_delayed' in cleaned.columns
    # All values must be boolean — True where status == 'Delayed', False otherwise
    assert cleaned['is_delayed'].dtype == bool

# actual_days and delivery_gap derived columns should also be created
def test_derived_columns_exist(sample_df):
    cleaned = clean_data(sample_df)
    assert 'actual_days' in cleaned.columns
    assert 'delivery_gap' in cleaned.columns
