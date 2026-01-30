import streamlit as st
from streamlit_gsheets import GSheetsConnection
import re
import requests

st.set_page_config(page_title="منصة نُقوش السودان", page_icon="🇸🇩", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .main-title { color: #008751; text-align: center; font-size: 40px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🇸🇩 منصة نُقوش: نداءات الاستغاثة</p>', unsafe_allow_html=True)

# دالة سحرية لاستخراج الإحداثيات من أي نص أو رابط
def extract_coords(text):
    try:
        text = str(text)
        # إذا كان رابطاً من خرائط جوجل
        if "http" in text:
            full_url = requests.get(text, allow_redirects=True, timeout=3).url
            match = re.search(r'@([-?\d\.]+),([-?\d\.]+)', full_url)
            if match: return float(match.group(1)), float(match.group(2))
        
        # إذا كانت إحداثيات نصية (مثل التي أرسلتها أنت)
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", text)
        if len(numbers) >= 2:
            return float(numbers[0]), float(numbers[1])
    except: return None, None
    return None, None

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()

    if not df.empty:
        # معالجة البيانات
        coords = df['رابط الموقع'].apply(extract_coords)
        df['lat'] = coords.apply(lambda x: x[0])
        df['lon'] = coords.apply(lambda x: x[1])
        df_clean = df.dropna(subset=['lat', 'lon'])

        # عرض الخريطة بشكل احترافي
        st.subheader("📍 خريطة النداءات النشطة")
        st.map(df_clean)

        # عرض الجدول
        st.subheader("📋 تفاصيل الاحتياجات")
        st.dataframe(df[['name', 'need', 'رابط الموقع']], use_container_width=True)
    else:
        st.info("لا توجد نداءات حالياً. المنصة جاهزة لاستقبال الاستغاثات.")

except Exception as e:
    st.error("يرجى التأكد من اتصال الإنترنت أو إعدادات الربط.")

st.sidebar.title("عن منصة نُقوش")
st.sidebar.info("هذه المنصة تهدف لربط المتطوعين بالمحتاجين في السودان عبر تحديد المواقع بدقة.")
