import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium


# Load the SPI GeoJSON data
def load_spi_data():
    try:
        # Load the SPI GeoJSON file using geopandas
        gdf = gpd.read_file('SPI_12_GeoJSON.geojson')
        
        # Ensure the GeoDataFrame has valid geometries
        gdf = gdf[gdf.geometry.notnull()]
        
        return gdf
    except Exception as e:
        st.error(f"Error loading SPI GeoJSON file: {e}")
        return None


# Function to create an interactive map
def create_spi_map():
    gdf = load_spi_data()
    
    if gdf is None or gdf.empty:
        st.warning("No valid SPI data available to display on the map.")
        return None
    
    # Initialize the folium map at the center of the GeoDataFrame
    centroid = gdf.geometry.unary_union.centroid
    m = folium.Map(location=[centroid.y, centroid.x], zoom_start=6, tiles='OpenStreetMap')

    # Check for multiple layers and add them to the map
    # GeoDataFrame may contain multiple layers, handle that
    layers = gdf['geometry'].apply(lambda x: x.__class__.__name__).unique()

    # Add each layer to the map
    for layer in layers:
        # Filter the data by geometry type and add it to the map
        layer_data = gdf[gdf['geometry'].apply(lambda x: x.__class__.__name__) == layer]
        
        if layer_data.empty:
            continue
        
        folium.GeoJson(
            layer_data,
            name=f"{layer} Data",
            style_function=lambda feature: {
                "fillColor": "blue" if feature["properties"].get("SPI_value", 0) > 0 else "red",
                "color": "black",
                "weight": 0.5,
                "fillOpacity": 0.6,
            },
            tooltip=folium.GeoJsonTooltip(fields=["id", "first", "label"], aliases=["ID:", "First:", "Label:"]),
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
    
    # Create and display the map
    m = create_spi_map()
    if m:
        st_folium(m, width=800, height=600)  # Display the folium map in Streamlit


# Run the app
if __name__ == "__main__":
    display_home()





