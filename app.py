import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="منصة نُقوش للنفير", page_icon="📍", layout="wide")

# الروابط
raw_url = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/gviz/tq?tqx=out:csv"
form_url = "https://forms.gle/abaLQPeGHi6LjKuu6"

# --- وظيفة جلب البيانات مع التخزين المؤقت لتحسين السرعة ---
@st.cache_data(ttl=300)  # يتم تحديث البيانات كل 5 دقائق فقط بدلاً من كل ثانية
def load_data(url):
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    df.rename(columns={
        'lat': 'latitude', 'long': 'longitude', 
        'lon': 'longitude', 'خط العرض': 'latitude', 
        'خط الطول': 'longitude'
    }, inplace=True, errors='ignore')
    
    # تحويل سريع ومعالجة الإحداثيات
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df['latitude'] = df['latitude'].apply(lambda x: x/10000 if x > 1000 else x)
    df['longitude'] = df['longitude'].apply(lambda x: x/10000 if x > 1000 else x)
    return df.dropna(subset=['latitude', 'longitude'])

# واجهة المستخدم
st.markdown("<h1 style='text-align: center; color: #d32f2f;'>📍 غرفة طوارئ نُقوش</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ خيارات")
    st.link_button("➕ إضافة نداء جديد", form_url, use_container_width=True)
    if st.button("🔄 تحديث البيانات الآن"):
        st.cache_data.clear()  # زر لإجبار التطبيق على جلب البيانات الجديدة فوراً
        st.rerun()

try:
    df = load_data(raw_url)

    if not df.empty:
        # عرض الخريطة الأصلية السريعة
        st.map(df, color="#d32f2f", size=20)
        
        st.write("---")
        col_select, col_table = st.columns([1, 2])
        
        with col_select:
            st.subheader("🎯 توجيه سريع")
            name_col = 'name' if 'name' in df.columns else df.columns[1]
            person = st.selectbox("اختر صاحب النداء:", df[name_col].unique())
            p_data = df[df[name_col] == person].iloc[0]
            g_link = f"https://www.google.com/maps?q={p_data['latitude']},{p_data['longitude']}"
            st.link_button(f"🚗 فتح الموقع في الخريطة", g_link, use_container_width=True)
        
        with col_table:
            st.subheader("📋 كشف البلاغات")
            st.dataframe(df, use_container_width=True, height=250)
            
    else:
        st.warning("🔄 لا توجد بيانات حالياً.")

except Exception as e:
    st.error(f"خطأ تقني: {e}")
