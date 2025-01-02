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
def create_map(zoom_level, tile_type, show_spi, show_svi):
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
    m = folium.Map(location=[centroid.y, centroid.x], zoom_start=zoom_level, tiles=tile_type)

    # Add the SPI layer if selected
    if show_spi:
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

    # Add the SVI/NDVI layer if selected
    if show_svi:
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
    folium.LayerControl(position='topright').add_to(m)
    
    return m

# Function to display the home page
def display_home():
    st.title("Drought Monitoring Web Application")
    st.write(
        """
        This application displays both the SPI and SVI/NDVI data for monitoring drought conditions. 
        The SPI data is used to assess precipitation deficit and drought severity, while the SVI/NDVI data is used to assess vegetation health. 
        Use the sidebar to control the map's settings.
        """
    )

    # Sidebar controls for the user to interact with
    st.sidebar.title("Map Controls")
    
    # Control for zoom level
    zoom_level = st.sidebar.slider("Zoom Level", min_value=1, max_value=18, value=6, step=1)
    
    # Control for map tile layer
    tile_type = st.sidebar.selectbox("Select Map Tile", ["OpenStreetMap", "Stamen Terrain", "Stamen Toner", "Stamen Watercolor"])

    # Control for which layers to display
    show_spi = st.sidebar.checkbox("Show SPI Data", value=True)
    show_svi = st.sidebar.checkbox("Show SVI/NDVI Data", value=True)

    # Create and display the map with the selected settings
    m = create_map(zoom_level, tile_type, show_spi, show_svi)
    if m:
        st_folium(m, width=800, height=600)  # Display the folium map in Streamlit

# Run the app
if __name__ == "__main__":
    display_home()














