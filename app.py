import streamlit as st
from streamlit_gsheets import GSheetsConnection
import re

st.set_page_config(page_title="منصة نُقوش السودان", layout="wide")
st.title("🇸🇩 منصة نُقوش: نداءات الاستغاثة")

def parse_coords(text):
    try:
        text = str(text)
        # استخراج الأرقام من صيغة (15°34'40.8"N 32°29'08.7"E)
        parts = re.findall(r"[-+]?\d*\.\d+|\d+", text)
        if len(parts) >= 6:
            lat = float(parts[0]) + float(parts[1])/60 + float(parts[2])/3600
            lon = float(parts[3]) + float(parts[4])/60 + float(parts[5])/3600
            return lat, lon
        # إذا كانت إحداثيات عشرية بسيطة
        elif len(parts) >= 2:
            return float(parts[0]), float(parts[1])
    except: return None, None
    return None, None

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()

    if not df.empty:
        # معالجة العمود الثالث (رابط الموقع)
        col = 'رابط الموقع' if 'رابط الموقع' in df.columns else df.columns[2]
        coords = df[col].apply(parse_coords)
        df['lat'] = coords.apply(lambda x: x[0])
        df['lon'] = coords.apply(lambda x: x[1])
        
        df_map = df.dropna(subset=['lat', 'lon'])
        
        if not df_map.empty:
            st.subheader("📍 خريطة النداءات الميدانية")
            st.map(df_map)
        
        st.subheader("📋 تفاصيل النداءات")
        st.dataframe(df[['name', 'need', col]], use_container_width=True)
    else:
        st.info("الجدول متصل وبانتظار البيانات.")
except Exception as e:
    st.error("يرجى التأكد من إعدادات الـ Secrets ومشاركة الجدول.")
