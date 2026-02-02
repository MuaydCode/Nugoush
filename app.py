import streamlit as st
import pandas as pd

# اختبار بسيط جداً لنعرف هل التطبيق يعمل أصلاً؟
st.write("التطبيق يعمل بنجاح! جاري محاولة جلب البيانات...")

# الرابط المباشر
URL = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/export?format=csv"

try:
    df = pd.read_csv(URL)
    st.success("تم الاتصال بجوجل شيت!")
    
    # عرض أول 5 صفوف للتأكد
    st.subheader("عينة من البيانات:")
    st.write(df.head())
    
    # محاولة رسم الخريطة إذا كانت الأعمدة موجودة
    # سنفترض أن الأعمدة هي الأول والثاني للحذر
    st.subheader("الخريطة:")
    st.map(df) 
    
except Exception as e:
    st.error(f"فشل جلب البيانات. الخطأ هو: {e}")
    st.info("تأكد أن ملف جوجل شيت مفتوح للجميع (Anyone with the link)")
