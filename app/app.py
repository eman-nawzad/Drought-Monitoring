import streamlit as st
import folium
import geopandas as gpd
from streamlit_folium import st_folium

# File paths
spi_geojson = "data/SPI-J.geojson"  # Path to SPI GeoJSON file
lst_geojson = "data/LST.geojson"  # Path to LST GeoJSON file

# Load GeoJSON files
spi_gdf = gpd.read_file(spi_geojson).to_crs("EPSG:4326")
lst_gdf = gpd.read_file(lst_geojson).to_crs("EPSG:4326")

# Merge SPI and LST data by spatial join
combined_gdf = gpd.sjoin(spi_gdf, lst_gdf, how="inner", op="intersects")

# Create a combined column for display
combined_gdf["popup_info"] = combined_gdf.apply(
    lambda row: f"<b>SPI:</b> {row['SPI']}<br><b>LST:</b> {row['LST']}", axis=1
)

# Sidebar: Filters
st.sidebar.title("SPI & LST Interactive Map")
st.sidebar.info("Explore the relationship between SPI and surface temperature.")
spi_range = st.sidebar.slider("SPI Range", float(combined_gdf["SPI"].min()), float(combined_gdf["SPI"].max()), (float(combined_gdf["SPI"].min()), float(combined_gdf["SPI"].max())))
lst_range = st.sidebar.slider("LST Range", float(combined_gdf["LST"].min()), float(combined_gdf["LST"].max()), (float(combined_gdf["LST"].min()), float(combined_gdf["LST"].max())))

# Filter the GeoDataFrame based on selected ranges
filtered_gdf = combined_gdf[
    (combined_gdf["SPI"] >= spi_range[0]) & (combined_gdf["SPI"] <= spi_range[1]) &
    (combined_gdf["LST"] >= lst_range[0]) & (combined_gdf["LST"] <= lst_range[1])
]

# Display filtered data
st.subheader("Filtered Data Table")
st.write(filtered_gdf)

# Map Center
if not filtered_gdf.empty:
    map_center = [filtered_gdf.geometry.centroid.y.mean(), filtered_gdf.geometry.centroid.x.mean()]
else:
    map_center = [0, 0]

# Create the interactive map
m = folium.Map(location=map_center, zoom_start=6)

# Add SPI and LST GeoJSON layers with popups
for _, row in filtered_gdf.iterrows():
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=6,
        color="blue" if row["SPI"] < 0 else "red",  # Blue for negative SPI, Red for positive
        fill=True,
        fill_color="blue" if row["SPI"] < 0 else "red",
        fill_opacity=0.7,
        popup=folium.Popup(row["popup_info"], max_width=300),
    ).add_to(m)

# Add map to Streamlit
st_folium(m, width=700, height=500)







































