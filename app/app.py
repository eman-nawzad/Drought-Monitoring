import streamlit as st
import folium
from streamlit_folium import st_folium

# Define SPI categories and their colors
spi_categories = [
    {"name": "Very Wet", "range": "> 2", "color": "#1f78b4"},
    {"name": "Moderately Wet", "range": "1.5 - 2", "color": "#33a02c"},
    {"name": "Neutral", "range": "-1.5 - 1.5", "color": "#ffff99"},
    {"name": "Moderately Dry", "range": "-2 - -1.5", "color": "#ff7f00"},
    {"name": "Very Dry", "range": "< -2", "color": "#e31a1c"},
]

# Generate legend dynamically
legend_html = "<div style='position: fixed; bottom: 10px; left: 10px; border:2px solid grey; z-index:9999; background-color:white; padding:10px; font-size:14px;'><b>Legend:</b><ul style='list-style-type:none; padding-left: 0;'>"
for category in spi_categories:
    legend_html += f"<li><span style='background-color:{category['color']}; color:white; padding:2px 5px;'>&nbsp;&nbsp;</span> {category['range']} ({category['name']})</li>"
legend_html += "</ul></div>"

# Add the legend to the Streamlit app
st.components.v1.html(legend_html, height=200)

# Map styling function
def style_function(feature):
    spi = feature['properties']['SPI']
    if spi > 2:
        return {'fillColor': '#1f78b4', 'color': '#1f78b4'}
    elif 1.5 < spi <= 2:
        return {'fillColor': '#33a02c', 'color': '#33a02c'}
    elif -1.5 < spi <= 1.5:
        return {'fillColor': '#ffff99', 'color': '#ffff99'}
    elif -2 < spi <= -1.5:
        return {'fillColor': '#ff7f00', 'color': '#ff7f00'}
    else:
        return {'fillColor': '#e31a1c', 'color': '#e31a1c'}

# Load the SPI GeoJSON file
geojson_file = "SPI_12_GeoJSON.geojson"

# Create a Folium map
m = folium.Map(location=[35.5, 44.0], zoom_start=6)
folium.GeoJson(
    geojson_file,
    style_function=style_function
).add_to(m)

# Display the map in the Streamlit app
st_folium(m, width=700, height=500)
