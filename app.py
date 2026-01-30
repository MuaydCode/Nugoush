import streamlit as st
from streamlit_gsheets import GSheetsConnection
import re
import requests

# إعداد الصفحة
st.set_page_config(page_title="منصة نُقوش", layout="wide")
st.title("🇸🇩 منصة نُقوش للنفير الرقمي")

# دالة ذكية لاستخراج الموقع من الرابط
def get_coords(url):
    try:
        # إذا كان الرابط قصيراً، نقوم بفتحه لمعرفة الإحداثيات
        full_url = requests.get(url, allow_redirects=True, timeout=5).url
        match = re.search(r'@([-?\d\.]+),([-?\d\.]+)', full_url)
        if match:
            return float(match.group(1)), float(match.group(2))
    except:
        return None, None
    return None, None

# الربط بقاعدة البيانات
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()

    # التأكد من وجود البيانات
    if not df.empty and 'رابط الموقع' in df.columns:
        with st.spinner('جاري تحديث الخريطة...'):
            # تحويل الروابط إلى نقاط
            df['coords'] = df['رابط الموقع'].apply(get_coords)
            df['lat'] = df['coords'].apply(lambda x: x[0])
            df['lon'] = df['coords'].apply(lambda x: x[1])
            
            # عرض الخريطة
            df_map = df.dropna(subset=['lat', 'lon'])
            if not df_map.empty:
                st.map(df_map)
            
            # عرض الجدول أسفل الخريطة
            st.subheader("📋 النداءات الحالية")
            st.dataframe(df[['name', 'need', 'رابط الموقع']], use_container_width=True)
    else:
        st.info("بانتظار إضافة أول نداء استغاثة في الجدول...")

except Exception as e:
    st.error("خطأ في الربط: تأكد من وضع رابط الجدول الصحيح في Secrets واجعله 'عاماً'")
