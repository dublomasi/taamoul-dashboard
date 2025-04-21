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

    # Clean up headers
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.encode("utf-8").str.decode("utf-8")
    df.rename(columns=lambda x: x.strip(), inplace=True)

    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("**Detected columns:**")
    st.code(df.columns.tolist())

    # Get columns safely
    comment_col = df.get("Comment")
    sentiment_col = df.get("Sentiment")
    reply_col = df.get("Suggested Reply")
    playlist_col = df.get("Playlist")
    language_col = df.get("Language")

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
        pos_count = sentiment_col.astype(str).str.lower().eq("positive").sum()
        st.metric("Positive Sentiment", pos_count)
    else:
        st.warning("Missing column: 'Sentiment'")

    if reply_col is not None:
        pending = reply_col.isna().sum()
        st.metric("Pending Replies", pending)
    else:
        st.warning("Missing column: 'Suggested Reply'")

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
        st.info("No sentiment data to show chart.")

    st.markdown("---")

    # Data Table
    with st.expander("View Comments"):
        cols_to_show = []
        if comment_col is not None: cols_to_show.append("Comment")
        if sentiment_col is not None: cols_to_show.append("Sentiment")
        if reply_col is not None: cols_to_show.append("Suggested Reply")
        if playlist_col is not None: cols_to_show.append("Playlist")
        if language_col is not None: cols_to_show.append("Language")

        if cols_to_show:
            st.dataframe(df[cols_to_show])
        else:
            st.info("No viewable columns.")

except Exception as e:
    st.error("❌ Could not load or parse the Google Sheet.")
    st.exception(e)
