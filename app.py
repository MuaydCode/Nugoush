import streamlit as st
from streamlit_gsheets import GSheetConnection
import pandas as pd

# 1. إعداد الصفحة
st.set_page_config(page_title="منصة نُقوش", layout="wide")

st.title("📍 خريطة نداءات الاستغاثة")

# 2. الربط مع جوجل شيت (مع الغاء التخزين المؤقت تماماً)
try:
    conn = st.connection("gsheets", type=GSheetConnection)
    
    # رابط الجدول الخاص بك
    url = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/edit?usp=drivesdk"
    
    # جلب البيانات مع تحديث لحظي ttl=0
    df = conn.read(spreadsheet=url, ttl=0)

    # حذف الصفوف الفارغة
    df = df.dropna(how="all")

    if not df.empty:
        # عرض الخريطة
        st.map(df)
        
        # عرض الجدول للتأكد من اسم "جدو موسى"
        st.write("### البيانات المسجلة حالياً:")
        st.dataframe(df)
    else:
        st.info("الجدول فارغ حالياً، أضف بيانات في جوجل شيت لتظهر هنا.")

except Exception as e:
    st.error("خطأ في الاتصال: تأكد من إضافة st-gsheets-connection في ملف requirements.txt")
    st.exception(e)

# 3. زر جانبي للتحديث الإجباري
if st.sidebar.button('🔄 تحديث الخريطة الآن'):
    st.cache_data.clear()
    st.rerun()
