import streamlit as st
import pandas as pd

st.set_page_config(page_title="منصة نُقوش", layout="wide")
st.title("📍 خريطة نداءات الاستغاثة - نُقوش")

# رابط الجدول بصيغة CSV
url = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/gviz/tq?tqx=out:csv"

try:
    # قراءة البيانات
    df = pd.read_csv(url)
    
    # تنظيف الأعمدة من أي فراغات مخفية (مثل اللي ظهرت في الإيرور \u200b)
    df.columns = df.columns.str.strip()

    # محاولة ذكية لإيجاد أعمدة الإحداثيات حتى لو بأي اسم
    # سنقوم بتغيير اسم الأعمدة برمجياً لتوافق الخريطة
    rename_dict = {}
    for col in df.columns:
        if 'lat' in col.lower(): rename_dict[col] = 'latitude'
        if 'long' in col.lower() or 'lon' in col.lower(): rename_dict[col] = 'longitude'
    
    df.rename(columns=rename_dict, inplace=True)

    # حذف الصفوف الفارغة
    df = df.dropna(subset=['latitude', 'longitude'], thresh=1) if 'latitude' in df.columns else df.dropna(how="all")

    if 'latitude' in df.columns and 'longitude' in df.columns:
        # عرض الخريطة
        st.map(df)
        
        st.write("---")
        st.subheader("📋 النداءات المسجلة:")
        # تنسيق الجدول ليظهر بشكل جميل
        st.dataframe(df, use_container_width=True)
        
        if "جدو موسى" in df.values:
            st.success("✅ تم العثور على بيانات 'جدو موسى' بنجاح!")
    else:
        st.error("⚠️ لم أجد أعمدة الإحداثيات. من فضلك تأكد أن اسم العمود في الجدول هو latitude و longitude")
        st.write("الأعمدة الحالية في جدولك هي:", list(df.columns))

except Exception as e:
    st.error(f"حدث خطأ: {e}")

if st.sidebar.button('🔄 تحديث فوري'):
    st.rerun()
