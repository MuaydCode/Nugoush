import streamlit as st
import pandas as pd
import time

# 1. إعدادات الهوية والاحترافية
st.set_page_config(page_title="غرفة طوارئ نُقوش", page_icon="📍", layout="wide")

# الروابط الخاصة بك
CSV_URL = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/gviz/tq?tqx=out:csv"
FORM_URL = "https://forms.gle/abaLQPeGHi6LjKuu6"

# 2. وظيفة جلب البيانات (مُحصنة ضد الأخطاء)
@st.cache_data(show_spinner=False) # تم إزالة الـ ttl لجعل التحديث يدوياً ومضموناً
def get_clean_data():
    try:
        # إضافة بارامتر عشوائي للرابط لضمان عدم جلب نسخة قديمة من المتصفح
        query_url = f"{CSV_URL}&cache_buster={time.time()}"
        df = pd.read_csv(query_url).dropna(how='all')
        df.columns = df.columns.str.strip()
        
        rename_dict = {
            'الاسم': 'name', 'الحوجة': 'need', 'رقم الهاتف': 'phone',
            'latitude': 'lat', 'longitude': 'lon', 'خط العرض': 'lat', 'خط الطول': 'lon'
        }
        df.rename(columns=rename_dict, inplace=True, errors='ignore')

        df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
        df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
        
        # تصحيح الإحداثيات وإزالة التالف
        df = df.dropna(subset=['lat', 'lon'])
        df = df[(df['lat'].between(-90, 90)) & (df['lon'].between(-180, 180))]
        return df
    except Exception:
        return pd.DataFrame()

# 3. واجهة المستخدم
st.markdown("<h1 style='text-align: center; color: #d32f2f;'>📍 منصة نُقوش للطوارئ</h1>", unsafe_allow_html=True)

# القائمة الجانبية
with st.sidebar:
    st.markdown("### 🛠 التحكم")
    st.link_button("➕ إضافة بلاغ جديد", FORM_URL, use_container_width=True)
    
    # تعديل زر التحديث ليكون قاطعاً
    if st.button("🔄 تحديث البيانات الآن", use_container_width=True):
        st.cache_data.clear() # مسح الكاش برمجياً
        st.rerun() # إعادة تشغيل التطبيق بالبيانات الجديدة
        
    st.write("---")
    search = st.text_input("🔍 ابحث (بالاسم أو الحوجة):")

# جلب البيانات
with st.spinner('جاري جلب أحدث البلاغات...'):
    df = get_clean_data()

# تصفية البحث
if search and not df.empty:
    df = df[df.apply(lambda row: search.lower() in row.astype(str).str.lower().values, axis=1)]

# 4. العرض
if not df.empty:
    st.map(df[['lat', 'lon']], color="#FF0000", size=45)
    st.write("---")
    st.subheader(f"📋 البلاغات النشطة ({len(df)})")

    for _, row in df.iterrows():
        name = row.get('name', 'بلاغ مجهول')
        need = row.get('need', 'غير محدد')
        phone = str(row.get('phone', ''))
        
        with st.expander(f"🔴 {name} | {need}"):
            c1, c2, c3 = st.columns(3)
            with c1: st.write(f"**الهاتف:**\n{phone}")
            with c2:
                st.markdown(f'<a href="tel:{phone}" style="display: block; text-align: center; background-color: #28a745; color: white; padding: 10px; text-decoration: none; border-radius: 8px;">📞 اتصل الآن</a>', unsafe_allow_html=True)
            with c3:
                g_link = f"https://www.google.com/maps?q={row['lat']},{row['lon']}"
                st.link_button("🚗 توجيه (GPS)", g_link, use_container_width=True)
else:
    st.warning("⚠️ لا توجد بلاغات حالياً أو البيانات قيد التحديث.")

st.caption("غرفة عمليات نُقوش - التحديث الاحترافي")
