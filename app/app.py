import geopandas as gpd
import folium
import streamlit as st

# Load your GeoJSON files (LST and SPI)
lst_gdf = gpd.read_file('data/LST.geojson')  # Update path to LST GeoJSON
spi_gdf = gpd.read_file('data/SPI-J.geojson')  # Update path to SPI GeoJSON

# Get the centroid of the LST GeoDataFrame to center the map
latitude = lst_gdf.geometry.centroid.y.mean()
longitude = lst_gdf.geometry.centroid.x.mean()

# Create a map centered around the centroid of the LST data
m = folium.Map(location=[latitude, longitude], zoom_start=10)

# Add LST data to the map
for _, row in lst_gdf.iterrows():
    folium.GeoJson(row['geometry']).add_to(m)

# Add SPI data to the map
for _, row in spi_gdf.iterrows():
    folium.GeoJson(row['geometry']).add_to(m)

# Save the map to an HTML file
map_path = 'data/interactive_map.html'  # Path where you want to save the map
m.save(map_path)

# Display the map in Streamlit
st.title("Drought Monitoring Map")
st.write("This map shows the LST and SPI data for drought monitoring.")
st.markdown(f'<iframe src="{map_path}" width="100%" height="600"></iframe>', unsafe_allow_html=True)










































