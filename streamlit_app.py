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

# Google Sheet (CSV export)
sheet_url = "https://docs.google.com/spreadsheets/d/1-Ggb6dpLnG708qdp_498uWE3XUpQYIh8f7WBrvPJGEY/export?format=csv"

try:
    df = pd.read_csv(sheet_url)

    # Clean headers
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.encode("utf-8").str.decode("utf-8")
    df.rename(columns=lambda x: x.strip(), inplace=True)

    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("**Detected columns:**")
    st.code(df.columns.tolist())

    # Filter safely only if Playlist & Language exist
    if "Playlist" in df.columns:
        playlist = st.selectbox("Filter by Playlist:", ["All"] + sorted(df["Playlist"].dropna().unique()))
        if playlist != "All":
            df = df[df["Playlist"] == playlist]

    if "Language" in df.columns:
        language = st.selectbox("Filter by Language:", ["All"] + sorted(df["Language"].dropna().unique()))
        if language != "All":
            df = df[df["Language"] == language]

    # Check before metrics
    comment_col = "Comment" in df.columns
    sentiment_col = "Sentiment" in df.columns
    reply_col = "Suggested Reply" in df.columns

    if sentiment_col and reply_col:
        st.metric("Total Comments", len(df))
        st.metric("Positive Sentiment", len(df[df["Sentiment"].str.lower() == "positive"]))
        st.metric("Pending Replies", df["Suggested Reply"].isna().sum())

        st.markdown("---")

        # Pie Chart
        st.subheader("Sentiment Distribution")
        fig, ax = plt.subplots()
        df["Sentiment"].value_counts().plot.pie(
            autopct='%1.1f%%',
            startangle=90,
            counterclock=False,
            ax=ax
        )
        ax.set_ylabel("")
        st.pyplot(fig)
    else:
        st.warning("Some required columns (Sentiment or Suggested Reply) are missing. Pie chart and metrics skipped.")

    st.markdown("---")

    # Safe comment viewer
    with st.expander("View Comments"):
        available_cols = [col for col in ["Comment", "Sentiment", "Suggested Reply", "Playlist", "Language"] if col in df.columns]
        if available_cols:
            st.dataframe(df[available_cols])
        else:
            st.info("No displayable columns found.")

except Exception as e:
    st.error("❌ Could not load or parse the Google Sheet.")
    st.exception(e)
