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

# Live Google Sheet
sheet_url = "https://docs.google.com/spreadsheets/d/1-Ggb6dpLnG708qdp_498uWE3XUpQYIh8f7WBrvPJGEY/export?format=csv"

try:
    df = pd.read_csv(sheet_url)
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.encode('utf-8').str.decode('utf-8')
    df.rename(columns=lambda x: x.strip(), inplace=True)

    # Debug: show actual columns
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("**Loaded columns:**")
    st.code(df.columns.tolist())

    # Validate required columns
    required_columns = ["Comment", "Sentiment", "Suggested Reply"]
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        st.error(f"❌ Missing columns in sheet: {', '.join(missing)}")
    else:
        # Optional filters
        if "Playlist" in df.columns:
            playlist = st.selectbox("Filter by Playlist:", ["All"] + sorted(df["Playlist"].dropna().unique()))
            if playlist != "All":
                df = df[df["Playlist"] == playlist]

        if "Language" in df.columns:
            lang = st.selectbox("Filter by Language:", ["All"] + sorted(df["Language"].dropna().unique()))
            if lang != "All":
                df = df[df["Language"] == lang]

        # Metrics
        st.metric("Total Comments", len(df))
        st.metric("Positive Sentiment", len(df[df["Sentiment"].str.lower() == "positive"]))
        st.metric("Pending Replies", df["Suggested Reply"].isna().sum())

        st.markdown("---")

        # Sentiment Pie Chart
        st.subheader("Sentiment Distribution")
        fig, ax = plt.subplots()
        df["Sentiment"].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, counterclock=False, ax=ax)
        ax.set_ylabel('')
        st.pyplot(fig)

        st.markdown("---")

        # Expandable Data Table
        with st.expander("View Comments"):
            display_cols = ["Comment", "Sentiment", "Suggested Reply"]
            if "Playlist" in df.columns:
                display_cols.append("Playlist")
            if "Language" in df.columns:
                display_cols.append("Language")
            st.dataframe(df[display_cols])

except Exception as e:
    st.error("❌ Failed to load or display data.")
    st.exception(e)
