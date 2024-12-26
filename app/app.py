import streamlit as st
import folium
from streamlit_folium import st_folium

# App title
st.title("SPI 12-Month GeoJSON Visualization")

# Path to your GeoJSON file
geojson_path = "SPI_12_GeoJSON.geojson"

# Create a map
map_center = [34.5, 43.5]  # Replace with your region's approximate center (latitude, longitude)
m = folium.Map(location=map_center, zoom_start=6)

# Add the GeoJSON layer
folium.GeoJson(
    geojson_path,
    name="SPI",
    style_function=lambda feature: {
        "fillColor": "#0073e6" if feature["properties"]["value"] < 0 else "#ffcc00",
        "color": "black",
        "weight": 0.5,
        "fillOpacity": 0.7,
    },
).add_to(m)

# Add a legend
legend_html = """
<div style="
    position: fixed;
    bottom: 50px;
    left: 50px;
    width: 200px;
    height: 120px;
    background-color: white;
    z-index: 1000;
    border: 2px solid gray;
    padding: 10px;
    font-size: 14px;
">
<b>Legend</b><br>
<div style="display: flex; align-items: center;">
  <div style="background-color: #0073e6; width: 20px; height: 20px; margin-right: 10px;"></div>
  <span>SPI < 0 (Dry)</span>
</div>
<div style="display: flex; align-items: center;">
  <div style="background-color: #ffcc00; width: 20px; height: 20px; margin-right: 10px;"></div>
  <span>SPI ≥ 0 (Wet)</span>
</div>
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# Display the map in Streamlit
st_data = st_folium(m, width=700, height=500)

