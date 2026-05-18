import matplotlib.pyplot as plt
import streamlit as st
from processing.analytics import status_distribution

# render draws a pie chart showing the breakdown of order statuses
# A pie chart is ideal here because we want to show proportions of a whole
def render(df):
    st.subheader("Order Status Distribution")

    # Get the count of each status value as a Series
    counts = status_distribution(df)

    # Build color list in the same order as counts.index
    # Consistent colors let users immediately understand the chart without re-reading labels
    color_map = {'Delivered': 'green', 'Pending': 'orange', 'Delayed': 'red'}
    colors = [color_map.get(label, 'gray') for label in counts.index]

    fig, ax = plt.subplots()

    # autopct='%1.1f%%' adds percentage labels inside each pie slice
    # startangle=90 rotates the chart so the first slice starts at the top
    ax.pie(counts.values, labels=counts.index, colors=colors,
           autopct='%1.1f%%', startangle=90)

    ax.set_title("Order Status Distribution")

    # st.pyplot renders the Matplotlib figure inside the Streamlit page
    st.pyplot(fig)

    # Show the raw counts as a table below the chart for precise numbers
    st.dataframe(counts.rename("Order Count"))
