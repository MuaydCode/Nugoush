import streamlit as st
import pandas as pd

# 1. إعدادات الهوية والاحترافية
st.set_page_config(page_title="غرفة طوارئ نُقوش", page_icon="📍", layout="wide")

# الروابط الخاصة بك
CSV_URL = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/gviz/tq?tqx=out:csv"
FORM_URL = "https://forms.gle/abaLQPeGHi6LjKuu6"

# 2. وظيفة جلب البيانات (مُحصنة ضد الأخطاء)
@st.cache_data(ttl=30)
def get_clean_data():
    try:
        # قراءة البيانات مع تجاهل الصفوف الفارغة
        df = pd.read_csv(CSV_URL).dropna(how='all')
        df.columns = df.columns.str.strip()
        
        # توحيد أسماء الأعمدة (عربي وإنجليزي) مهما كانت في الجدول
        rename_dict = {
            'الاسم': 'name', 'الحوجة': 'need', 'رقم الهاتف': 'phone', 'phone': 'phone',
            'latitude': 'lat', 'longitude': 'lon', 'خط العرض': 'lat', 'خط الطول': 'lon',
            'lat': 'lat', 'long': 'lon'
        }
        df.rename(columns=rename_dict, inplace=True, errors='ignore')

        # تحويل الإحداثيات لأرقام وحذف التالف منها (بين -90 و 90)
        df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
        df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
        
        # تصحيح الإحداثيات التي أُدخلت بدون نقطة (مثل 155006)
        df['lat'] = df['lat'].apply(lambda x: x/10000 if abs(x) > 90 else x)
        df['lon'] = df['lon'].apply(lambda x: x/10000 if abs(x) > 180 else x)
        
        # حذف أي سطر ليس فيه إحداثيات صحيحة
        df = df.dropna(subset=['lat', 'lon'])
        df = df[(df['lat'].between(-90, 90)) & (df['lon'].between(-180, 180))]
        return df
    except Exception:
        return pd.DataFrame()

# 3. واجهة المستخدم (التصميم)
st.markdown("<h1 style='text-align: center; color: #d32f2f;'>📍 منصة نُقوش للطوارئ</h1>", unsafe_allow_html=True)

# القائمة الجانبية
with st.sidebar:
    st.markdown("### 🛠 التحكم")
    st.link_button("➕ إضافة بلاغ جديد", FORM_URL, use_container_width=True)
    if st.button("🔄 تحديث الخريطة", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.write("---")
    search = st.text_input("🔍 ابحث (بالاسم أو الحوجة):")

# جلب البيانات
df = get_clean_data()

# تصفية البحث إذا وُجد
if search and not df.empty:
    df = df[df.apply(lambda row: search.lower() in row.astype(str).str.lower().values, axis=1)]

# 4. العرض الرئيسي (الخريطة + القوائم)
if not df.empty:
    # عرض الخريطة الاحترافية
    st.map(df[['lat', 'lon']], color="#FF0000", size=45)
    
    st.write("---")
    st.subheader(f"📋 البلاغات النشطة ({len(df)})")

    # عرض البلاغات بشكل بطاقات احترافية
    for _, row in df.iterrows():
        name = row.get('name', 'بلاغ مجهول')
        need = row.get('need', 'غير محدد')
        phone = str(row.get('phone', ''))
        
        with st.expander(f"🔴 {name} | {need}"):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.write(f"**رقم التواصل:**\n{phone}")
            with c2:
                # زر اتصال مباشر (HTML للعمل على الموبايل)
                st.markdown(f'<a href="tel:{phone}" style="display: block; text-align: center; background-color: #28a745; color: white; padding: 10px; text-decoration: none; border-radius: 8px;">📞 اتصل الآن</a>', unsafe_allow_html=True)
            with c3:
                # رابط خرائط جوجل
                g_link = f"https://www.google.com/maps?q={row['lat']},{row['lon']}"
                st.link_button("🚗 توجيه (GPS)", g_link, use_container_width=True)
else:
    st.warning("⚠️ لا توجد بلاغات صحيحة حالياً. تأكد من إدخال الإحداثيات في النموذج بشكل سليم (مثال: 15.589).")

st.markdown("---")
st.caption("غرفة عمليات نُقوش - الإصدار الاحترافي 2026")
