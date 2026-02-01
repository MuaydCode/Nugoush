import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="غرفة طوارئ نُقوش", page_icon="📍", layout="wide")

# الروابط
CSV_URL = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/gviz/tq?tqx=out:csv"
FORM_URL = "https://forms.gle/abaLQPeGHi6LjKuu6"

@st.cache_data(show_spinner=False)
def load_data():
    try:
        # إضافة متغير زمني لمنع النسخ القديمة
        df = pd.read_csv(f"{CSV_URL}&cache={int(time.time())}").dropna(how='all')
        df.columns = [str(c).strip() for c in df.columns]
        
        # تحويل أسماء الأعمدة لتسهيل القراءة
        mapping = {
            'الاسم': 'name', 'الحوجة': 'need', 'رقم الهاتف': 'phone',
            'latitude': 'lat', 'longitude': 'lon', 'خط العرض': 'lat', 'خط الطول': 'lon'
        }
        df.rename(columns=mapping, inplace=True, errors='ignore')
        
        # تحويل الإحداثيات وحذف التالف
        df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
        df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
        return df
    except:
        return pd.DataFrame()

st.markdown("<h1 style='text-align: center; color: #d32f2f;'>📍 منصة نُقوش للطوارئ</h1>", unsafe_allow_html=True)

# القائمة الجانبية
with st.sidebar:
    st.link_button("➕ إضافة بلاغ جديد", FORM_URL, use_container_width=True)
    if st.button("🔄 تحديث البيانات", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

df = load_data()

# فحص البيانات الصالحة للخريطة
valid_map_data = df.dropna(subset=['lat', 'lon'])

if not valid_map_data.empty:
    st.map(valid_map_data[['lat', 'lon']])
    st.write("---")
    st.subheader(f"📋 البلاغات النشطة ({len(valid_map_data)})")
    
    # عرض البلاغات
    for _, row in valid_map_data.iterrows():
        with st.expander(f"🔴 {row.get('name', 'بلاغ')} | {row.get('need', 'طوارئ')}"):
            st.write(f"📞 الهاتف: {row.get('phone', 'غير متوفر')}")
            g_link = f"https://www.google.com/maps?q={row['lat']},{row['lon']}"
            st.link_button("🚗 فتح الموقع في الخرائط", g_link)
else:
    st.error("⚠️ لم تظهر الخريطة لأنه لا توجد إحداثيات (خط عرض وطول) صحيحة في الجدول.")
    st.info("إليك ما قرأه البرنامج من الجدول حالياً، تأكد من وجود أرقام في أعمدة الإحداثيات:")
    st.dataframe(df) # هذا سيظهر لك الجدول كما يراه الكود حالياً

st.caption("نُقوش 2026")
