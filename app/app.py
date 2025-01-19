import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import pandas as pd
import requests
import json

# Define dataset paths for SPI and LST
spi_file = "data/SPI-J.geojson"  # SPI GeoJSON file path
lst_file = "data/LST-geojson.geojson"  # MODIS LST GeoJSON file path

# Load SPI dataset (already in GeoJSON format)
spi_gdf = gpd.read_file(spi_file)
spi_gdf = spi_gdf.to_crs("EPSG:4326")  # Ensure the CRS is in EPSG:4326 for mapping

# Load LST dataset (assuming it is in GeoJSON format as well)
lst_gdf = gpd.read_file(lst_file)
lst_gdf = lst_gdf.to_crs("EPSG:4326")  # Ensure the CRS is in EPSG:4326 for mapping

# Display the SPI and LST DataTables
st.subheader("SPI Data Attribute Table")
st.write(spi_gdf)  # Display the SPI GeoDataFrame

st.subheader("MODIS LST Data Attribute Table")
st.write(lst_gdf)  # Display the LST GeoDataFrame

# Map the numerical values or existing labels to the custom drought severity labels for SPI
drought_severity_map = {
    0: "Extreme drought",
    1: "Severe drought",
    2: "Moderate drought",
    3: "Mild drought",
    4: "Normal or above"
}

# Apply the mapping to the drought_severity column
spi_gdf["drought_severity"] = spi_gdf["drought_severity"].map(drought_severity_map)

# Sidebar for SPI and LST data visualization
st.sidebar.title("Drought and Temperature Viewer")

# Sidebar for SPI severity selection
drought_filter = st.sidebar.selectbox(
    "Filter by Drought Severity", ["All"] + list(drought_severity_map.values())
)

# Filter the SPI dataset based on the drought severity
if drought_filter != "All":
    filtered_spi_gdf = spi_gdf[spi_gdf["drought_severity"] == drought_filter]
else:
    filtered_spi_gdf = spi_gdf

# Sidebar warning message for no data
if filtered_spi_gdf.empty:
    st.sidebar.warning(f"No data available for the selected drought severity '{drought_filter}'. Please try a different selection.")
else:
    st.sidebar.success(f"Displaying data for the selected drought severity '{drought_filter}'.")

# Display filtered SPI attribute table
st.subheader(f"Filtered SPI Attribute Table - Drought Severity: {drought_filter}")
st.write(filtered_spi_gdf)

# Create map centered on the centroid of the SPI dataset
centroid_spi = filtered_spi_gdf.geometry.centroid
avg_lat_spi = centroid_spi.y.mean()
avg_lon_spi = centroid_spi.x.mean()

# Create the map
m = folium.Map(location=[avg_lat_spi, avg_lon_spi], zoom_start=8)

# Function to generate popups with SPI drought severity
def generate_spi_popup(row):
    popup_content = f"<strong>Feature Information</strong><br>"
    severity_class = row["drought_severity"]
    popup_content += f"<b>Drought Severity:</b> {severity_class}<br>"
    return popup_content

# Function to generate popups with LST temperature information
def generate_lst_popup(row):
    popup_content = f"<strong>Feature Information</strong><br>"
    lst_value = row["LST"]  # Assuming the LST data has a "LST" column
    popup_content += f"<b>Surface Temperature (°C):</b> {lst_value}<br>"
    return popup_content

# Add SPI GeoJSON layer with popups and colors
def add_spi_geojson_layer(spi_gdf, map_obj):
    geo_json = folium.GeoJson(
        spi_gdf,
        style_function=lambda feature: {
            "color": "#FF4500", "weight": 1, "fillOpacity": 0.6
        },
        name="SPI Drought Severity"
    )
    for _, row in spi_gdf.iterrows():
        popup = folium.Popup(generate_spi_popup(row), max_width=300)
        geo_json.add_child(popup)
    geo_json.add_to(map_obj)

# Add LST GeoJSON layer with popups and colors
def add_lst_geojson_layer(lst_gdf, map_obj):
    geo_json = folium.GeoJson(
        lst_gdf,
        style_function=lambda feature: {
            "color": "#FFD700", "weight": 1, "fillOpacity": 0.6
        },
        name="MODIS LST Temperature"
    )
    for _, row in lst_gdf.iterrows():
        popup = folium.Popup(generate_lst_popup(row), max_width=300)
        geo_json.add_child(popup)
    geo_json.add_to(map_obj)

# Add SPI and LST layers to the map
add_spi_geojson_layer(filtered_spi_gdf, m)
add_lst_geojson_layer(lst_gdf, m)

# Adjust the map view to fit the bounds of the datasets
if not filtered_spi_gdf.empty:
    bounds_spi = filtered_spi_gdf.geometry.total_bounds  # [minx, miny, maxx, maxy]
    m.fit_bounds([[bounds_spi[1], bounds_spi[0]], [bounds_spi[3], bounds_spi[2]]])

# Add Layer Control
folium.LayerControl().add_to(m)

# Display the map
st_folium(m, width=700, height=500)






































