import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="غرفة طوارئ نُقوش", page_icon="📍", layout="wide")

# الرابط (تأكد من عمل Publish to web بصيغة CSV)
CSV_URL = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/pub?output=csv"
FORM_URL = "https://forms.gle/abaLQPeGHi6LjKuu6"

@st.cache_data(ttl=10)
def load_data():
    try:
        # إضافة متغير لمنع التخزين القديم
        df = pd.read_csv(f"{CSV_URL}&cache={int(time.time())}")
        df.columns = [str(c).strip() for c in df.columns]
        
        # بحث ذكي عن الأعمدة
        for col in df.columns:
            if 'عرض' in col or 'lat' in col.lower():
                df.rename(columns={col: 'lat'}, inplace=True)
            if 'طول' in col or 'lon' in col.lower() or 'lng' in col.lower():
                df.rename(columns={col: 'lon'}, inplace=True)
            if 'اسم' in col or 'name' in col.lower():
                df.rename(columns={col: 'name'}, inplace=True)
            if 'هاتف' in col or 'phone' in col.lower() or 'موبايل' in col.lower():
                df.rename(columns={col: 'phone'}, inplace=True)
            if 'حوجة' in col or 'need' in col.lower():
                df.rename(columns={col: 'need'}, inplace=True)

        # تحويل وتنظيف
        df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
        df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
        return df.dropna(subset=['lat', 'lon'])
    except Exception as e:
        st.error(f"فشل جلب البيانات: {e}")
        return pd.DataFrame()

# التصميم
st.markdown("<h1 style='text-align: center; color: #d32f2f;'>📍 منصة نُقوش للطوارئ</h1>", unsafe_allow_html=True)

df = load_data()

# القائمة الجانبية
with st.sidebar:
    st.markdown("### 🛠 الإدارة")
    st.link_button("➕ إضافة بلاغ", FORM_URL, use_container_width=True)
    if st.button("🔄 تحديث فوري", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.write("---")
    search = st.text_input("🔍 بحث بالاسم أو النوع:")

# عرض النتائج
if not df.empty:
    if search:
        df = df[df.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
    
    # الخريطة
    st.map(df[['lat', 'lon']])
    
    # القائمة التفاعلية
    st.write("---")
    for _, row in df.iterrows():
        with st.expander(f"🔴 {row.get('name', 'بلاغ')} | {row.get('need', 'طوارئ')}"):
            c1, c2 = st.columns(2)
            p = str(row.get('phone', ''))
            with c1:
                st.markdown(f'<a href="tel:{p}" style="display:block; text-align:center; background:#28a745; color:white; padding:10px; border-radius:10px; text-decoration:none;">📞 اتصال {p}</a>', unsafe_allow_html=True)
            with c2:
                st.link_button("🚗 توجيه GPS", f"https://www.google.com/maps?q={row['lat']},{row['lon']}", use_container_width=True)
else:
    st.warning("⚠️ لا توجد بلاغات حالياً. تأكد من أن الجدول يحتوي على أرقام في أعمدة الإحداثيات.")
    # عرض الجدول للتأكد من وصول البيانات
    st.write("بيانات الجدول (تأكد من وجود أرقام تحت خط الطول والعرض):")
    st.dataframe(pd.read_csv(CSV_URL))
