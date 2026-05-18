import matplotlib.pyplot as plt
import streamlit as st
from processing.analytics import delivery_variance

# render draws a histogram of delivery times with mean and median reference lines
# Showing both lines helps identify if the distribution is skewed by outliers
def render(df):
    st.subheader("Delivery Time Variance")

    # Get the delivery_time_days column as a clean Series (no NaN)
    times = delivery_variance(df)

    mean_val = times.mean()
    median_val = times.median()

    fig, ax = plt.subplots(figsize=(8, 5))

    # bins=20 divides the range into 20 equal-width buckets for the histogram
    # edgecolor='white' adds borders between bars so they're easier to distinguish
    ax.hist(times, bins=20, color='steelblue', edgecolor='white', alpha=0.8)

    # Vertical dashed lines show where mean and median fall in the distribution
    # If mean >> median, there are right-skewed outliers pulling the average up
    ax.axvline(mean_val, color='red', linestyle='--', linewidth=1.5,
               label=f'Mean: {mean_val:.1f} days')
    ax.axvline(median_val, color='orange', linestyle='-', linewidth=1.5,
               label=f'Median: {median_val:.1f} days')

    ax.set_title("Delivery Time Variance")
    ax.set_xlabel("Delivery Time (Days)")
    ax.set_ylabel("Number of Orders")

    # Legend makes the two reference lines immediately identifiable
    ax.legend()

    st.pyplot(fig)
