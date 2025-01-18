import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import pandas as pd

# Define dataset paths
data_file = "data/SPI-J.geojson"  # Replace with the correct path to your GeoJSON file

# Load the dataset
gdf = gpd.read_file(data_file)

# Reproject to EPSG:4326 to handle geometry CRS warnings
gdf = gdf.to_crs("EPSG:4326")

# Display the full attribute table
st.subheader("Attribute Table")
st.write(gdf)  # Display the entire GeoDataFrame to inspect column names

# Sidebar
st.sidebar.title("SPI Drought Severity Map Viewer")
show_all_layers = st.sidebar.checkbox("Show All Layers")

# Sidebar filter for drought severity categories
drought_filter = st.sidebar.selectbox(
    "Filter by Drought Category", [
        "All",
        "Extreme drought",
        "Severe drought",
        "Moderate drought",
        "Mild drought",
        "Normal"
    ]
)

# Map numeric values to drought severity categories
drought_severity_mapping = {
    0: "Extreme drought",
    1: "Severe drought",
    2: "Moderate drought",
    3: "Mild drought",
    4: "Normal",
}

# Apply drought severity mapping
gdf["drought severity"] = gdf["drought severity"].map(drought_severity_mapping)

# Filter the dataset based on the drought category
if drought_filter != "All":
    filtered_gdf = gdf[gdf["drought severity"] == drought_filter]
else:
    filtered_gdf = gdf

# Sidebar warning message for no data
if filtered_gdf.empty:
    st.sidebar.warning(f"No data available for the selected drought category '{drought_filter}'. Please try a different selection.")
else:
    st.sidebar.success(f"Displaying data for the selected drought category '{drought_filter}'.")

# Create map centered on the centroid of the dataset
centroid = filtered_gdf.geometry.centroid
avg_lat = centroid.y.mean()
avg_lon = centroid.x.mean()
m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

# Function to generate popups with drought severity
def generate_popup(row):
    popup_content = f"<strong>Feature Information</strong><br>"
    severity_class = row["drought severity"]
    popup_content += f"<b>Drought Severity:</b> {severity_class}<br>"
    return popup_content

# Function to set color based on drought severity
drought_severity_colors = {
    "Extreme drought": "darkred",
    "Severe drought": "red",
    "Moderate drought": "orange",
    "Mild drought": "yellow",
    "Normal": "green",
}

def get_style_function(feature):
    severity = feature['properties']['drought severity']
    color = drought_severity_colors.get(severity, "gray")  # Default to gray if no matching class
    return {"color": color, "weight": 1, "fillOpacity": 0.6}

# Add GeoJSON layer with popups and colors
def add_geojson_layer(gdf, map_obj):
    geo_json = folium.GeoJson(
        gdf,
        style_function=get_style_function,
        name="SPI Drought Severity"  # Set the name for LayerControl
    )
    for _, row in gdf.iterrows():
        popup = folium.Popup(generate_popup(row), max_width=300)
        geo_json.add_child(popup)
    geo_json.add_to(map_obj)

# Add the filtered GeoJSON layer
add_geojson_layer(filtered_gdf, m)

# Adjust the map view to the bounding box of the selected class
if drought_filter != "All" and not filtered_gdf.empty:
    # Get the bounding box of the selected class
    bounds = filtered_gdf.geometry.total_bounds  # [minx, miny, maxx, maxy]
    # Zoom to the bounding box
    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

folium.LayerControl().add_to(m)

# Display the map
st_folium(m, width=700, height=500)

































