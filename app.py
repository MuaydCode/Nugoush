import streamlit as st
import pandas as pd

# 1. إعدادات واجهة المستخدم
st.set_page_config(page_title="منصة نُقوش", page_icon="🇸🇩")
st.title("🇸🇩 منصة نُقوش للنفير الرقمي")

# 2. إنشاء مخزن بيانات مؤقت (Session State) بصورة صحيحة
if 'requests' not in st.session_state:
    st.session_state.requests = pd.DataFrame({
        'الاسم': ['تطوعي', 'مستشفى', 'مركز إيواء'],
        'الحاجة': ['توزيع مياه', 'نقص أكسجين', 'وجبات جاهزة'],
        'lat': [15.5007, 14.4012, 19.6158],
        'lon': [32.5599, 33.5199, 37.2164]
    })

# 3. القائمة الجانبية لإدخال البيانات
with st.sidebar:
    st.header("أضف نداء نفيـــر")
    with st.form("emergency_form"):
        u_name = st.text_input("الاسم أو الجهة")
        u_need = st.selectbox("نوع الحاجة", ["دواء", "غذاء", "إجلاء", "مياه"])
        u_lat = st.number_input("خط العرض (Latitude)", value=15.0, format="%.4f")
        u_lon = st.number_input("خط الطول (Longitude)", value=32.0, format="%.4f")
        
        submitted = st.form_submit_button("إرسال النداء")
        
        if submitted:
            new_row = pd.DataFrame({'الاسم': [u_name], 'الحاجة': [u_need], 'lat': [u_lat], 'lon': [u_lon]})
            st.session_state.requests = pd.concat([st.session_state.requests, new_row], ignore_index=True)
            st.success("تم إضافة نداءك للخريطة!")

# 4. عرض الخريطة
st.subheader("📍 خريطة الانتشار الحالية")
st.map(st.session_state.requests)

# 5. عرض الجدول
st.table(st.session_state.requests)
