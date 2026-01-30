import streamlit as st
from streamlit_gsheets import GSheetsConnection
import re

st.set_page_config(page_title="منصة نُقوش السودان", layout="wide", page_icon="🇸🇩")

st.title("🇸🇩 منصة نُقوش: نداءات الاستغاثة")

def parse_coords(text):
    try:
        text = str(text)
        parts = re.findall(r"[-+]?\d*\.\d+|\d+", text)
        if len(parts) >= 6:
            lat = float(parts[0]) + float(parts[1])/60 + float(parts[2])/3600
            lon = float(parts[3]) + float(parts[4])/60 + float(parts[5])/3600
            return lat, lon
        elif len(parts) >= 2:
            return float(parts[0]), float(parts[1])
    except: return None, None
    return None, None

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()

    if not df.empty:
        col = 'رابط الموقع' if 'رابط الموقع' in df.columns else df.columns[2]
        coords = df[col].apply(parse_coords)
        df['lat'] = coords.apply(lambda x: x[0])
        df['lon'] = coords.apply(lambda x: x[1])
        
        df_map = df.dropna(subset=['lat', 'lon'])
        
        if not df_map.empty:
            st.subheader("📍 خريطة النداءات الميدانية")
            st.map(df_map)
            
            st.subheader("📋 تفاصيل النداءات وكيفية الوصول")
            
            # إنشاء رابط مباشر لخرائط جوجل لكل نداء
            for index, row in df_clean.iterrows():
                with st.expander(f"🔴 نداء من: {row['name']}"):
                    st.write(f"**الحاجة:** {row['need']}")
                    google_maps_url = f"https://www.google.com/maps?q={row['lat']},{row['lon']}"
                    st.link_button("🚀 فتح الموقع في خرائط جوجل للوصول", google_maps_url)
        
    else:
        st.info("الجدول متصل وبانتظار البيانات.")
except Exception as e:
    st.error("يرجى التأكد من إعدادات الـ Secrets ومشاركة الجدول.")
