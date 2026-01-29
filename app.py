import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. إعدادات الصفحة والهوية البصرية
st.set_page_config(page_title="منصة نُقوش - النفير الرقمي", page_icon="🇸🇩", layout="wide")

# تخصيص الألوان (تصحيح خطأ unsafe_allow_html)
st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    div.stButton > button:first-child {
        background-color: #007229;
        color: white;
        border-radius: 8px;
        border: none;
        height: 3em;
    }
    .stTextInput>div>div>input { border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🇸🇩 منصة نُقوش: النفير الرقمي السوداني")
st.write("منصة مجتمعية لربط نداءات الاستغاثة بالمتطوعين بناءً على الموقع الجغرافي.")

# 2. الاتصال بجدول بيانات جوجل (قاعدة البيانات)
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    data = conn.read(ttl="0")
except Exception as e:
    st.error("خطأ في الاتصال بقاعدة البيانات. تأكد من إعدادات Secrets.")
    data = pd.DataFrame(columns=['name', 'need', 'lat', 'lon'])

# 3. محرك البحث والتصفية
with st.expander("🔍 خيارات البحث والتصفية", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        search_query = st.text_input("ابحث عن مدينة أو حي (مثلاً: الدمازين، أمدرمان)")
    with col2:
        filter_type = st.multiselect("نوع الحاجة", ["دواء", "غذاء", "إجلاء", "مياه"], default=["دواء", "غذاء", "إجلاء", "مياه"])

# تصفية البيانات
filtered_df = data.copy()
if search_query:
    filtered_df = filtered_df[filtered_df['name'].str.contains(search_query, case=False, na=False)]
if filter_type:
    filtered_df = filtered_df[filtered_df['need'].isin(filter_type)]

# 4. عرض الخريطة والنتائج
st.subheader("📍 خريطة النداءات النشطة")
if not filtered_df.empty:
    st.map(filtered_df)
    st.dataframe(filtered_df, use_container_width=True)
else:
    st.warning("لا توجد بيانات تطابق بحثك حالياً.")

# 5. إضافة نداء استغاثة جديد
st.divider()
st.subheader("📢 أضف نداء جديد")
with st.form("add_new_request", clear_on_submit=True):
    c1, c2 = st.columns(2)
    with c1:
        new_name = st.text_input("المنطقة أو الحي")
        new_need = st.selectbox("نوع الحاجة", ["دواء", "غذاء", "إجلاء", "مياه"])
    with c2:
        new_lat = st.number_input("خط العرض (Latitude)", value=15.5000, format="%.4f")
        new_lon = st.number_input("خط الطول (Longitude)", value=32.5000, format="%.4f")
    
    submit_button = st.form_submit_button("إرسال النداء للمنصة")

    if submit_button:
        if new_name:
            new_data = pd.DataFrame([[new_name, new_need, new_lat, new_lon]], columns=['name', 'need', 'lat', 'lon'])
            updated_df = pd.concat([data, new_data], ignore_index=True)
            conn.update(data=updated_df)
            st.success("تم تسجيل النداء بنجاح! سيظهر الآن على الخريطة.")
            st.rerun()
        else:
            st.error("يرجى كتابة اسم المنطقة.")

# تذييل الصفحة
st.markdown("---")
st.caption("نُقوش: مشروع تطوعي مفتوح المصدر لخدمة إنسان السودان.")
