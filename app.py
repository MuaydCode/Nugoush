import streamlit as st

# محاولة استيراد المكتبات بحذر
try:
    from streamlit_gsheets import GSheetConnection
    import pandas as pd
    IMPORT_SUCCESS = True
except ImportError:
    IMPORT_SUCCESS = False

st.set_page_config(page_title="منصة نُقوش", layout="wide")

if not IMPORT_SUCCESS:
    st.error("❌ السيرفر لم يقم بتثبيت المكتبات المطلوبة بعد.")
    st.info("تأكد من وجود ملف requirements.txt في GitHub وعمل Reboot للتطبيق.")
else:
    st.title("📍 خريطة نداءات الاستغاثة - نُقوش")
    
    try:
        # الربط المباشر
        conn = st.connection("gsheets", type=GSheetConnection)
        url = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/edit?usp=drivesdk"
        
        # جلب البيانات (بدون تخزين مؤقت)
        df = conn.read(spreadsheet=url, ttl=0)
        df = df.dropna(how="all")

        if not df.empty:
            st.map(df)
            st.subheader("📋 البيانات من الجدول:")
            st.dataframe(df)
        else:
            st.warning("الجدول فارغ، أضف بيانات ليظهر 'جدو موسى'.")
            
    except Exception as e:
        st.error(f"حدث خطأ أثناء جلب البيانات: {e}")

# زر لإجبار السيرفر على التحديث
if st.sidebar.button('🔄 تحديث إجباري'):
    st.rerun()
