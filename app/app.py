import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Load your SPI GeoJSON data
def load_spi_data():
    # Use geopandas to load the SPI GeoJSON (file is in the same directory as app.py)
    gdf = gpd.read_file('SPI_12_GeoJSON.geojson')
    return gdf

# Function to create an interactive map with OpenStreetMap
def create_spi_map():
    gdf = load_spi_data()
    
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
    st_folium(m, width=700, height=500)  # Display the folium map in Streamlit

# Function to display the about page
def display_about():
    st.title("About")
    st.write(
        """
        This web application is designed to help monitor drought conditions using the Standardized Precipitation Index (SPI).
        The data visualized in this app represents drought conditions for the year 2023. It helps identify regions with precipitation deficits or surpluses.
        """
    )

# Main application function
def main():
    # Add sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio( ["Go to ", "Home", "About"])
    
    # Render the selected page
    if page == "Home":
        display_home()
    elif page == "About":
        display_about()

if __name__ == "__main__":
    main()

