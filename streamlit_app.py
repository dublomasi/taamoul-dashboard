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

sheet_url = "https://docs.google.com/spreadsheets/d/1-Ggb6dpLnG708qdp_498uWE3XUpQYIh8f7WBrvPJGEY/export?format=csv"

try:
    df = pd.read_csv(sheet_url)

    # Clean columns
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.encode('utf-8').str.decode('utf-8')

    # Show current time and columns
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("**Detected columns:**")
    st.code(df.columns.tolist())

    # Define available columns
    cols = df.columns.tolist()
    has = lambda name: name in cols

    # Optional filters
    if has("Playlist"):
        playlist_options = ["All"] + sorted(df["Playlist"].dropna().unique())
        selected = st.selectbox("Filter by Playlist", playlist_options)
        if selected != "All":
            df = df[df["Playlist"] == selected]

    if has("Language"):
        lang_options = ["All"] + sorted(df["Language"].dropna().unique())
        selected = st.selectbox("Filter by Language", lang_options)
        if selected != "All":
            df = df[df["Language"] == selected]

    # Metrics
    st.metric("Total Comments", len(df))

    if has("Sentiment"):
        pos_count = df["Sentiment"].astype(str).str.lower().eq("positive").sum()
        st.metric("Positive Sentiment", pos_count)
    else:
        st.warning("No 'Sentiment' column found.")

    if has("Suggested Reply"):
        missing_replies = df["Suggested Reply"].isna().sum()
        st.metric("Pending Replies", missing_replies)
    else:
        st.warning("No 'Suggested Reply' column found.")

    st.markdown("---")

    # Chart
    if has("Sentiment"):
        st.subheader("Sentiment Distribution")
        fig, ax = plt.subplots()
        df["Sentiment"].value_counts().plot.pie(
            autopct="%1.1f%%", startangle=90, counterclock=False, ax=ax
        )
        ax.set_ylabel("")
        st.pyplot(fig)
    else:
        st.info("Sentiment column missing — chart skipped.")

    st.markdown("---")

    # Comments Table
    with st.expander("View Comments"):
        view_cols = [c for c in ["Comment", "Sentiment", "Suggested Reply", "Playlist", "Language"] if has(c)]
        if view_cols:
            st.dataframe(df[view_cols])
        else:
            st.info("No viewable columns available.")

except Exception as e:
    st.error("❌ Could not load or parse the Google Sheet.")
    st.exception(e)
