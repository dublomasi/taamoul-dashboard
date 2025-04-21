import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load live Google Sheet data
sheet_url = "https://docs.google.com/spreadsheets/d/1-Ggb6dpLnG708qdp_498uWE3XUpQYIh8f7WBrvPJGEY/export?format=csv"
df = pd.read_csv(sheet_url)

# Page settings
st.set_page_config(page_title="Taamoul HQ - YouTube Comment Agent", layout="centered")
st.title("Taamoul HQ - YouTube Comment Agent")

# Basic Metrics
total_comments = len(df)
positive_comments = len(df[df['Sentiment'].str.lower() == 'positive'])
pending_replies = df['Suggested Reply'].isna().sum()

st.metric("Total Comments", total_comments)
st.metric("Positive Sentiment", positive_comments)
st.metric("Pending Replies", pending_replies)

# Divider
st.markdown("---")

# Sentiment Distribution Chart
st.subheader("Sentiment Distribution")
sentiment_counts = df['Sentiment'].value_counts()

fig, ax = plt.subplots()
colors = ['#4caf50', '#2196f3', '#f44336']  # Green, Blue, Red
sentiment_counts.plot.pie(autopct='%1.1f%%', colors=colors, ax=ax)
ax.set_ylabel('')  # Hide y-label
st.pyplot(fig)

# Divider
st.markdown("---")

# Optional: Show Table of Comments
with st.expander("View All Comments"):
    st.dataframe(df[['Comment', 'Sentiment', 'Suggested Reply']])
