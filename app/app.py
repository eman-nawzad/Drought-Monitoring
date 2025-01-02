import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import os

# Define the paths to the SPI GeoJSON files
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

# Function to create an interactive map
def create_map(data, layer_name):
    if data is None or data.empty:
        st.warning(f"No valid {layer_name} data available to display on the map.")
        return None
    
    # Initialize the folium map at the center of the GeoDataFrame
    centroid = data.geometry.unary_union.centroid
    m = folium.Map(location=[centroid.y, centroid.x], zoom_start=6, tiles='OpenStreetMap')

    # Add the selected dataset to the map
    folium.GeoJson(
        data,
        name=layer_name,
        style_function=lambda feature: {
            "fillColor": "blue" if feature["properties"].get("SPI_value", 0) > 0 else "red",
            "color": "black",
            "weight": 0.5,
            "fillOpacity": 0.6,
        },
    ).add_to(m)

    # Add a layer control to toggle between layers (if any)
    folium.LayerControl().add_to(m)
    
    return m

# Function to display the home page
def display_home():
    st.title("Drought Monitoring Web Application")
    st.write(
        """
        This application displays either the SPI or SVI/NDVI data for monitoring drought conditions. 
        The SPI data is used to assess precipitation deficit and drought severity, while the SVI/NDVI data is used to assess vegetation health. 
        Use the dropdown below to choose which dataset you want to visualize.
        """
    )
    
    # Allow user to choose between SPI and SVI datasets
    dataset_choice = st.selectbox(
        "Select the dataset to display:",
        ("SPI", "SVI/NDVI")
    )
    
    # Load the corresponding dataset based on user choice
    if dataset_choice == "SPI":
        data = load_spi_data()
        layer_name = "SPI Data"
    else:
        data = load_svi_ndvi_data()
        layer_name = "SVI/NDVI Data"
    
    # Create and display the selected map
    m = create_map(data, layer_name)
    if m:
        st_folium(m, width=800, height=600)  # Display the folium map in Streamlit

# Run the app
if __name__ == "__main__":
    display_home()







