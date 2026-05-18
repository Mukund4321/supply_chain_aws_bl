import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from processing.analytics import delay_tracking

# render draws a scatter plot of order_qty vs delivery_time_days, colored by status
# This reveals whether large or small orders are more likely to be delayed
def render(df):
    st.subheader("Delay Tracking: Order Qty vs Delivery Time")

    # Get the relevant columns for this scatter plot
    data = delay_tracking(df)

    # Define consistent colors so Delivered=green, Pending=orange, Delayed=red
    palette = {'Delivered': 'green', 'Pending': 'orange', 'Delayed': 'red'}

    fig, ax = plt.subplots(figsize=(9, 5))

    # Seaborn's scatterplot handles the color mapping automatically via hue + palette
    # alpha=0.7 adds slight transparency so overlapping points are still visible
    sns.scatterplot(
        data=data,
        x='order_qty',
        y='delivery_time_days',
        hue='status',
        palette=palette,
        alpha=0.7,
        ax=ax
    )

    ax.set_title("Delay Tracking: Order Qty vs Delivery Time")
    ax.set_xlabel("Order Quantity")
    ax.set_ylabel("Delivery Time (Days)")

    # Move legend outside the plot so it doesn't overlap data points
    ax.legend(title="Status", bbox_to_anchor=(1.05, 1), loc='upper left')

    st.pyplot(fig)
