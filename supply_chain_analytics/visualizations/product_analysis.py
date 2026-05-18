import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from processing.analytics import product_analysis

# render draws a heatmap showing total order_qty per warehouse-product combination
# Heatmaps are excellent for spotting high/low demand intersections at a glance
def render(df):
    st.subheader("Product Analysis Heatmap")

    # Get the pivot table: rows = warehouse, columns = product, values = total order_qty
    pivot = product_analysis(df)

    fig, ax = plt.subplots(figsize=(9, 4))

    # annot=True prints the numeric value inside each cell so users don't need to read the colorbar
    # fmt='d' formats values as integers (no decimal places)
    # cmap='YlOrRd' = yellow → orange → red, higher values appear darker/redder
    sns.heatmap(pivot, annot=True, fmt='d', cmap='YlOrRd', linewidths=0.5, ax=ax)

    ax.set_title("Product Analysis Heatmap (Order Qty by Warehouse & Product)")
    ax.set_xlabel("Product")
    ax.set_ylabel("Warehouse")

    st.pyplot(fig)

    # Show the underlying pivot table so users can see exact numbers in tabular form
    st.dataframe(pivot)
