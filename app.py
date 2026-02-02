import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="نُقوش للطوارئ", layout="wide")

# 2. رابط البيانات (المعدل للتحميل المباشر)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/export?format=csv"

st.title("📍 منصة نُقوش للنفير الرقمي")

# 3. دالة جلب البيانات
@st.cache_data(ttl=5)
def get_data():
    try:
        # قراءة الملف مباشرة
        df = pd.read_csv(SHEET_URL)
        # توحيد أسماء الأعمدة (حذف المسافات وتحويلها لصغير)
        df.columns = [str(c).strip().lower() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"فشل الاتصال بجدول البيانات: {e}")
        return pd.DataFrame()

df = get_data()

# 4. عرض النتائج للتشخيص
if not df.empty:
    st.success("✅ تم الاتصال بجدول البيانات بنجاح!")
    
    # البحث عن أعمدة الإحداثيات
    lat_col = next((c for c in df.columns if 'عرض' in c or 'lat' in c), None)
    lon_col = next((c for c in df.columns if 'طول' in c or 'lon' in c), None)

    if lat_col and lon_col:
        # تحويل الأرقام ورسم الخريطة
        df[lat_col] = pd.to_numeric(df[lat_col], errors='coerce')
        df[lon_col] = pd.to_numeric(df[lon_col], errors='coerce')
        map_df = df.dropna(subset=[lat_col, lon_col])
        
        st.subheader("🗺️ خريطة البلاغات")
        st.map(map_df.rename(columns={lat_col: 'lat', lon_col: 'lon'}))
    else:
        st.warning("⚠️ تم جلب البيانات ولكن لم أجد أعمدة باسم 'lat' و 'lon' أو 'عرض' و 'طول'.")
    
    st.subheader("📋 البيانات الواردة:")
    st.dataframe(df)
else:
    st.info("بانتظار وصول البيانات من Google Sheets...")

if st.button("🔄 تحديث"):
    st.cache_data.clear()
    st.rerun()
