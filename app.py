import streamlit as st
from streamlit_gsheets import GSheetConnection
import pandas as pd

# إعدادات واجهة التطبيق
st.set_page_config(page_title="منصة نُقوش للنفير", page_icon="📍", layout="wide")

st.markdown("<h1 style='text-align: center; color: #2E7D32;'>📍 منصة نُقوش لنداءات الاستغاثة</h1>", unsafe_allow_label=True)
st.write("---")

# إنشاء الاتصال بجوجل شيت
# ttl=0 تعني عدم تخزين البيانات القديمة وجلب الجديد فوراً عند كل تحديث
conn = st.connection("gsheets", type=GSheetConnection)

try:
    # قراءة البيانات - استبدل الرابط برابط جدولك إذا تغير
    url = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/edit?usp=drivesdk"
    df = conn.read(spreadsheet=url, ttl=0)

    # تنظيف البيانات من أي صفوف فارغة تماماً
    df = df.dropna(how="all")

    if not df.empty:
        # عرض الخريطة 
        # ملاحظة: تأكد أن الأعمدة في الجدول اسمها بالظبط (latitude) و (longitude)
        st.subheader("🌐 خريطة الاستغاثة الحية")
        st.map(df)

        # عرض البيانات في جدول أنيق أسفل الخريطة
        st.write("---")
        st.subheader("📋 تفاصيل النداءات")
        st.dataframe(df, use_container_width=True)
        
    else:
        st.info("نظام نُقوش جاهز: لا توجد نداءات نشطة حالياً في الجدول.")

except Exception as e:
    st.error("⚠️ عذراً، هناك مشكلة في الاتصال بالبيانات.")
    st.info("تأكد من إعدادات الـ Secrets في Streamlit Cloud وصلاحية الرابط.")

# زر التحديث في القائمة الجانبية
if st.sidebar.button('🔄 تحديث البيانات الآن'):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.write("👨‍💻 مطور بواسطة: فريق نُقوش المتطوع")
