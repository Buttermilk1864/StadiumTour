import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium
import googlemaps

st.set_page_config(page_title="Family Road Trip", layout="wide")
st.title("⚾ Road Trip Dashboard")

# Initialize Google Maps Client using the secret key
try:
    gmaps = googlemaps.Client(key=st.secrets["GOOGLE_MAPS_KEY"])
except:
    gmaps = None

# Load data
df = pd.read_csv("itinerary.csv", sep=",", encoding="utf-8-sig")

# Sidebar navigation
page = st.sidebar.selectbox("Choose a View", ["Itinerary", "Map", "Live ETA"])

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

elif page == "Live ETA":
    st.header("⏱️ Time to Next Stop")
    if gmaps is None:
        st.error("Google Maps API key not found in Streamlit Secrets!")
    else:
        current_loc = st.text_input("Where are you right now?", placeholder="e.g., Breezewood, PA or 123 Main St")
        next_stop = st.selectbox("Where are you heading?", df['Location'].tolist())
        
        if st.button("Calculate ETA") and current_loc:
            with st.spinner("Calculating route..."):
                try:
                    # Ask Google for the driving distance and time
                    result = gmaps.distance_matrix(origins=current_loc, 
                                                   destinations=next_stop, 
                                                   mode="driving", 
                                                   departure_time="now") # 'now' uses live traffic
                    
                    trip_data = result['rows'][0]['elements'][0]
                    
                    if trip_data['status'] == 'OK':
                        distance = trip_data['distance']['text']
                        duration = trip_data['duration_in_traffic']['text']
                        
                        st.success(f"**Distance:** {distance}")
                        st.info(f"**Estimated Drive Time (with live traffic):** {duration}")
                    else:
                        st.warning("Could not find a driving route between those locations.")
                except Exception as e:
                    st.error(f"Error calculating ETA: {e}")