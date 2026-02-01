import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="غرفة طوارئ نُقوش", page_icon="📍", layout="wide")

# الرابط الخاص بك
CSV_URL = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/gviz/tq?tqx=out:csv"
FORM_URL = "https://forms.gle/abaLQPeGHi6LjKuu6"

@st.cache_data(show_spinner=False)
def get_clean_data():
    try:
        # إضافة توقيت لمنع الكاش القديم
        t = int(time.time())
        df = pd.read_csv(f"{CSV_URL}&v={t}").dropna(how='all')
        
        # تنظيف العناوين
        df.columns = [str(c).strip() for c in df.columns]
        
        # خريطة تحويل الأسماء (عربي وإنجليزي)
        mapping = {
            'الاسم': 'name', 'اسم المتضرر': 'name',
            'الحوجة': 'need', 'نوع الحوجة': 'need',
            'رقم الهاتف': 'phone', 'الهاتف': 'phone',
            'خط العرض': 'lat', 'latitude': 'lat',
            'خط الطول': 'lon', 'longitude': 'lon'
        }
        df.rename(columns=mapping, inplace=True, errors='ignore')

        # تحويل الأرقام
        df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
        df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
        
        # تنظيف الصفوف التي ليس بها إحداثيات
        df = df.dropna(subset=['lat', 'lon'])
        return df
    except Exception as e:
        return pd.DataFrame()

# التصميم
st.markdown("<h1 style='text-align: center; color: #d32f2f;'>📍 منصة نُقوش للطوارئ</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.link_button("➕ إضافة بلاغ جديد", FORM_URL, use_container_width=True)
    if st.button("🔄 تحديث البيانات", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    search = st.text_input("🔍 ابحث هنا:")

df = get_clean_data()

if not df.empty:
    # عرض الخريطة
    st.map(df[['lat', 'lon']])
    
    st.write("---")
    # عرض البيانات في بطاقات
    for _, row in df.iterrows():
        # التأكد من وجود البيانات أو وضع نص افتراضي
        n = row.get('name', 'بدون اسم')
        h = row.get('need', 'بلاغ طوارئ')
        p = str(row.get('phone', ''))
        
        if search.lower() in str(n).lower() or search.lower() in str(h).lower():
            with st.expander(f"🔴 {n} | {h}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"📞 {p}")
                    st.markdown(f'<a href="tel:{p}" style="color:white; background:green; padding:5px 15px; border-radius:5px; text-decoration:none;">اتصال مباشر</a>', unsafe_allow_html=True)
                with col2:
                    g_map = f"https://www.google.com/maps?q={row['lat']},{row['lon']}"
                    st.link_button("🚗 فتح في الخرائط", g_map)
else:
    st.warning("⚠️ لم يتم العثور على بيانات. تأكد من أن الجدول يحتوي على بلاغات بإحداثيات صحيحة.")
    # سأعرض لك الجدول الخام هنا لتكتشف أين المشكلة في العناوين
    st.write("البيانات المستلمة من الجدول (للفحص):")
    raw_df = pd.read_csv(CSV_URL)
    st.dataframe(raw_df)

st.caption("نُقوش 2026")
