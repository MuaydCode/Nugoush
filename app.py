import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="منصة نُقوش", layout="wide")

# الرابط الخاص بك (تم التأكد من تحويله لـ CSV)
URL = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/export?format=csv"

st.title("📍 غرفة طوارئ نُقوش")
st.markdown("---")

def load_data():
    try:
        # قراءة البيانات مع تجاهل الأخطاء في الصفوف
        df = pd.read_csv(URL, on_bad_lines='skip')
        
        # تنظيف أسماء الأعمدة
        df.columns = [str(c).strip().lower() for c in df.columns]
        
        # البحث عن الأعمدة (عربي وإنجليزي)
        lat_col = next((c for c in df.columns if 'عرض' in c or 'lat' in c), None)
        lon_col = next((c for c in df.columns if 'طول' in c or 'lon' in c), None)
        
        if lat_col and lon_col:
            df = df.rename(columns={lat_col: 'lat', lon_col: 'lon'})
            df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
            df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
            return df.dropna(subset=['lat', 'lon'])
        return df # إرجاع الجدول حتى لو لم تكن هناك إحداثيات للتشخيص
    except Exception as e:
        st.error(f"عذراً، هناك مشكلة في الاتصال بالبيانات: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # إذا وجدت إحداثيات، ارسم الخريطة
    if 'lat' in df.columns and 'lon' in df.columns:
        st.subheader("🗺️ خريطة البلاغات الحية")
        st.map(df[['lat', 'lon']])
    
    st.write("---")
    st.subheader("📑 قائمة البيانات المستلمة")
    st.dataframe(df)
else:
    st.info("جاري انتظار البيانات من قوقل شيت... تأكد من أن الجدول ليس فارغاً.")

if st.button("🔄 تحديث البيانات الآن"):
    st.cache_data.clear()
    st.rerun()
