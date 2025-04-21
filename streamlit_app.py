
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data from Google Sheets
sheet_url = "https://docs.google.com/spreadsheets/d/1-Ggb6dpLnG708qdp_498uWE3XUpQYIh8f7WBrvPJGEY/export?format=csv"
df = pd.read_csv(sheet_url)

st.set_page_config(page_title="Taamoul HQ Dashboard", layout="wide")

st.title("Taamoul HQ - YouTube Comment Agent")

# Summary metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Comments", len(df))
col2.metric("Positive Sentiment", df[df["Sentiment"] == "Positive"].shape[0])
col3.metric("Pending Replies", df[df["Status"] == "Pending"].shape[0])

# Pie chart: Sentiment Breakdown
st.subheader("Sentiment Distribution")
fig_sentiment = px.pie(df, names="Sentiment", title="Overall Sentiment")
st.plotly_chart(fig_sentiment, use_container_width=True)

# Bar chart: Reply Status
st.subheader("Reply Status Overview")
fig_status = px.histogram(df, x="Status", color="Status", title="Reply Status Count")
st.plotly_chart(fig_status, use_container_width=True)

# Data Table
st.subheader("Comment Log")
st.dataframe(df)
