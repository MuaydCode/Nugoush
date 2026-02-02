import streamlit as st
import pandas as pd

st.title("Nugoush Platform - Emergency Test")

# The most direct way to get Google Sheets data
sheet_id = "1JaWlB_7mOYl2ZO1A1meINlcNFE75G3XM2tptfdkDJM0"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    df = pd.read_csv(url)
    st.success("Connection Successful!")
    
    # Simple Map
    st.subheader("Live Map")
    # Streamlit looks for 'lat'/'lon' or 'latitude'/'longitude'
    # Let's force rename for the test
    df.columns = [c.strip().lower() for c in df.columns]
    
    # Basic data display
    st.write("Data Preview:", df.head())
    
    if 'lat' in df.columns and 'lon' in df.columns:
        st.map(df)
    else:
        st.warning("Data loaded, but 'lat' and 'lon' columns not found.")

except Exception as e:
    st.error(f"Error: {e}")
