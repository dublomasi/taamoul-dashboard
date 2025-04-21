import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Streamlit layout
st.set_page_config(page_title="Taamoul HQ Dashboard", layout="centered")

# Logo
st.markdown(
    "<div style='text-align: center; margin-bottom: 10px;'>"
    "<img src='https://i.ibb.co/t3P8ktJ/taamoul-logo.png' width='160'>"
    "</div>", unsafe_allow_html=True
)

st.title("Taamoul HQ – YouTube Comment Agent")

# Google Sheet URL
sheet_url = "https://docs.google.com/spreadsheets/d/1-Ggb6dpLnG708qdp_498uWE3XUpQYIh8f7WBrvPJGEY/export?format=csv"

try:
    df = pd.read_csv(sheet_url)

    if df.empty:
        st.error("⚠️ The Google Sheet loaded but contains no data.")
    else:
        # Timestamp
        st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Optional filters
        if "Playlist" in df.columns:
            playlist = st.selectbox("Filter by Playlist:", ["All"] + sorted(df["Playlist"].dropna().unique().tolist()))
            if playlist != "All":
                df = df[df["Playlist"] == playlist]

        if "Language" in df.columns:
            lang = st.selectbox("Filter by Language:", ["All", "Arabic", "English", "Mixed"])
            if lang != "All":
                df = df[df["Language"] == lang]

        # Clean up
        df['Sentiment'] = df['Sentiment'].astype(str)

        # Metrics
        total_comments = len(df)
        positive_comments = len(df[df['Sentiment'].str.lower() == 'positive'])
        pending_replies = df['Suggested Reply'].isna().sum()

        st.metric("Total Comments", total_comments)
        st.metric("Positive Sentiment", positive_comments)
        st.metric("Pending Replies", pending_replies)

        st.markdown("---")

        # Sentiment chart
        st.subheader("Sentiment Distribution")
        sentiment_counts = df['Sentiment'].value_counts()
        fig, ax = plt.subplots()
        sentiment_counts.plot.pie(
            autopct='%1.1f%%',
            startangle=90,
            counterclock=False,
            ax=ax
        )
        ax.set_ylabel('')
        st.pyplot(fig)

        st.markdown("---")

        # Data preview
        with st.expander("View Comment Data"):
            preview_cols = ['Comment', 'Sentiment', 'Suggested Reply']
            if "Playlist" in df.columns:
                preview_cols.append("Playlist")
            if "Language" in df.columns:
                preview_cols.append("Language")
            st.dataframe(df[preview_cols])

except Exception as e:
    st.error("❌ Could not load data from Google Sheet.")
    st.error(str(e))
