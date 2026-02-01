import streamlit as st
import pandas as pd

# إعداد الصفحة لتكون سريعة وخفيفة
st.set_page_config(page_title="منصة نُقوش", layout="wide")

# رابط الجدول
url = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/gviz/tq?tqx=out:csv"

st.markdown("<h2 style='text-align: center; color: #d32f2f;'>📍 منصة نُقوش السريعة</h2>", unsafe_allow_html=True)

try:
    # جلب البيانات
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    
    # توحيد الإحداثيات وتنظيفها
    df.rename(columns={'lat': 'latitude', 'long': 'longitude', 'lon': 'longitude'}, inplace=True, errors='ignore')
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    
    # معالجة النقطة العشرية آلياً
    df['latitude'] = df['latitude'].apply(lambda x: x/10000 if x > 1000 else x)
    df['longitude'] = df['longitude'].apply(lambda x: x/10000 if x > 1000 else x)
    df = df.dropna(subset=['latitude', 'longitude'])

    if not df.empty:
        # --- الخريطة السريعة (Native Streamlit Map) ---
        # هذه الخريطة لا تظهر "ورقة مطوية" وتتحرك بسلاسة عالية
        st.map(df, color="#d32f2f", size=20)
        
        st.write("---")
        
        # --- نظام اختيار النداء السريع ---
        st.subheader("⚡ توجيه سريع للموقع")
        selected_person = st.selectbox("اختر اسم الشخص للذهاب لموقعه فوراً:", df['name'].unique())
        
        # جلب بيانات الشخص المختار
        person_data = df[df['name'] == selected_person].iloc[0]
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.info(f"📍 نداء من: **{person_data['name']}** | الحوجة: **{person_data.get('need', 'غير محددة')}**")
        with col2:
            # رابط جوجل ماب المباشر (Direct Deep Link)
            g_url = f"https://www.google.com/maps/search/?api=1&query={person_data['latitude']},{person_data['longitude']}"
            st.link_button("🚗 افتح في خرائط جوجل", g_url, use_container_width=True)

        st.write("---")
        st.subheader("📋 كشف النداءات الكامل")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("بانتظار بيانات صحيحة...")

except Exception as e:
    st.error(f"خطأ في التحميل: {e}")
