import matplotlib.pyplot as plt
import streamlit as st
from processing.analytics import regional_demand

# render draws a horizontal bar chart of total order quantity per region
# Horizontal bars are easier to read when region names are long strings
def render(df):
    st.subheader("Regional Demand")

    # Get total qty and order count grouped by region
    demand = regional_demand(df)

    # Sort by total_qty descending so the busiest region appears at the top
    demand = demand.sort_values('total_qty', ascending=True)

    fig, ax = plt.subplots(figsize=(8, 5))

    # barh = horizontal bar chart; region on y-axis, quantity on x-axis
    ax.barh(demand['region'], demand['total_qty'], color='steelblue')

    ax.set_title("Regional Demand")
    ax.set_xlabel("Total Order Quantity")
    ax.set_ylabel("Region")

    # Add value labels at the end of each bar for quick reading
    for i, val in enumerate(demand['total_qty']):
        ax.text(val + 5, i, str(val), va='center', fontsize=9)

    st.pyplot(fig)

    # Show order count next to qty so users see both volume metrics
    st.dataframe(demand.sort_values('total_qty', ascending=False).reset_index(drop=True))
