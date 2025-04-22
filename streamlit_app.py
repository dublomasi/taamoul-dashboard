import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt  # فعّل إذا كنت تريد رسم بياني

# إعداد الصفحة
st.set_page_config(page_title="Taamoul HQ", layout="wide")

# شعار محلي – تأكد من وجود الملف داخل مجلد assets
st.image("assets/taamoul-logo.png", width=150)

# عنوان الصفحة
st.title("Taamoul HQ – YouTube Comment Agent")
st.caption("Last updated: 2025-04-22 03:49:55")

# تحميل البيانات
df = pd.read_csv("comments.csv")

# عرض الأعمدة المكتشفة
st.markdown("### Detected columns:")
st.code(list(df.columns))

# ====== إحصائيات سريعة (Metrics) ======
st.markdown("### Dashboard Overview")
total_comments = len(df)
positive_comments = len(df[df["Sentiment"] == "positive"])
negative_comments = len(df[df["Sentiment"] == "negative"])
neutral_comments = len(df[df["Sentiment"] == "neutral"])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Comments", total_comments)
col2.metric("Positive", positive_comments)
col3.metric("Negative", negative_comments)
col4.metric("Neutral", neutral_comments)

# ====== فلاتر ======
col5, col6 = st.columns(2)
with col5:
    playlist_filter = st.selectbox("Filter by Playlist", ["All"] + sorted(df["Playlist"].dropna().unique().tolist()))
with col6:
    lang_filter = st.selectbox("Filter by Language", ["All"] + sorted(df["Language"].dropna().unique().tolist()))

# ====== تطبيق الفلاتر ======
filtered_df = df.copy()
if playlist_filter != "All":
    filtered_df = filtered_df[filtered_df["Playlist"] == playlist_filter]
if lang_filter != "All":
    filtered_df = filtered_df[filtered_df["Language"] == lang_filter]

# ====== عرض البيانات ======
st.markdown("### Filtered Comments")
st.dataframe(filtered_df, use_container_width=True)

# ====== رسم بياني اختياري ======
# sentiment_counts = filtered_df["Sentiment"].value_counts()
# fig, ax = plt.subplots()
# sentiment_counts.plot(kind="bar", ax=ax, color="skyblue")
# ax.set_title("Sentiment Breakdown")
# st.pyplot(fig)

# ====== التذييل ======
st.markdown("---")
st.markdown("Made with ❤️ by Yousuf | taamoul.streamlit.app")
