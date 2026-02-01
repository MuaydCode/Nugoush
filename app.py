import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="منصة نُقوش للنفير", layout="wide")

# رابط الجدول
url = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/gviz/tq?tqx=out:csv"

def main():
    st.markdown("<h2 style='text-align: center;'>📍 منصة نُقوش - إدارة الاستغاثات الحية</h2>", unsafe_allow_html=True)

    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        
        # توحيد الأسماء وتحويل الأرقام
        df.rename(columns={'lat': 'latitude', 'long': 'longitude', 'lon': 'longitude'}, inplace=True, errors='ignore')
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        df = df.dropna(subset=['latitude', 'longitude'])

        if not df.empty:
            # إنشاء خريطة تفاعلية متطورة
            m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=12)

            for i, row in df.iterrows():
                # تجهيز نص النافذة (Popup)
                # قمت بتصحيح رابط خرائط جوجل ليعمل مباشرة مع الاحداثيات
                google_maps_link = f"https://www.google.com/maps?q={row['latitude']},{row['longitude']}"
                popup_text = f"""
                <div style='font-family: Arial; direction: rtl; text-align: right;'>
                <b>الاسم:</b> {row.get('name', 'غير مسجل')}<br>
                <b>الحوجة:</b> {row.get('need', 'غير محددة')}<br><br>
                <a href="{google_maps_link}" target="_blank">
                <button style="background-color: #2e7d32; color: white; border: none; padding: 10px; border-radius: 5px; cursor: pointer; width: 100%;">
                🚗 الانتقال للموقع
                </button></a>
                </div>
                """
                
                folium.Marker(
                    [row['latitude'], row['longitude']],
                    popup=folium.Popup(popup_text, max_width=300),
                    tooltip=f"نداء من: {row.get('name', 'مواطن')}",
                    icon=folium.Icon(color='red', icon='info-sign')
                ).add_to(m)

            # عرض الخريطة التفاعلية
            st_folium(m, width="100%", height=500)
            
            st.write("---")
            st.subheader("📋 كشف النداءات بالتفصيل")
            st.dataframe(df, use_container_width=True)
            
        else:
            st.info("الخريطة جاهزة، بانتظار إدخال بيانات صحيحة في الجدول.")

    except Exception as e:
        st.error(f"حدث خطأ: {e}")

if __name__ == "__main__":
    main()
