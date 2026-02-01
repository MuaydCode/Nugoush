import streamlit as st
import pandas as pd

st.set_page_config(page_title="منصة نُقوش", layout="wide")
st.title("📍 خريطة نداءات الاستغاثة - نُقوش")

url = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/gviz/tq?tqx=out:csv"

try:
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()

    # تحويل الأسماء
    rename_dict = {}
    for col in df.columns:
        if 'lat' in col.lower(): rename_dict[col] = 'latitude'
        if 'long' in col.lower() or 'lon' in col.lower(): rename_dict[col] = 'longitude'
    df.rename(columns=rename_dict, inplace=True)

    if 'latitude' in df.columns and 'longitude' in df.columns:
        # تحويل لـ فلوت ومعالجة الأرقام الكبيرة (بدون نقطة)
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')

        # حركة ذكية: إذا كان الرقم أكبر من 1000 (معناه نسيت النقطة)، قسمه ليوضع في مكانه الصح
        df['latitude'] = df['latitude'].apply(lambda x: x/10000 if x > 1000 else x)
        df['longitude'] = df['longitude'].apply(lambda x: x/10000 if x > 1000 else x)
        
        df = df.dropna(subset=['latitude', 'longitude'])

        if not df.empty:
            st.map(df)
            st.dataframe(df)
        else:
            st.error("البيانات لا تزال غير صالحة للخريطة.")
except Exception as e:
    st.error(f"خطأ: {e}")
