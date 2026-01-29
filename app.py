import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. إعدادات الهوية البصرية (ألوان مستوحاة من علم السودان)
st.set_page_config(page_title="منصة نُقوش - النفير الرقمي", page_icon="🇸🇩", layout="wide")

# تخصيص المظهر عبر CSS بسيط
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    stButton>button { width: 100%; border-radius: 5px; background-color: #007229; color: white; }
    </style>
    """, unsafe_allow_status_code=True)

st.title("🇸🇩 منصة نُقوش: معاً لأجل السودان")
st.info("هذه المنصة تهدف لربط المتضررين بالمتطوعين بناءً على الموقع الجغرافي.")

# 2. الاتصال بقاعدة البيانات
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    return conn.read(ttl="0")

data = load_data()

# 3. محرك البحث والتصفية
st.subheader("🔍 البحث عن نداءات في منطقتك")
col1, col2 = st.columns(2)
with col1:
    search_city = st.text_input("اكتب اسم المدينة أو الحي (مثلاً: الدمازين)")
with col2:
    filter_need = st.multiselect("تصفية حسب نوع الحاجة", ["دواء", "غذاء", "إجلاء", "مياه"], default=["دواء", "غذاء", "إجلاء", "مياه"])

# تصفية البيانات بناءً على مدخلات المستخدم
filtered_data = data.copy()
if search_city:
    filtered_data = filtered_data[filtered_data['name'].str.contains(search_city, case=False, na=False)]
filtered_data = filtered_data[filtered_data['need'].isin(filter_need)]

# 4. عرض الخريطة والنداءات المصفاة
st.map(filtered_data)
st.dataframe(filtered_data, use_container_width=True)

# 5. إضافة نداء جديد (في الأسفل لسهولة الوصول)
st.divider()
st.subheader("📢 أضف نداء استغاثة جديد")
with st.expander("اضغط هنا لتعبئة بيانات النداء"):
    with st.form("new_request"):
        c1, c2 = st.columns(2)
        with c1:
            u_name = st.text_input("المنطقة / الحي (مثلاً: الدمازين - حي النهضة)")
            u_need = st.selectbox("ماذا تحتاج؟", ["دواء", "غذاء", "إجلاء", "مياه"])
        with c2:
            u_lat = st.number_input("إحداثيات العرض (يمكنك نسخها من خرائط جوجل)", value=15.0, format="%.4f")
            u_lon = st.number_input("إحداثيات الطول", value=32.0, format="%.4f")
        
        btn = st.form_submit_button("إرسال النداء الآن")
        if btn:
            new_row = pd.DataFrame([[u_name, u_need, u_lat, u_lon]], columns=['name', 'need', 'lat', 'lon'])
            updated_df = pd.concat([data, new_row], ignore_index=True)
            conn.update(data=updated_df)
            st.success("تم نشر نداءك بنجاح، نسأل الله السلامة للجميع.")
            st.rerun()
