import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="منصة نُقوش", layout="wide")

url = "https://docs.google.com/spreadsheets/d/1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0/gviz/tq?tqx=out:csv"

st.markdown("<h2 style='text-align: center; color: #2E7D32;'>📍 منصة نُقوش لنداءات الاستغاثة</h2>", unsafe_allow_html=True)

try:
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    
    # توحيد أسماء الإحداثيات
    df.rename(columns={'lat': 'latitude', 'long': 'longitude', 'lon': 'longitude'}, inplace=True, errors='ignore')
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    
    # معالجة الأرقام التي تفتقد للنقطة (كما فعلنا سابقاً)
    df['latitude'] = df['latitude'].apply(lambda x: x/10000 if x > 1000 else x)
    df['longitude'] = df['longitude'].apply(lambda x: x/10000 if x > 1000 else x)
    
    df = df.dropna(subset=['latitude', 'longitude'])

    if not df.empty:
        # إنشاء الخريطة
        center_lat = df['latitude'].mean()
        center_lon = df['longitude'].mean()
        m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

        for i, row in df.iterrows():
            # رابط جوجل ماب الصحيح
            g_link = f"https://www.google.com/maps?q={row['latitude']},{row['longitude']}"
            
            popup_html = f"""
            <div style="direction: rtl; text-align: right; font-family: Arial;">
                <b>الاسم:</b> {row.get('name', 'غير مسجل')}<br>
                <b>الحوجة:</b> {row.get('need', 'غير محددة')}<br><br>
                <a href="{g_link}" target="_blank">
                    <button style="background-color: #d32f2f; color: white; border: none; padding: 8px; border-radius: 5px; cursor: pointer; width: 100%;">
                        🚗 فتح الاتجاهات
                    </button>
                </a>
            </div>
            """
            folium.Marker(
                [row['latitude'], row['longitude']],
                popup=folium.Popup(popup_html, max_width=200),
                tooltip=row.get('name', 'نداء استغاثة'),
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)

        # عرض الخريطة
        st_folium(m, width=1200, height=500)
        
        st.write("---")
        st.subheader("📋 كشف النداءات بالتفصيل")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ لم يتم العثور على إحداثيات صحيحة في الجدول.")

except Exception as e:
    st.error(f"يوجد مشكلة في المكتبات: تأكد من إضافة streamlit-folium في requirements.txt")
