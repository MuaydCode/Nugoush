import streamlit as st
import pandas as pd

st.set_page_config(page_title="غرفة طوارئ نُقوش", layout="wide", page_icon="🚨")

# الروابط
url = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/gviz/tq?tqx=out:csv"
form_url = "https://forms.gle/abaLQPeGHi6LjKuu6"

@st.cache_data(ttl=60)
def load_data(link):
    try:
        data = pd.read_csv(link)
        data.columns = data.columns.str.strip()
        # توحيد أسماء الأعمدة (عربي وإنجليزي)
        data.rename(columns={
            'الاسم': 'name', 'الحوجة': 'need', 'رقم الهاتف': 'phone',
            'latitude': 'lat', 'longitude': 'lon', 'خط العرض': 'lat', 'خط الطول': 'lon'
        }, inplace=True, errors='ignore')
        
        data['lat'] = pd.to_numeric(data['lat'], errors='coerce')
        data['lon'] = pd.to_numeric(data['lon'], errors='coerce')
        return data.dropna(subset=['lat', 'lon'])
    except:
        return pd.DataFrame()

# --- الواجهة ---
st.markdown("<h1 style='text-align: center; color: #d32f2f;'>📍 غرفة طوارئ نُقوش</h1>", unsafe_allow_html=True)

df = load_data(url)

# القائمة الجانبية (Sidebar)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1067/1067347.png", width=100)
    st.markdown("### إدارة البلاغات")
    st.link_button("➕ إضافة بلاغ استغاثة", form_url, use_container_width=True)
    
    st.write("---")
    search = st.text_input("🔍 بحث بالاسم أو نوع الحوجة:")
    if st.button("🔄 تحديث البيانات", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# معالجة البحث
if search:
    df = df[df.apply(lambda row: search.lower() in row.astype(str).str.lower().values, axis=1)]

# العرض الرئيسي
if not df.empty:
    # الخريطة المطورة
    st.map(df[['lat', 'lon']], color="#FF0000", size=40)
    
    st.write("---")
    st.subheader(f"📋 البلاغات النشطة ({len(df)})")
    
    # تحويل الجدول لشكل تفاعلي مع زر اتصال
    for i, row in df.iterrows():
        with st.expander(f"🔴 {row.get('name', 'بلاغ جديد')} - {row.get('need', 'حوجة غير محددة')}"):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.write(f"**الهاتف:** {row.get('phone', 'غير مسجل')}")
            with c2:
                # زر اتصال مباشر
                phone = str(row.get('phone', ''))
                st.markdown(f'<a href="tel:{phone}" style="background-color: #28a745; color: white; padding: 8px 20px; text-decoration: none; border-radius: 5px;">📞 اتصال الآن</a>', unsafe_allow_html=True)
            with c3:
                # زر جوجل ماب
                g_link = f"https://www.google.com/maps?q={row['lat']},{row['lon']}"
                st.link_button("🚗 توجيه (GPS)", g_link)
else:
    st.info("لا توجد بلاغات تطابق بحثك أو الجدول فارغ.")

st.markdown("---")
st.caption("نُقوش: نُساند، نُغيث، ونُشيّد.")
