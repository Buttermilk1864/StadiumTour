import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium
import googlemaps

# 1. Page Config & Custom CSS for the "Scouting Report" look
st.set_page_config(page_title="Stadium Tour Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e1e1e; padding: 15px; border-radius: 10px; border: 1px solid #2d5a27; }
    h1, h2, h3 { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True) # <-- This was the fixed line

st.title("⚾ Stadium Tour Scouting Report")

# Initialize Google Maps
try:
    gmaps = googlemaps.Client(key=st.secrets["GOOGLE_MAPS_KEY"])
except:
    gmaps = None

# Load data with the new header structure
df = pd.read_csv("itinerary.csv", sep=",", encoding="utf-8-sig")
df.columns = df.columns.str.strip()

# Sidebar
page = st.sidebar.selectbox("Scout Menu", ["Itinerary", "Interactive Map", "Live Radar (ETA)"])

if page == "Itinerary":
    st.header("📅 The Master Schedule")
    if not df.empty and 'Date' in df.columns:
        for d in df['Date'].unique():
            st.subheader(f"🗓️ {d}")
            day_df = df[df['Date'] == d]
            for _, row in day_df.iterrows():
                icon = "🚗" if row['Action'] == "Travel" else "⚾" if row['Action'] == "Activity" else "🍔"
                with st.expander(f"{icon} {row['Start_Time']} - {row['Destination']}"):
                    st.write(f"**From:** {row['Start_Loc']} ➡️ **To:** {row['End_Loc']}")
                    if str(row['Distance']) != "nan" and row['Distance'] != "N/A":
                        st.success(f"📏 Distance: {row['Distance']} | ⏳ Duration: {row['Duration']}")
    else:
        st.info("No scouting data found. Use the Admin GUI to add stops!")

elif page == "Interactive Map":
    st.header("📍 Route Mapping")
    
    # Check if we actually have data and the address column exists
    if not df.empty and 'End_Addr' in df.columns:
        # Filter out any rows that have empty addresses
        map_df = df.dropna(subset=['End_Addr'])
        map_df = map_df[map_df['End_Addr'] != ""]
        
        if not map_df.empty:
            m = folium.Map(location=[39.8283, -98.5795], zoom_start=4, tiles="CartoDB dark_matter")
            
            for _, row in map_df.iterrows():
                if gmaps:
                    try:
                        geocode_result = gmaps.geocode(row['End_Addr'])
                        if geocode_result:
                            loc = geocode_result[0]['geometry']['location']
                            folium.Marker(
                                [loc['lat'], loc['lng']], 
                                popup=f"{row['Destination']}",
                                icon=folium.Icon(color='green', icon='star')
                            ).add_to(m)
                    except:
                        continue
            st_folium(m, width=900, height=500)
        else:
            st.info("No addresses found to map yet. Use the Admin GUI to add a stop with a full address!")
    else:
        st.info("Start scouting by adding your first stop in the Admin GUI!")

elif page == "Live Radar (ETA)":
    st.header("⏱️ Real-Time Scouting")
    if gmaps:
        curr = st.text_input("Current Scout Position", placeholder="e.g. Nashville, TN")
        # Use 'Destination' column for the dropdown
        dest_list = df['Destination'].unique().tolist() if not df.empty else []
        dest = st.selectbox("Target Destination", dest_list)
        
        if st.button("Calculate Arrival") and curr:
            # Force Imperial (Miles) here
            res = gmaps.distance_matrix(curr, dest, mode="driving", units="imperial", departure_time="now")
            if res['rows'][0]['elements'][0]['status'] == 'OK':
                data = res['rows'][0]['elements'][0]
                st.metric("Miles to Go", data['distance']['text'])
                st.metric("Time in Traffic", data['duration_in_traffic']['text'])
            else:
                st.error("Route not found.")