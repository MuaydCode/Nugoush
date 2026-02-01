import streamlit as st
import pandas as pd

st.set_page_config(page_title="منصة نُقوش للنفير", layout="wide")

# الرابط الخاص بك
raw_url = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/gviz/tq?tqx=out:csv"
form_url = "https://forms.gle/abaLQPeGHi6LjKuu6"

@st.cache_data(ttl=60) # تقليل وقت الانتظار لدقيقة واحدة فقط لسرعة التحديث
def load_data(url):
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    # دعم الأسماء العربية والإنجليزية معاً
    df.rename(columns={
        'الاسم': 'name', 'الحوجة': 'need',
        'خط العرض': 'latitude', 'lat': 'latitude',
        'خط الطول': 'longitude', 'long': 'longitude', 'lon': 'longitude'
    }, inplace=True, errors='ignore')
    
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    return df.dropna(subset=['latitude', 'longitude'])

st.markdown("<h1 style='text-align: center; color: #d32f2f;'>📍 غرفة طوارئ نُقوش</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.link_button("➕ إضافة نداء جديد", form_url, use_container_width=True)
    # إضافة زر مسح الكاش للتأكد من جلب الجديد
    if st.button("🔄 جلب البيانات الجديدة الآن"):
        st.cache_data.clear()
        st.rerun()

try:
    df = load_data(raw_url)
    if not df.empty:
        st.map(df)
        st.write("---")
        # عرض الجدول للتأكد من أن البيانات وصلت
        st.subheader("📋 البلاغات المستلمة")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ الجدول متصل ولكن لم يتم العثور على إحداثيات صحيحة. تأكد من ملء خانات latitude و longitude في النموذج.")
except Exception as e:
    st.error(f"خطأ في الاتصال: {e}")
