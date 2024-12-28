import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Load your SPI GeoJSON data
def load_spi_data():
    try:
        gdf = gpd.read_file('SPI_12_GeoJSON.geojson')
        return gdf
    except Exception as e:
        st.error(f"Error loading SPI GeoJSON file: {e}")
        return None

# Function to create an interactive map with OpenStreetMap
def create_spi_map():
    gdf = load_spi_data()
    if gdf is None or gdf.empty:
        st.warning("No valid SPI data available to display on the map.")
        return None
    
    # Ensure the GeoDataFrame has valid geometries
    gdf = gdf[gdf.geometry.notnull()]
    
    # Initialize the folium map at the center of the GeoDataFrame
    centroid = gdf.geometry.unary_union.centroid
    m = folium.Map(location=[centroid.y, centroid.x], zoom_start=6, tiles='OpenStreetMap')

    # Add SPI GeoJSON data to the map
    folium.GeoJson(
        gdf,
        name="SPI Data",
        style_function=lambda feature: {
            "fillColor": "blue" if feature["properties"]["value"] > 0 else "red",
            "color": "black",
            "weight": 0.5,
            "fillOpacity": 0.6,
        },
        tooltip=folium.GeoJsonTooltip(fields=["value"], aliases=["SPI Value:"]),
    ).add_to(m)

    folium.LayerControl().add_to(m)
    return m

# Function to display the home page
def display_home():
    st.title("Drought Monitoring Web Application")
    st.write(
        """
        This application displays the SPI data for monitoring drought conditions. The SPI data is used to assess precipitation deficit and drought severity. 
        The map below shows the SPI data for the year 2023. Higher values indicate wetter conditions, and lower values indicate drier conditions.
        """
    )
    m = create_spi_map()
    if m:
        st_folium(m, width=800, height=600)  # Display the folium map in Streamlit

# Run the app
if __name__ == "__main__":
    display_home()

