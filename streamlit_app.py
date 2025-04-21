import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ✅ LIVE Google Sheet CSV export link
sheet_url = "https://docs.google.com/spreadsheets/d/1-Ggb6dpLnG708qdp_498uWE3XUpQYIh8f7WBrvPJGEY/export?format=csv"
df = pd.read_csv(sheet_url)

# Debug print
st.write(df.head())  # <- This helps confirm it’s loading

# Metrics
st.title("Taamoul HQ - YouTube Comment Agent")
st.metric("Total Comments", len(df))
st.metric("Positive Sentiment", len(df[df['Sentiment'].str.lower() == 'positive']))
st.metric("Pending Replies", df['Suggested Reply'].isna().sum())

# Pie Chart
st.subheader("Sentiment Distribution")
sentiment_counts = df['Sentiment'].value_counts()
fig, ax = plt.subplots()
sentiment_counts.plot.pie(autopct='%1.1f%%', ax=ax)
ax.set_ylabel('')
st.pyplot(fig)
