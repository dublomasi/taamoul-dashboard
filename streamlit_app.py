import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Taamoul HQ Dashboard", layout="centered")

# Logo
st.markdown(
    "<div style='text-align: center;'><img src='https://i.ibb.co/t3P8ktJ/taamoul-logo.png' width='160'></div>",
    unsafe_allow_html=True
)

st.title("Taamoul HQ – YouTube Comment Agent")

# Google Sheet
sheet_url = "https://docs.google.com/spreadsheets/d/1-Ggb6dpLnG708qdp_498uWE3XUpQYIh8f7WBrvPJGEY/export?format=csv"

try:
    df = pd.read_csv(sheet_url)

    # Clean headers
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.encode("utf-8").str.decode("utf-8")

    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("**Detected columns:**")
    st.code(df.columns.tolist())

    # Extract columns safely
    comment_col = df["Comment"] if "Comment" in df.columns else None
    sentiment_col = df["Sentiment"] if "Sentiment" in df.columns else None
    reply_col = df["Suggested Reply"] if "Suggested Reply" in df.columns else None
    playlist_col = df["Playlist"] if "Playlist" in df.columns else None
    language_col = df["Language"] if "Language" in df.columns else None

    # Filters
    if playlist_col is not None:
        playlist = st.selectbox("Filter by Playlist:", ["All"] + sorted(playlist_col.dropna().unique()))
        if playlist != "All":
            df = df[playlist_col == playlist]

    if language_col is not None:
        language = st.selectbox("Filter by Language:", ["All"] + sorted(language_col.dropna().unique()))
        if language != "All":
            df = df[language_col == language]

    # Metrics
    st.metric("Total Comments", len(df))

    if sentiment_col is not None:
        positive_count = sentiment_col.str.lower().eq("positive").sum()
        st.metric("Positive Sentiment", positive_count)
    else:
        st.warning("Missing 'Sentiment' column.")

    if reply_col is not None:
        pending_count = reply_col.isna().sum()
        st.metric("Pending Replies", pending_count)
    else:
        st.warning("Missing 'Suggested Reply' column.")

    st.markdown("---")

    # Pie chart
    if sentiment_col is not None:
        st.subheader("Sentiment Distribution")
        fig, ax = plt.subplots()
        sentiment_col.value_counts().plot.pie(
            autopct='%1.1f%%',
            startangle=90,
            counterclock=False,
            ax=ax
        )
        ax.set_ylabel("")
        st.pyplot(fig)
    else:
        st.info("Cannot show chart — 'Sentiment' column is missing.")

    st.markdown("---")

    # Table
    with st.expander("View Comments"):
        cols = {
            "Comment": comment_col,
            "Sentiment": sentiment_col,
            "Suggested Reply": reply_col,
            "Playlist": playlist_col,
            "Language": language_col
        }
        available = [name for name, col in cols.items() if col is not None]
        if available:
            st.dataframe(df[available])
        else:
            st.info("No columns available to show.")

except Exception as e:
    st.error("❌ Could not load or parse the Google Sheet.")
    st.exception(e)
