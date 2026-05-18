import os

# FILE_PATH tells the data loader where to find the raw CSV dataset
# We use os.path so this works on any operating system (Windows/Mac/Linux)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = os.path.join(BASE_DIR, "data", "aws_supply_chain_orders_raw.csv")

# PAGE_TITLE is shown at the top of the Streamlit browser tab and app header
PAGE_TITLE = "Supply Chain Analytics Dashboard"

# DATE_COLUMNS lists column names that should be parsed as datetime objects
# Without this, pandas reads dates as plain strings, which breaks date math
DATE_COLUMNS = ['order_date', 'delivery_date']

# NUMERIC_COLS lists columns that should contain numbers
# We reference these during cleaning to fill missing values and validate types
NUMERIC_COLS = ['order_qty', 'delivery_time_days']
