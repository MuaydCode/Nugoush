import streamlit as st
import pandas as pd
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة نُقوش للطوارئ", page_icon="📍", layout="wide")

# الروابط الخاصة بك
CSV_URL = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/gviz/tq?tqx=out:csv"
FORM_URL = "https://forms.gle/abaLQPeGHi6LjKuu6"

# 2. دالة جلب البيانات (شاملة)
@st.cache_data(ttl=30)
def load_emergency_data():
    try:
        # إضافة v=time لضمان جلب بيانات جديدة دائماً
        df = pd.read_csv(f"{CSV_URL}&v={int(time.time())}")
        
        # تنظيف أسماء الأعمدة من المسافات
        df.columns = [str(c).strip() for c in df.columns]
        
        # خريطة تحويل الأسماء لتوحيدها برمجياً
        mapping = {
            'الاسم': 'name', 'اسم المتضرر': 'name', 'name': 'name',
            'الحوجة': 'need', 'نوع الحوجة': 'need', 'need': 'need',
            'رقم الهاتف': 'phone', 'phone': 'phone',
            'latitude': 'lat', 'lat': 'lat', 'خط العرض': 'lat',
            'longitude': 'lon', 'lon': 'lon', 'خط الطول': 'lon'
        }
        df.rename(columns=mapping, inplace=True, errors='ignore')
        
        # تحويل الإحداثيات إلى أرقام (وإلغاء أي نصوص)
        df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
        df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
        
        # حذف الصفوف التي لا تحتوي على إحداثيات نهائياً
        df = df.dropna(subset=['lat', 'lon'])
        
        # فلترة الإحداثيات المنطقية فقط (بين -90 و 90)
        df = df[(df['lat'] >= -90) & (df['lat'] <= 90)]
        df = df[(df['lon'] >= -180) & (df['lon'] <= 180)]
        
        return df
    except Exception as e:
        st.error(f"عذراً، حدث خطأ في الاتصال بالبيانات: {e}")
        return pd.DataFrame()

# 3. واجهة التطبيق الرئيسية
st.markdown("<h1 style='text-align: center; color: #d32f2f;'>📍 غرفة طوارئ نُقوش</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>نظام إدارة بلاغات الاستغاثة والنفير</p>", unsafe_allow_html=True)

# القائمة الجانبية
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1067/1067347.png", width=80)
    st.markdown("### 🛠 لوحة التحكم")
    st.link_button("➕ إضافة نداء استغاثة", FORM_URL, use_container_width=True)
    
    if st.button("🔄 تحديث الخريطة والبيانات", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.write("---")
    search_query = st.text_input("🔍 ابحث (بالاسم أو نوع الحوجة):", "")

# جلب البيانات
df_final = load_emergency_data()

# 4. منطق العرض
if not df_final.empty:
    # فلترة البحث
    if search_query:
        df_final = df_final[df_final.apply(lambda row: search_query.lower() in row.astype(str).str.lower().values, axis=1)]

    # عرض الخريطة
    st.subheader("🗺 موقع البلاغات على الخريطة")
    st.map(df_final[['lat', 'lon']])
    
    st.write("---")
    
    # عرض الجدول والبطاقات
    st.subheader(f"📋 قائمة البلاغات النشطة ({len(df_final)})")
    
    for index, row in df_final.iterrows():
        name = row.get('name', 'بلاغ غير معرف')
        need = row.get('need', 'طوارئ عامة')
        phone = str(row.get('phone', ''))
        
        with st.expander(f"🔴 {name} - {need}"):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**رقم الهاتف:** {phone}")
                st.write(f"**الإحداثيات:** {row['lat']}, {row['lon']}")
            with col2:
                # زر اتصال مباشر للموبايل
                st.markdown(f'<a href="tel:{phone}" style="display: block; text-align: center; background-color: #28a745; color: white; padding: 10px; text-decoration: none; border-radius: 8px;">📞 اتصل الآن</a>', unsafe_allow_html=True)
            with col3:
                # رابط جوجل ماب للتوجيه
                google_maps_url = f"https://www.google.com/maps?q={row['lat']},{row['lon']}"
                st.link_button("🚗 توجيه GPS", google_maps_url, use_container_width=True)

else:
    st.warning("⚠️ لا توجد بلاغات مسجلة حالياً أو الإحداثيات في الجدول غير صحيحة.")
    st.info("تأكد من إدخال الإحداثيات في النموذج كأرقام (مثال: 15.500)")

# تذييل الصفحة
st.markdown("---")
st.caption("منصة نُقوش 2026 - نُساند، نُغيث، ونُشيّد.")
