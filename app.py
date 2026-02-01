import streamlit as st
import pandas as pd
import plotly.express as px # لإضافة رسوم بيانية احترافية
import time

st.set_page_config(page_title="منصة نُقوش الاحترافية", page_icon="🛡️", layout="wide")

# الرابط المنشور (CSV)
CSV_URL = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/pub?output=csv"
FORM_URL = "https://forms.gle/abaLQPeGHi6LjKuu6"

@st.cache_data(ttl=15)
def load_and_analyze():
    try:
        df = pd.read_csv(f"{CSV_URL}&v={int(time.time())}")
        df.columns = [str(c).strip() for c in df.columns]
        
        # البحث الذكي عن الأعمدة
        mappings = {
            'عرض': 'lat', 'lat': 'lat', 'طول': 'lon', 'lon': 'lon',
            'اسم': 'name', 'حوجة': 'need', 'هاتف': 'phone', 'موبايل': 'phone'
        }
        for k, v in mappings.items():
            for col in df.columns:
                if k in col.lower(): df.rename(columns={col: v}, inplace=True)
        
        df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
        df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
        return df.dropna(subset=['lat', 'lon'])
    except:
        return pd.DataFrame()

# --- واجهة المستخدم ---
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🛡️ غرفة عمليات نُقوش الرقمية</h1>", unsafe_allow_html=True)

df = load_and_analyze()

if not df.empty:
    # 1. قسم المؤشرات (KPIs) - هنا تظهر الاحترافية
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("إجمالي البلاغات", len(df))
    with col2:
        top_need = df['need'].value_counts().idxmax() if 'need' in df.columns else "غير محدد"
        st.metric("الحوجة الأكثر طلباً", top_need)
    with col3:
        st.metric("تغطية جغرافية", f"{df['lat'].nunique()} منطقة")
    with col4:
        st.metric("حالة النظام", "متصل مباشر")

    # 2. الخريطة والرسوم البيانية
    tab1, tab2 = st.tabs(["🗺️ الخريطة التفاعلية", "📊 تحليل البيانات"])
    
    with tab1:
        st.map(df[['lat', 'lon']], color='#D32F2F', size=50)
    
    with tab2:
        c_left, c_right = st.columns(2)
        with c_left:
            # رسم بياني لأنواع الحوجة
            if 'need' in df.columns:
                fig = px.pie(df, names='need', title='توزيع البلاغات حسب نوع الحوجة', hole=0.4)
                st.plotly_chart(fig, use_container_width=True)
        with c_right:
            # رسم بياني للنمو (إذا وجد عمود التاريخ)
            st.info("💡 سيتم إضافة تحليل زمني تلقائياً عند زيادة عدد البلاغات.")

    # 3. قسم إدارة البلاغات (البطاقات)
    st.markdown("### 📋 تفاصيل البلاغات الميدانية")
    search = st.text_input("🔍 ابحث عن اسم، منطقة، أو نوع حوجة محددة:")
    
    filtered_df = df
    if search:
        filtered_df = df[df.apply(lambda r: search.lower() in str(r).lower(), axis=1)]

    for _, row in filtered_df.iterrows():
        with st.expander(f"🚩 {row.get('need', 'بلاغ')} - {row.get('name', 'مجهول')}"):
            c1, c2, c3 = st.columns([2, 1, 1])
            with c1:
                st.write(f"**رقم الهاتف:** {row.get('phone', 'غير متوفر')}")
            with c2:
                st.markdown(f'<a href="tel:{row.get("phone", "")}" style="display:block; text-align:center; background:#059669; color:white; padding:8px; border-radius:8px; text-decoration:none;">📞 اتصال مباشر</a>', unsafe_allow_html=True)
            with c3:
                st.link_button("🚗 توجيه GPS", f"https://www.google.com/maps?q={row['lat']},{row['lon']}", use_container_width=True)

else:
    st.error("⚠️ لم يتم استلام بيانات صالحة بعد. تأكد من إعدادات 'النشر على الويب' في قوقل شيت.")

# القائمة الجانبية
with st.sidebar:
    st.markdown("### ⚙️ الإدارة")
    st.link_button("➕ إضافة بلاغ جديد", FORM_URL, use_container_width=True)
    if st.button("🔄 تحديث شامل للبيانات", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
