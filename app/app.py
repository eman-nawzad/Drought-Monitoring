import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Load your SPI GeoJSON data
def load_spi_data():
    # Use geopandas to load the SPI GeoJSON
    gdf = gpd.read_file('SPI_12_GeoJSON.geojson')  # File is in the same directory as app.py
    return gdf

# Function to create an interactive map with zoom functionality
def create_interactive_map():
    gdf = load_spi_data()

    # Get the bounds of the GeoDataFrame to center the map
    bounds = gdf.total_bounds  # [minx, miny, maxx, maxy]
    map_center = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]

    # Create a folium map
    m = folium.Map(location=map_center, zoom_start=6)

    # Add the GeoJSON data to the map
    folium.GeoJson(
        gdf,
        name="SPI Data",
        style_function=lambda feature: {
            "fillColor": "#0073e6" if feature["properties"]["SPI"] < 0 else "#ffcc00",
            "color": "black",
            "weight": 0.5,
            "fillOpacity": 0.7,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["SPI"],  # Replace with the correct key
            aliases=["SPI Value:"],
            localize=True,
        ),
    ).add_to(m)

    # Add layer control to enable toggling layers
    folium.LayerControl().add_to(m)

    return m

# Function to display information and instructions
def display_info():
    st.title("Drought Monitoring Web Application")
    st.write(
        """
        This application displays the SPI data for monitoring drought conditions. The SPI data is used to assess precipitation deficit and drought severity. 
        The interactive map below allows you to zoom in and out to explore the SPI data in greater detail.
        """
    )

# Main application function
def main():
    display_info()

    # Generate the interactive map
    m = create_interactive_map()

    # Display the map using Streamlit Folium
    st_folium(m, width=800, height=500)

if __name__ == "__main__":
    main()


