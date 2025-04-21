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

    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.encode("utf-8").str.decode("utf-8")

    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("**Detected columns:**")
    st.code(df.columns.tolist())

    # Safe columns
    playlist_col = df.get("Playlist")
    language_col = df.get("Language")
    sentiment_col = df.get("Sentiment")
    reply_col = df.get("Suggested Reply")
    comment_col = df.get("Comment")

    # Filters
    if playlist_col is not None:
        selected_playlist = st.selectbox("Filter by Playlist", ["All"] + sorted(playlist_col.dropna().unique()))
        if selected_playlist != "All":
            df = df[playlist_col == selected_playlist]

    if language_col is not None:
        selected_language = st.selectbox("Filter by Language", ["All"] + sorted(language_col.dropna().unique()))
        if selected_language != "All":
            df = df[language_col == selected_language]

    # Metrics
    st.metric("Total Comments", len(df))

    if sentiment_col is not None:
        pos_count = sentiment_col.astype(str).str.lower().eq("positive").sum()
        st.metric("Positive Sentiment", pos_count)
    else:
        st.warning("Missing 'Sentiment' column")

    if reply_col is not None:
        missing_replies = reply_col.isna().sum()
        st.metric("Pending Replies", missing_replies)
    else:
        st.warning("Missing 'Suggested Reply' column")

    st.markdown("---")

    # Pie Chart
    if sentiment_col is not None:
        st.subheader("Sentiment Distribution")
        fig, ax = plt.subplots()
        sentiment_col.value_counts().plot.pie(
            autopct="%1.1f%%", startangle=90, counterclock=False, ax=ax
        )
        ax.set_ylabel("")
        st.pyplot(fig)
    else:
        st.info("No sentiment data available for chart.")

    st.markdown("---")

    # Data Table
    with st.expander("View Comments"):
        display = {}
        if comment_col is not None:
            display["Comment"] = comment_col
        if sentiment_col is not None:
            display["Sentiment"] = sentiment_col
        if reply_col is not None:
            display["Suggested Reply"] = reply_col
        if playlist_col is not None:
            display["Playlist"] = playlist_col
        if language_col is not None:
            display["Language"] = language_col

        if display:
            result_df = pd.DataFrame(display)
            st.dataframe(result_df)
        else:
            st.info("No columns available to show.")

except Exception as e:
    st.error("❌ Could not load or parse the Google Sheet.")
    st.exception(e)
