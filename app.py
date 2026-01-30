import streamlit as st
from streamlit_gsheets import GSheetConnection
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="منصة نُقوش للنفير", layout="wide")

st.title("📍 خريطة نداءات الاستغاثة - نُقوش")

# الربط مع جوجل شيت وتحديد زمن التحديث بـ 0 ثانية لضمان جلب البيانات فوراً
conn = st.connection("gsheets", type=GSheetConnection)

# جلب البيانات بدون تخزين مؤقت (ttl=0) لضمان التحديث اللحظي
try:
    df = conn.read(
        spreadsheet="https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/edit?usp=drivesdk",
        ttl=0  # السر هنا: 0 يعني لا تخزن البيانات، اقرأها الآن من الجدول
    )
    
    # تنظيف البيانات من الصفوف الفارغة
    df = df.dropna(how="all")

    if not df.empty:
        # عرض الخريطة
        # ملاحظة: تأكد أن أعمدة الإحداثيات في الجدول اسمها (latitude و longitude)
        st.map(df)
        
        # عرض جدول البيانات للتأكد
        st.subheader("قائمة النداءات الحالية:")
        st.dataframe(df)
    else:
        st.warning("لا توجد نداءات استغاثة حالياً في الجدول.")

except Exception as e:
    st.error(f"حدث خطأ في جلب البيانات: {e}")

# زر لتحديث البيانات يدوياً
if st.button('تحديث الخريطة الآن'):
    st.rerun()
