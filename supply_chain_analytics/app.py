import sys
import os

# Add the project root to sys.path so Python can find our local modules
# Without this, imports like 'from processing.data_loader import load_data' would fail
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from config.settings import FILE_PATH, PAGE_TITLE
from processing.data_loader import load_data
from processing.data_cleaner import clean_data

# Import each visualization module — each has a render(df) function
from visualizations import (
    status_dashboard,
    warehouse_performance,
    regional_demand,
    delivery_variance,
    delay_tracking,
    product_analysis,
)

# st.set_page_config must be the very first Streamlit call in the script
# It sets the browser tab title and page layout (wide = full browser width)
st.set_page_config(page_title=PAGE_TITLE, layout="wide")

# st.title renders a large H1 heading at the top of the page
st.title(PAGE_TITLE)

# --- Load and clean data once, cache it so Streamlit doesn't reload on every interaction ---
# @st.cache_data stores the function result; on re-runs it returns the cached version
@st.cache_data
def get_data():
    # Load raw CSV from the path defined in config/settings.py
    raw_df = load_data(FILE_PATH)
    # Clean and enrich the data (fill nulls, add derived columns, etc.)
    clean_df = clean_data(raw_df)
    return raw_df, clean_df

raw_df, df = get_data()

# --- Raw Data Expander ---
# st.expander creates a collapsible section so the raw table doesn't crowd the page
with st.expander("Raw Data Preview"):
    # Show basic shape info so users know how large the dataset is
    st.write(f"Dataset shape: {raw_df.shape[0]} rows × {raw_df.shape[1]} columns")
    # df.head() shows only the first 5 rows to keep the preview concise
    st.dataframe(raw_df.head())

# --- Sidebar Navigation ---
# st.sidebar.radio creates a vertical list of radio buttons in the left sidebar
# Users click a page name to switch views without reloading the app
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a Page",
    [
        "Status Dashboard",
        "Warehouse Performance",
        "Regional Demand",
        "Delivery Variance",
        "Delay Tracking",
        "Product Analysis",
    ]
)

# --- Page Routing ---
# Route the selected page name to its corresponding render() function
# Each render() function receives the cleaned DataFrame and draws its charts
if page == "Status Dashboard":
    status_dashboard.render(df)

elif page == "Warehouse Performance":
    warehouse_performance.render(df)

elif page == "Regional Demand":
    regional_demand.render(df)

elif page == "Delivery Variance":
    delivery_variance.render(df)

elif page == "Delay Tracking":
    delay_tracking.render(df)

elif page == "Product Analysis":
    product_analysis.render(df)
