import streamlit as st
import pandas as pd

# تعيين الصفحة أولاً
st.set_page_config(page_title="Nugoush Test")

st.title("Testing Connection...")

# رابط مباشر ومبسط
sheet_id = "1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    # محاولة القراءة
    df = pd.read_csv(url)
    st.success("Connected to Data!")
    st.write("Columns found:", list(df.columns))
    st.dataframe(df.head())
except Exception as e:
    st.error(f"Critical Error: {e}")
