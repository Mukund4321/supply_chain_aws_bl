import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from processing.analytics import warehouse_performance

# render shows two charts: avg delivery days per warehouse, and qty per warehouse/product
# Together they help diagnose whether slow warehouses are also high-volume ones
def render(df):
    st.subheader("Warehouse Performance")

    # Compute the aggregated warehouse metrics
    perf = warehouse_performance(df)

    # --- Chart 1: Average delivery days per warehouse ---
    fig1, ax1 = plt.subplots()

    # A bar chart clearly compares a single metric across discrete categories (warehouses)
    sns.barplot(data=perf, x='warehouse', y='avg_delivery_days', palette='Blues_d', ax=ax1)

    ax1.set_title("Avg Delivery Days per Warehouse")
    ax1.set_xlabel("Warehouse")
    ax1.set_ylabel("Avg Delivery Days")

    st.pyplot(fig1)

    # --- Chart 2: Total order quantity per warehouse, broken down by product ---
    # First we need to reshape the data so each product is a separate column
    product_qty = df.groupby(['warehouse', 'product'])['order_qty'].sum().reset_index()

    # pivot makes warehouse the x-axis and each product a separate bar group
    pivot = product_qty.pivot(index='warehouse', columns='product', values='order_qty').fillna(0)

    fig2, ax2 = plt.subplots(figsize=(10, 5))

    # kind='bar' with a pivot DataFrame draws a grouped bar chart automatically
    pivot.plot(kind='bar', ax=ax2, colormap='tab10')

    ax2.set_title("Total Order Qty per Warehouse by Product")
    ax2.set_xlabel("Warehouse")
    ax2.set_ylabel("Total Order Qty")

    # Rotate x-axis labels so warehouse names don't overlap
    ax2.tick_params(axis='x', rotation=0)
    ax2.legend(title="Product", bbox_to_anchor=(1.05, 1), loc='upper left')

    st.pyplot(fig2)

    # Show the numeric summary table so users can see exact delay rates
    st.dataframe(perf)
