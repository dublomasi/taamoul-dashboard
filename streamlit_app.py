import streamlit as st
import pandas as pd
# Optional: only enable if matplotlib is installed
# import matplotlib.pyplot as plt

# ====== Layout & Branding ======

st.set_page_config(page_title="Taamoul HQ", layout="wide")

# Logo (local image file)
st.image("assets/taamoul-logo.png", width=150)

st.title("Taamoul HQ – YouTube Comment Agent")
st.caption("Last updated: 2025-04-22 03:49:55")

# ====== Load Data ======

# You can replace this with your actual data source
df = pd.read_csv("comments.csv")  # or any other source

# ====== Detected Columns Display ======
st.markdown("### Detected columns:")
st.code(list(df.columns))

# ====== Filters ======
col1, col2 = st.columns(2)
with col1:
    playlist_filter = st.selectbox("Filter by Playlist", ["All"] + sorted(df["Playlist"].unique().tolist()))
with col2:
    lang_filter = st.selectbox("Filter by Language", ["All"] + sorted(df["Language"].unique().tolist()))

filtered_df = df.copy()
if playlist_filter != "All":
    filtered_df = filtered_df[filtered_df["Playlist"] == playlist_filter]
if lang_filter != "All":
    filtered_df = filtered_df[filtered_df["Language"] == lang_filter]

# ====== Display Data ======
st.markdown("### Filtered Comments")
st.dataframe(filtered_df, use_container_width=True)

# ====== Optional Sentiment Chart ======
# Uncomment after matplotlib is installed
# sentiment_counts = filtered_df["Sentiment"].value_counts()
# fig, ax = plt.subplots()
# sentiment_counts.plot(kind="bar", ax=ax, color="skyblue")
# ax.set_title("Sentiment Breakdown")
# st.pyplot(fig)

# ====== Footer ======
st.markdown("---")
st.markdown("Made with ❤️ by Yousuf | taamoul.streamlit.app")
