import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import os

# Define the paths to the SPI and SVI/NDVI GeoJSON files
SPI_GEOJSON_PATH = os.path.join('data', 'SPI_12_GeoJSON.geojson')
SVI_NDVI_GEOJSON_PATH = os.path.join('data', 'SVI_NDVI_Export (1).geojson')

# Load the SPI GeoJSON data
def load_spi_data():
    try:
        # Load the SPI GeoJSON file using geopandas
        gdf = gpd.read_file(SPI_GEOJSON_PATH)
        
        # Ensure the GeoDataFrame has valid geometries
        gdf = gdf[gdf.geometry.notnull()]
        
        return gdf
    except Exception as e:
        st.error(f"Error loading SPI GeoJSON file: {e}")
        return None

# Load the SVI/NDVI GeoJSON data
def load_svi_ndvi_data():
    try:
        # Load the SVI/NDVI GeoJSON file using geopandas
        gdf = gpd.read_file(SVI_NDVI_GEOJSON_PATH)
        
        # Ensure the GeoDataFrame has valid geometries
        gdf = gdf[gdf.geometry.notnull()]
        
        return gdf
    except Exception as e:
        st.error(f"Error loading SVI/NDVI GeoJSON file: {e}")
        return None

# Function to create an interactive map with layers
def create_map():
    # Load both SPI and SVI datasets
    spi_data = load_spi_data()
    svi_data = load_svi_ndvi_data()
    
    if spi_data is None or spi_data.empty:
        st.warning("No valid SPI data available to display on the map.")
        return None
    if svi_data is None or svi_data.empty:
        st.warning("No valid SVI/NDVI data available to display on the map.")
        return None
    
    # Initialize the folium map at the center of the GeoDataFrames
    centroid = spi_data.geometry.unary_union.centroid
    m = folium.Map(location=[centroid.y, centroid.x], zoom_start=6, tiles='OpenStreetMap')

    # Add the SPI layer to the map
    folium.GeoJson(
        spi_data,
        name="SPI Data",
        style_function=lambda feature: {
            "fillColor": "blue" if feature["properties"].get("SPI_value", 0) > 0 else "red",
            "color": "black",
            "weight": 0.5,
            "fillOpacity": 0.6,
        },
    ).add_to(m)
    
    # Add the SVI/NDVI layer to the map
    folium.GeoJson(
        svi_data,
        name="SVI/NDVI Data",
        style_function=lambda feature: {
            "fillColor": "green" if feature["properties"].get("NDVI_value", 0) > 0 else "yellow",
            "color": "black",
            "weight": 0.5,
            "fillOpacity": 0.6,
        },
    ).add_to(m)

    # Add a LayerControl for layer selection inside the map
    folium.LayerControl(position='topleft').add_to(m)
    
    return m

# Function to display the home page
def display_home():
    st.title("Drought Monitoring Web Application")
    st.write(
        """
        This application displays both the SPI and SVI/NDVI data for monitoring drought conditions. 
        The SPI data is used to assess precipitation deficit and drought severity, while the SVI/NDVI data is used to assess vegetation health. 
        You can toggle between the layers using the map's layer selector.
        """
    )
    
    # Create and display the map
    m = create_map()
    if m:
        st_folium(m, width=800, height=600)  # Display the folium map in Streamlit

# Run the app
if __name__ == "__main__":
    display_home()
















