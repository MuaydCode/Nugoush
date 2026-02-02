import streamlit as st
import pandas as pd
import time

# محاولة استيراد مكتبة الرسوم البيانية، إذا لم توجد لن يتوقف التطبيق
try:
    import plotly.express as px
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

# الرابط الخاص بك (تم تعديله ليعمل من الموبايل تلقائياً)
RAW_URL = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/edit?usp=sharing"

def get_csv_url(url):
    if "/edit" in url:
        return url.split('/edit')[0] + '/export?format=csv'
    return url

st.set_page_config(page_title="غرفة طوارئ نُقوش", layout="wide")

# جلب البيانات
CSV_URL = get_csv_url(RAW_URL)

@st.cache_data(ttl=10)
def load_data():
    try:
        df = pd.read_csv(CSV_URL)
        df.columns = [str(c).strip().lower() for c in df.columns]
        
        # البحث عن أعمدة الإحداثيات (خطوط الطول والعرض)
        lat_col = next((c for c in df.columns if 'عرض' in c or 'lat' in c), None)
        lon_col = next((c for c in df.columns if 'طول' in c or 'lon' in c), None)
        
        if lat_col and lon_col:
            df = df.rename(columns={lat_col: 'lat', lon_col: 'lon'})
            df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
            df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
            return df.dropna(subset=['lat', 'lon'])
        return pd.DataFrame()
    except:
        return pd.DataFrame()

st.title("📍 منصة نُقوش للطوارئ")

df = load_data()

if not df.empty:
    # عرض الخريطة أولاً (الأهم)
    st.map(df[['lat', 'lon']])
    
    # عرض الإحصائيات إذا كانت المكتبة موجودة
    if HAS_PLOTLY and 'need' in df.columns:
        st.write("---")
        fig = px.pie(df, names='need', title='توزيع الاحتياجات')
        st.plotly_chart(fig)
    
    st.write("### 📋 سجل البلاغات")
    st.dataframe(df)
else:
    st.error("⚠️ لم نتمكن من قراءة الإحداثيات. تأكد من وجود أعمدة باسم (خط العرض) و (خط الطول) في جدولك.")

if st.button("🔄 تحديث البيانات"):
    st.cache_data.clear()
    st.rerun()
