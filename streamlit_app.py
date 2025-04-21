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

    # Clean headers
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.encode("utf-8").str.decode("utf-8")

    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("**Detected columns:**")
    st.code(df.columns.tolist())

    # Define original columns
    original_df = df.copy()

    # Optional Filters
    if "Playlist" in df.columns:
        playlist_options = ["All"] + sorted(df["Playlist"].dropna().unique())
        selected_playlist = st.selectbox("Filter by Playlist", playlist_options)
        if selected_playlist != "All":
            df = df[df["Playlist"].astype(str) == selected_playlist]

    if "Language" in df.columns:
        language_options = ["All"] + sorted(df["Language"].dropna().unique())
        selected_language = st.selectbox("Filter by Language", language_options)
        if selected_language != "All":
            df = df[df["Language"].astype(str) == selected_language]

    # Metrics
    st.metric("Total Comments", len(df))

    if "Sentiment" in df.columns:
        pos_count = df["Sentiment"].astype(str).str.lower().eq("positive").sum()
        st.metric("Positive Sentiment", pos_count)
    else:
        st.warning("Missing column: 'Sentiment'")

    if "Suggested Reply" in df.columns:
        pending = df["Suggested Reply"].isna().sum()
        st.metric("Pending Replies", pending)
    else:
        st.warning("Missing column: 'Suggested Reply'")

    st.markdown("---")

    # Pie Chart
    if "Sentiment" in df.columns:
        st.subheader("Sentiment Distribution")
        fig, ax = plt.subplots()
        df["Sentiment"].value_counts().plot.pie(
            autopct="%1.1f%%", startangle=90, counterclock=False, ax=ax
        )
        ax.set_ylabel("")
        st.pyplot(fig)
    else:
        st.info("No sentiment data to show chart.")

    st.markdown("---")

    # Data Table
    with st.expander("View Comments"):
        cols_to_show = [c for c in ["Comment", "Sentiment", "Suggested Reply", "Playlist", "Language"] if c in df.columns]
        if cols_to_show:
            st.dataframe(df[cols_to_show])
        else:
            st.info("No viewable columns available.")

except Exception as e:
    st.error("❌ Could not load or parse the Google Sheet.")
    st.exception(e)
