import streamlit as st
from streamlit_gsheets import GSheetsConnection

# إعداد الصفحة
st.set_page_config(page_title="منصة نُقوش", page_icon="🇸🇩", layout="wide")
st.title("🇸🇩 منصة نُقوش للنفير الرقمي")

# زر إضافة نداء جديد (يربط بالفورم البنفسجي)
form_url = "https://forms.gle/ECBm7eaeKMnErzpz8"
st.link_button("📢 أضف نداء استغاثة جديد", form_url)

# الاتصال وقراءة البيانات
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # قراءة الجدول Nugous h_DB
    df = conn.read()
    
    if not df.empty:
        st.subheader("📍 خريطة النداءات النشطة")
        # تنظيف البيانات وعرض الخريطة
        # تأكد أن أعمدة الجدول في ملفك هي 'lat' و 'lon'
        df_map = df.dropna(subset=['lat', 'lon'])
        st.map(df_map)
        
        st.subheader("📋 تفاصيل الاستغاثات")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("لا توجد نداءات مسجلة حالياً في الخريطة.")
except Exception as e:
    st.warning("يرجى التأكد من ربط قاعدة البيانات بشكل صحيح في الإعدادات.")
