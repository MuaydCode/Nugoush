import streamlit as st
from streamlit_gsheets import GSheetsConnection
import re

st.set_page_config(page_title="منصة نُقوش السودان", page_icon="🇸🇩", layout="wide")

st.title("🇸🇩 منصة نُقوش: نداءات الاستغاثة")

# دالة بسيطة جداً لاستخراج الأرقام من النص
def simple_extract(text):
    try:
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", str(text))
        if len(numbers) >= 2:
            return float(numbers[0]), float(numbers[1])
    except:
        return None, None
    return None, None

try:
    # الاتصال بالجدول
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()

    if not df.empty:
        # تحويل "رابط الموقع" إلى إحداثيات
        coords = df['رابط الموقع'].apply(simple_extract)
        df['lat'] = coords.apply(lambda x: x[0])
        df['lon'] = coords.apply(lambda x: x[1])
        
        # عرض الخريطة للنداءات التي تحتوي على موقع صحيح
        df_map = df.dropna(subset=['lat', 'lon'])
        
        if not df_map.empty:
            st.subheader("📍 خريطة النداءات")
            st.map(df_map)
        
        st.subheader("📋 قائمة النداءات")
        st.dataframe(df[['name', 'need', 'رابط الموقع']], use_container_width=True)
    else:
        st.info("الجدول متصل ولكنه فارغ.")

except Exception as e:
    st.error("⚠️ مشكلة في الربط: تأكد من أن رابط الجدول في Secrets صحيح وأن الملف متاح للجميع (Anyone with link).")
