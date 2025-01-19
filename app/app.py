import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import pandas as pd

# Define dataset paths
spi_data_file = "data/SPI-J.geojson"  # Replace with the correct path to SPI GeoJSON
lst_data_file = "data/LST.geojson"  # Replace with the correct path to LST GeoJSON

# Load the datasets
spi_gdf = gpd.read_file(spi_data_file)
lst_gdf = gpd.read_file(lst_data_file)

# Reproject to a common CRS
spi_gdf = spi_gdf.to_crs("EPSG:4326")
lst_gdf = lst_gdf.to_crs("EPSG:4326")

# Perform spatial join to combine SPI and LST data
combined_gdf = gpd.sjoin(spi_gdf, lst_gdf, how="inner", predicate="intersects")

# Add a combined metric for analysis (e.g., SPI and LST interaction)
combined_gdf["combined_metric"] = combined_gdf["SPI_value"] * combined_gdf["LST_value"]

# Sidebar
st.sidebar.title("Drought and Surface Temperature Map Viewer")
metric = st.sidebar.selectbox("Select metric to display:", ["SPI", "LST", "Combined Metric"])

# Filter combined_gdf based on the metric
if metric == "SPI":
    combined_gdf["display_metric"] = combined_gdf["SPI_value"]
elif metric == "LST":
    combined_gdf["display_metric"] = combined_gdf["LST_value"]
else:
    combined_gdf["display_metric"] = combined_gdf["combined_metric"]

# Create map centered on the centroid of the dataset
centroid = combined_gdf.geometry.centroid
avg_lat = centroid.y.mean()
avg_lon = centroid.x.mean()
m = folium.Map(location=[avg_lat, avg_lon], zoom_start=8)

# Define color palette
color_palette = ["#d73027", "#fc8d59", "#fee08b", "#d9ef8b", "#91cf60", "#1a9850"]

# Normalize values for visualization
min_val = combined_gdf["display_metric"].min()
max_val = combined_gdf["display_metric"].max()
combined_gdf["norm_metric"] = (
    (combined_gdf["display_metric"] - min_val) / (max_val - min_val)
)

# Function to style GeoJSON layer
def style_function(feature):
    value = feature["properties"]["norm_metric"]
    color_idx = int(value * (len(color_palette) - 1))
    return {"fillColor": color_palette[color_idx], "color": "black", "weight": 1, "fillOpacity": 0.7}

# Add GeoJSON layer
folium.GeoJson(
    combined_gdf,
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(fields=["SPI_value", "LST_value", "combined_metric"]),
).add_to(m)

# Display map
st_folium(m, width=700, height=500)

# Display filtered attribute table
st.subheader("Filtered Attribute Table")
st.write(combined_gdf[["SPI_value", "LST_value", "combined_metric"]])







































