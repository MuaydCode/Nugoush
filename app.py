import streamlit as st
import pandas as pd
from datetime import datetime

# إعداد الصفحة بهوية بصرية
st.set_page_config(page_title="منصة نُقوش للنفير", page_icon="📍", layout="wide")

# رابط الجدول ورابط نموذج الإضافة
url = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/gviz/tq?tqx=out:csv"
form_url = "https://docs.google.com/forms/your-form-link-here" # ضع رابط فورم الإضافة هنا

# تنسيق العنوان والشعار
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { background-color: #d32f2f; color: white; border-radius: 8px; }
    .title-text { color: #1e3d59; font-family: 'Tahoma'; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.markdown("<h1 class='title-text'>📍 غرفة طوارئ نُقوش</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>تاريخ اليوم: {datetime.now().strftime('%Y-%m-%d')}</p>", unsafe_allow_html=True)

    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        df.rename(columns={'lat': 'latitude', 'long': 'longitude', 'lon': 'longitude'}, inplace=True, errors='ignore')
        
        # تحويل وتنظيف البيانات
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        df['latitude'] = df['latitude'].apply(lambda x: x/10000 if x > 1000 else x)
        df['longitude'] = df['longitude'].apply(lambda x: x/10000 if x > 1000 else x)
        df = df.dropna(subset=['latitude', 'longitude'])

        # القائمة الجانبية
        with st.sidebar:
            st.image("https://cdn-icons-png.flaticon.com/512/854/854878.png", width=100)
            st.title("لوحة التحكم")
            st.write("---")
            if st.button("➕ إضافة بلاغ استغاثة"):
                st.info("سيتم فتح نموذج إدخال البيانات..")
                # هنا يمكن وضع رابط الفورم
            
            st.write("---")
            search = st.text_input("🔍 بحث عن اسم أو حوجة")

        if search:
            df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]

        # الإحصائيات (Metrics)
        cols = st.columns(3)
        cols[0].metric("إجمالي النداءات", len(df))
        cols[1].metric("حالات عاجلة", "قيد المعالجة")
        cols[2].metric("تحديث تلقائي", "نشط")

        # الخريطة والجدول
        if not df.empty:
            st.map(df, color="#d32f2f")
            
            st.subheader("📋 قائمة الاستغاثات الحالية")
            # تلوين الجدول لسهولة القراءة
            st.dataframe(df.style.highlight_max(axis=0, subset=['name'] if 'name' in df.columns else None), use_container_width=True)
            
            # ميزة التوجيه السريع
            st.divider()
            person = st.selectbox("🎯 اختر شخصاً لتحديد موقعه بدقة:", df['name'].unique())
            p_data = df[df['name'] == person].iloc[0]
            g_url = f"https://www.google.com/maps?q={p_data['latitude']},{p_data['longitude']}"
            st.link_button(f"🚗 اذهب الآن لموقع: {person}", g_url)
        else:
            st.warning("لا توجد بيانات مطابقة للبحث.")

    except Exception as e:
        st.error(f"حدث خطأ أثناء تحديث البيانات: {e}")

if __name__ == "__main__":
    main()
