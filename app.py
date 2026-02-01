import streamlit as st
import pandas as pd

st.set_page_config(page_title="منصة نُقوش للنفير", layout="wide")

raw_url = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/gviz/tq?tqx=out:csv"
form_url = "https://forms.gle/abaLQPeGHi6LjKuu6"

@st.cache_data(ttl=60)
def load_data(url):
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    
    # تحويل الأسماء للعربية والإنجليزية
    df.rename(columns={
        'الاسم': 'name', 'الحوجة': 'need',
        'خط العرض': 'latitude', 'lat': 'latitude',
        'خط الطول': 'longitude', 'long': 'longitude'
    }, inplace=True, errors='ignore')
    
    # تحويل البيانات لأرقام وحذف غير الصالح منها
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df = df.dropna(subset=['latitude', 'longitude'])
    
    # --- الفلترة السحرية لمنع الخطأ الذي ظهر لك ---
    # سنبقي فقط الأرقام المنطقية لخطوط العرض والطول
    df = df[(df['latitude'] >= -90) & (df['latitude'] <= 90)]
    df = df[(df['longitude'] >= -180) & (df['longitude'] <= 180)]
    
    return df

st.markdown("<h1 style='text-align: center; color: #d32f2f;'>📍 غرفة طوارئ نُقوش</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.link_button("➕ إضافة نداء جديد", form_url, use_container_width=True)
    if st.button("🔄 تحديث الخريطة الآن"):
        st.cache_data.clear()
        st.rerun()

try:
    df = load_data(raw_url)
    
    if not df.empty:
        # عرض الخريطة
        st.map(df)
        
        st.write("---")
        st.subheader("📋 البلاغات المستلمة")
        # عرض الجدول الأصلي كما هو لتعرف أين الخطأ في البيانات
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ لا توجد بيانات صالحة للعرض على الخريطة. تأكد من إدخال الإحداثيات بشكل صحيح (مثال: 15.5006).")

except Exception as e:
    st.error(f"حدث خطأ غير متوقع: {e}")
