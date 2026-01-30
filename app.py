import streamlit as st
from streamlit_gsheets import GSheetsConnection
import re

st.set_page_config(page_title="منصة نُقوش السودان", layout="wide", page_icon="🇸🇩")

st.title("🇸🇩 منصة نُقوش: نداءات الاستغاثة")

# دالة معالجة الإحداثيات
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

# محاولة الربط
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # نقوم بتحديد اسم الورقة إذا لزم الأمر، أو القراءة المباشرة
    df = conn.read()

    if df is not None and not df.empty:
        # تحديد الأعمدة (حتى لو تغيرت أسماؤها)
        name_col = 'name' if 'name' in df.columns else df.columns[0]
        need_col = 'need' if 'need' in df.columns else df.columns[1]
        loc_col = 'رابط الموقع' if 'رابط الموقع' in df.columns else df.columns[2]

        # معالجة المواقع
        coords = df[loc_col].apply(parse_coords)
        df['lat'] = coords.apply(lambda x: x[0])
        df['lon'] = coords.apply(lambda x: x[1])
        
        df_clean = df.dropna(subset=['lat', 'lon'])
        
        if not df_clean.empty:
            st.subheader("📍 خريطة النداءات النشطة")
            st.map(df_clean[['lat', 'lon']])
            
            st.subheader("📋 تفاصيل النداءات وكيفية الوصول")
            for index, row in df_clean.iterrows():
                with st.expander(f"🔴 نداء من: {row[name_col]}"):
                    st.write(f"**الحاجة:** {row[need_col]}")
                    # رابط خرائط جوجل المباشر
                    g_url = f"https://www.google.com/maps?q={row['lat']},{row['lon']}"
                    st.link_button("🚀 فتح في خرائط جوجل للوصول للبيت", g_url)
        else:
            st.info("بانتظار إضافة إحداثيات صحيحة في الجدول.")
    else:
        st.info("الجدول متصل ولكنه فارغ.")

except Exception as e:
    st.error("⚠️ خطأ في الربط: يرجى التأكد من الـ Secrets ومشاركة الجدول.")
    st.info("تأكد أن الملف في جوجل شيت متاح 'لأي شخص لديه الرابط' (Viewer).")
