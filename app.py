import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. إعدادات الصفحة والستايل
st.set_page_config(page_title="منصة نُقوش للنفير", layout="wide", initial_sidebar_state="expanded")

# رابط الجدول
url = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/gviz/tq?tqx=out:csv"

def main():
    st.markdown("<h1 style='text-align: center; color: #d32f2f;'>📍 منصة نُقوش لنداءات الاستغاثة</h1>", unsafe_allow_html=True)

    try:
        # 2. جلب وتجهيز البيانات
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        df.rename(columns={'lat': 'latitude', 'long': 'longitude', 'lon': 'longitude'}, inplace=True, errors='ignore')
        
        # تحويل الإحداثيات ومعالجة الأخطاء
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        df['latitude'] = df['latitude'].apply(lambda x: x/10000 if x > 1000 else x)
        df['longitude'] = df['longitude'].apply(lambda x: x/10000 if x > 1000 else x)
        df = df.dropna(subset=['latitude', 'longitude'])

        # 3. القائمة الجانبية (الفلترة)
        st.sidebar.header("🔍 خيارات التصفية")
        all_needs = ["الكل"] + sorted(df['need'].unique().tolist()) if 'need' in df.columns else ["الكل"]
        selected_need = st.sidebar.selectbox("اختر نوع الحوجة:", all_needs)

        if selected_need != "الكل":
            df = df[df['need'] == selected_need]

        # 4. إحصائيات سريعة (Metrics)
        col1, col2, col3 = st.columns(3)
        col1.metric("إجمالي النداءات", len(df))
        col2.metric("أنواع الحوجة", len(df['need'].unique()) if 'need' in df.columns else 0)
        col3.metric("المنطقة", "الخرطوم")

        # 5. بناء الخريطة المتطورة
        if not df.empty:
            m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=12, control_scale=True)

            for i, row in df.iterrows():
                # تحديد لون النقطة بناءً على الحوجة
                icon_color = 'red'
                need_type = str(row.get('need', '')).lower()
                if 'ماء' in need_type or 'مياه' in need_type: icon_color = 'blue'
                elif 'دواء' in need_type or 'علاج' in need_type: icon_color = 'green'
                elif 'غذاء' in need_type or 'اكل' in need_type: icon_color = 'orange'

                g_link = f"https://www.google.com/maps?q={row['latitude']},{row['longitude']}"
                
                popup_html = f"""
                <div style="direction: rtl; text-align: right; font-family: 'Tahoma'; border-radius: 10px;">
                    <h4 style="margin:0; color:#d32f2f;">👤 {row.get('name', 'غير مسجل')}</h4>
                    <hr style="margin:5px 0;">
                    <b>📦 الحوجة:</b> {row.get('need', 'غير محددة')}<br>
                    <b>📞 تواصل:</b> {row.get('phone', 'غير متوفر')}<br><br>
                    <a href="{g_link}" target="_blank" style="text-decoration:none;">
                        <button style="background-color: #2e7d32; color: white; border: none; padding: 10px; border-radius: 5px; cursor: pointer; width: 100%; font-weight: bold;">
                             فتح في الخريطة 🚗
                        </button>
                    </a>
                </div>
                """
                folium.Marker(
                    [row['latitude'], row['longitude']],
                    popup=folium.Popup(popup_html, max_width=250),
                    tooltip=f"{row.get('name', 'نداء')} - {row.get('need', '')}",
                    icon=folium.Icon(color=icon_color, icon='info-sign')
                ).add_to(m)

            # عرض الخريطة
            st_folium(m, width="100%", height=550)
            
            st.write("---")
            st.subheader("📋 جدول البيانات التفصيلي")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("⚠️ لا توجد بيانات مطابقة لهذا الفلتر.")

    except Exception as e:
        st.error(f"حدث خطأ في عرض المنصة: {e}")

if __name__ == "__main__":
    main()
