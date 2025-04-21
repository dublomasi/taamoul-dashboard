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

# Google Sheet (CSV)
sheet_url = "https://docs.google.com/spreadsheets/d/1-Ggb6dpLnG708qdp_498uWE3XUpQYIh8f7WBrvPJGEY/export?format=csv"

try:
    df = pd.read_csv(sheet_url)
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.encode("utf-8").str.decode("utf-8")
    df.rename(columns=lambda x: x.strip(), inplace=True)

    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("**Detected columns:**")
    st.code(df.columns.tolist())

    # Optional filters
    if "Playlist" in df.columns:
        playlist = st.selectbox("Filter by Playlist:", ["All"] + sorted(df["Playlist"].dropna().unique()))
        if playlist != "All":
            df = df[df["Playlist"] == playlist]

    if "Language" in df.columns:
        language = st.selectbox("Filter by Language:", ["All"] + sorted(df["Language"].dropna().unique()))
        if language != "All":
            df = df[df["Language"] == language]

    # Safe Metrics
    total_comments = len(df)
    st.metric("Total Comments", total_comments)

    if "Sentiment" in df.columns:
        positive_count = df["Sentiment"].str.lower().eq("positive").sum()
        st.metric("Positive Sentiment", positive_count)
    else:
        st.warning("Missing 'Sentiment' column — metric skipped.")

    if "Suggested Reply" in df.columns:
        pending_replies = df["Suggested Reply"].isna().sum()
        st.metric("Pending Replies", pending_replies)
    else:
        st.warning("Missing 'Suggested Reply' column — metric skipped.")

    st.markdown("---")

    # Safe Pie Chart
    if "Sentiment" in df.columns:
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
        st.info("No 'Sentiment' data to display pie chart.")

    st.markdown("---")

    # Comments Table
    with st.expander("View Comments"):
        display_cols = [col for col in ["Comment", "Sentiment", "Suggested Reply", "Playlist", "Language"] if col in df.columns]
        if display_cols:
            st.dataframe(df[display_cols])
        else:
            st.info("No displayable columns found.")

except Exception as e:
    st.error("❌ Could not load or parse the Google Sheet.")
    st.exception(e)
