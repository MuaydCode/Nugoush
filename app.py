import streamlit as st
from streamlit_gsheets import GSheetsConnection
import re

# إعداد واجهة المنصة
st.set_page_config(page_title="منصة نُقوش", layout="wide")
st.title("🇸🇩 منصة نُقوش للنفير الرقمي")

# دالة لاستخراج الإحداثيات من رابط جوجل
def extract_lat_lon(url):
    try:
        if not url: return None, None
        match = re.search(r'@([-?\d\.]+),([-?\d\.]+)', str(url))
        if match:
            return float(match.group(1)), float(match.group(2))
    except: return None, None
    return None, None

# الاتصال بالجدول
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()

    if not df.empty and 'رابط الموقع' in df.columns:
        # تحويل الروابط إلى نقاط على الخريطة
        coords = df['رابط الموقع'].apply(extract_lat_lon)
        df['lat'] = coords.apply(lambda x: x[0])
        df['lon'] = coords.apply(lambda x: x[1])
        
        # عرض الخريطة
        st.subheader("📍 خريطة الاستغاثة")
        st.map(df.dropna(subset=['lat', 'lon']))
        
        # عرض البيانات
        st.subheader("📋 النداءات المسجلة")
        st.dataframe(df[['name', 'need', 'رابط الموقع']], use_container_width=True)
    else:
        st.info("بانتظار إضافة أول نداء استغاثة عبر الرابط.")
except:
    st.error("يرجى التأكد من إعدادات الربط (Secrets)")
