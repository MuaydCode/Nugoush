import streamlit as st
import pandas as pd

# إعدادات سريعة
st.set_page_config(page_title="نُقوش", layout="wide")

# الروابط (تم التأكد منها)
url = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/gviz/tq?tqx=out:csv"
form_url = "https://forms.gle/abaLQPeGHi6LjKuu6"

st.markdown("<h2 style='text-align: center;'>📍 غرفة طوارئ نُقوش</h2>", unsafe_allow_html=True)

# تحسين جلب البيانات (تجاهل الأخطاء فوراً)
@st.cache_data(ttl=60)
def get_fast_data(link):
    try:
        data = pd.read_csv(link)
        # الاحتفاظ فقط بالأعمدة المهمة لتقليل الوزن
        data.rename(columns={'خط العرض': 'lat', 'خط الطول': 'lon', 'latitude': 'lat', 'longitude': 'lon'}, inplace=True)
        # تحويل الإحداثيات وحذف أي شيء غير رقمي فوراً
        data['lat'] = pd.to_numeric(data['lat'], errors='coerce')
        data['lon'] = pd.to_numeric(data['lon'], errors='coerce')
        # فلترة صارمة: فقط الأرقام الصحيحة للسودان وما حوله
        return data.dropna(subset=['lat', 'lon'])
    except:
        return pd.DataFrame()

df = get_fast_data(url)

# القائمة الجانبية
st.sidebar.link_button("➕ إضافة بلاغ", form_url)
if st.sidebar.button("🔄 تحديث"):
    st.cache_data.clear()
    st.rerun()

# العرض
if not df.empty:
    # عرض الخريطة بأبسط شكل ممكن (أسرع طريقة)
    st.map(df[['lat', 'lon']])
    st.write("---")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("الخريطة جاهزة.. بانتظار بيانات إحداثيات صحيحة من الجدول.")
