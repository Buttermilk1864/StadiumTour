import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="Family Road Trip", layout="wide")
st.title("⚾ Road Trip Dashboard")

# Load data
df = pd.read_csv("itinerary.csv", encoding="utf-8-sig")

# Sidebar navigation
page = st.sidebar.selectbox("Choose a View", ["Itinerary", "Map"])

if page == "Itinerary":
    st.header("Daily Schedule")
    for _, row in df.iterrows():
        with st.expander(f"Stop {row['Stop']}: {row['Location']}"):
            st.write(f"**Activity:** {row['Activity']}")
            st.link_button("View Food Menu", row['Menu_Link'])

elif page == "Map":
    st.header("Route Overview")
    m = folium.Map(location=[df.Lat.mean(), df.Lon.mean()], zoom_start=6)
    for _, row in df.iterrows():
        folium.Marker([row.Lat, row.Lon], popup=row.Location).add_to(m)
    st_folium(m, width=700)