import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة نُقوش", page_icon="🇸🇩")
st.title("🇸🇩 منصة نُقوش للنفير الرقمي")

# 2. إنشاء الاتصال بجدول بيانات جوجل (بناءً على الـ Secrets التي وضعتها)
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. وظيفة لجلب البيانات من الجدول
def load_data():
    return conn.read(ttl="0") # ttl="0" لضمان جلب البيانات الجديدة دائماً

data = load_data()

# 4. القائمة الجانبية لإدخال البيانات وحفظها في الجدول
with st.sidebar:
    st.header("أضف نداء نفيـــر")
    with st.form("emergency_form"):
        u_name = st.text_input("الاسم أو الجهة")
        u_need = st.selectbox("نوع الحاجة", ["دواء", "غذاء", "إجلاء", "مياه"])
        u_lat = st.number_input("خط العرض (Latitude)", value=15.5, format="%.4f")
        u_lon = st.number_input("خط الطول (Longitude)", value=32.5, format="%.4f")
        
        submitted = st.form_submit_button("إرسال النداء")
        
        if submitted:
            # إضافة السطر الجديد للجدول
            new_row = pd.DataFrame([[u_name, u_need, u_lat, u_lon]], columns=['name', 'need', 'lat', 'lon'])
            updated_df = pd.concat([data, new_row], ignore_index=True)
            conn.update(data=updated_df)
            st.success("تم حفظ النداء في قاعدة البيانات بنجاح!")
            st.rerun() # إعادة تشغيل التطبيق لتحديث الخريطة

# 5. عرض الخريطة والجدول من البيانات الحقيقية
st.subheader("📍 خريطة الانتشار الحالية (بيانات حقيقية)")
if not data.empty:
    st.map(data)
    st.table(data)
else:
    st.info("لا توجد نداءات مسجلة حالياً.")
