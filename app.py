import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والهوية
st.set_page_config(page_title="منصة نُقوش للنفير", page_icon="📍", layout="wide")

# 2. الروابط الخاصة بك (تم تجهيزها لتعمل مباشرة)
raw_url = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/gviz/tq?tqx=out:csv"
form_url = "https://forms.gle/abaLQPeGHi6LjKuu6"

# تنسيق العنوان
st.markdown("<h1 style='text-align: center; color: #d32f2f;'>📍 غرفة طوارئ نُقوش</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>نظام إدارة الاستغاثات والنداءات الميدانية الحية</p>", unsafe_allow_html=True)

# 3. القائمة الجانبية
with st.sidebar:
    st.header("⚙️ خيارات")
    st.link_button("➕ إضافة نداء جديد (للمتطوعين)", form_url, use_container_width=True)
    st.write("---")
    st.info("عند إضافة بلاغ عبر النموذج، سيظهر تلقائياً في الخريطة هنا بعد تحديث الصفحة.")

try:
    # 4. جلب ومعالجة البيانات
    df = pd.read_csv(raw_url)
    
    # تنظيف أسماء الأعمدة (لضمان مطابقتها للكود)
    df.columns = df.columns.str.strip()
    
    # تحويل أسماء الإحداثيات إذا كانت مختلفة
    df.rename(columns={
        'lat': 'latitude', 'long': 'longitude', 
        'lon': 'longitude', 'خط العرض': 'latitude', 
        'خط الطول': 'longitude'
    }, inplace=True, errors='ignore')

    # تحويل الإحداثيات لأرقام ومعالجة النقطة العشرية
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    
    # تصحيح مكان النقطة العشرية إذا تم إدخال الأرقام بدونها
    df['latitude'] = df['latitude'].apply(lambda x: x/10000 if x > 1000 else x)
    df['longitude'] = df['longitude'].apply(lambda x: x/10000 if x > 1000 else x)
    
    # حذف الصفوف التي لا تحتوي على إحداثيات
    df = df.dropna(subset=['latitude', 'longitude'])

    if not df.empty:
        # 5. عرض الخريطة السريعة
        st.map(df, color="#d32f2f", size=20)
        
        st.write("---")
        
        # 6. قسم التوجيه والجدول
        col_select, col_table = st.columns([1, 2])
        
        with col_select:
            st.subheader("🎯 توجيه سريع")
            # استخدام الاسم من الجدول، إذا لم يوجد نستخدم الفهرس
            name_col = 'name' if 'name' in df.columns else df.columns[1]
            person = st.selectbox("اختر صاحب النداء:", df[name_col].unique())
            
            p_data = df[df[name_col] == person].iloc[0]
            g_link = f"https://www.google.com/maps?q={p_data['latitude']},{p_data['longitude']}"
            st.link_button(f"🚗 فتح موقع {person} في خرائط جوجل", g_link, use_container_width=True)
        
        with col_table:
            st.subheader("📋 كشف البلاغات")
            st.dataframe(df, use_container_width=True, height=250)
            
    else:
        st.warning("🔄 لا توجد بيانات في الجدول حالياً. ابدأ بإضافة أول نداء عبر الزر الجانبي.")

except Exception as e:
    st.error(f"حدث خطأ في قراءة البيانات: {e}")
    st.info("تأكد من أن الجدول يحتوي على أعمدة بأسماء latitude و longitude.")

# تذييل الصفحة
st.markdown("---")
st.caption("منصة نُقوش للنفير - تم التصميم للمساعدة في جهود الإغاثة.")
