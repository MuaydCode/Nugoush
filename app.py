import streamlit as st
import pandas as pd

st.set_page_config(page_title="منصة نُقوش", layout="wide")
st.title("📍 خريطة نداءات الاستغاثة - نُقوش")

url = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/gviz/tq?tqx=out:csv"

try:
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()

    # تحويل أسماء الأعمدة لـ latitude و longitude
    rename_dict = {}
    for col in df.columns:
        if 'lat' in col.lower(): rename_dict[col] = 'latitude'
        if 'long' in col.lower() or 'lon' in col.lower(): rename_dict[col] = 'longitude'
    df.rename(columns=rename_dict, inplace=True)

    # --- السطر السحري الجديد ---
    # تحويل القيم في أعمدة الإحداثيات إلى أرقام وحذف أي قيم غير صحيحة
    if 'latitude' in df.columns and 'longitude' in df.columns:
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        df = df.dropna(subset=['latitude', 'longitude'])
    # ---------------------------

    if not df.empty:
        # عرض الخريطة
        st.subheader("🌐 موقع النداء على الخريطة")
        st.map(df)
        
        st.write("---")
        st.subheader("📋 تفاصيل النداءات:")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("البيانات موجودة ولكن الإحداثيات (الأرقام) غير صحيحة. تأكد من كتابة أرقام الطول والعرض بدقة.")

except Exception as e:
    st.error(f"حدث خطأ: {e}")

if st.sidebar.button('🔄 تحديث الخريطة'):
    st.rerun()
