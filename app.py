import streamlit as st
import pandas as pd

st.set_page_config(page_title="منصة نُقوش للنفير", layout="wide")
st.title("📍 خريطة نداءات الاستغاثة - نُقوش")

# رابط الجدول
url = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/gviz/tq?tqx=out:csv"

try:
    # 1. جلب البيانات
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()

    # 2. توحيد أسماء الأعمدة لتفادي أخطاء التسمية
    rename_dict = {}
    for col in df.columns:
        if 'lat' in col.lower(): rename_dict[col] = 'latitude'
        if 'long' in col.lower() or 'lon' in col.lower(): rename_dict[col] = 'longitude'
        if 'اسم' in col.lower() or 'name' in col.lower(): rename_dict[col] = 'الاسم'
    df.rename(columns=rename_dict, inplace=True)

    # 3. تحويل النصوص إلى أرقام (فلوت) غصباً عن تنسيق الجدول
    if 'latitude' in df.columns and 'longitude' in df.columns:
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        
        # حذف أي سطر فيه أخطاء في الإحداثيات
        df = df.dropna(subset=['latitude', 'longitude'])

        # 4. ميزة البحث (Search Bar)
        search_query = st.text_input("🔍 ابحث عن اسم، حوجة، أو موقع:", "")
        if search_query:
            # البحث في كل الأعمدة
            df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]

        if not df.empty:
            # 5. عرض الخريطة
            st.subheader(f"🌐 تم العثور على ({len(df)}) نداءات")
            st.map(df)
            
            st.write("---")
            st.subheader("📋 قائمة البيانات:")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("⚠️ لا توجد بيانات مطابقة للبحث أو أن الإحداثيات بالجدول غير صحيحة.")
    else:
        st.error("❌ لم يتم العثور على أعمدة الإحداثيات (latitude و longitude) في الجدول.")

except Exception as e:
    st.error(f"حدث خطأ تقني: {e}")

# زر التحديث
if st.sidebar.button('🔄 تحديث فوري للبيانات'):
    st.rerun()
