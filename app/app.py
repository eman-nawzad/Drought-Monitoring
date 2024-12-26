import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt

# Load your SPI GeoJSON data
def load_spi_data():
    # Use geopandas to load the SPI GeoJSON (file is in the same directory as app.py)
    gdf = gpd.read_file('SPI_12_GeoJSON.geojson')  # File is in the same directory as app.py
    return gdf

# Function to display SPI data on a map
def plot_spi_map():
    gdf = load_spi_data()
    
    # Create a simple map of SPI data
    fig, ax = plt.subplots(figsize=(10, 6))
    gdf.plot(ax=ax, cmap='viridis', legend=True)
    ax.set_title("SPI 12 Month (2023) - Drought Index")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    st.pyplot(fig)

# Function to display information and instructions
def display_info():
    st.title("Drought Monitoring Web Application")
    st.write(
        """
        This application displays the SPI data for monitoring drought conditions. The SPI data is used to assess precipitation deficit and drought severity. 
        The map above shows the SPI data for the year 2023. Higher values indicate wetter conditions, and lower values indicate drier conditions.
        """
    )

# Main application function
def main():
    display_info()
    plot_spi_map()

if __name__ == "__main__":
    main()



elif page == "SPI Map":
    st.markdown("<h2 class='header-font'>SPI Map</h2>", unsafe_allow_html=True)
    st.markdown("<p class='text-font'>This page displays the Standardized Precipitation Index (SPI) data as an interactive map.</p>", unsafe_allow_html=True)

    # Load SPI GeoJSON file
    spi_geojson_path = "SPI_12_GeoJSON.geojson"

    # Check if file exists
    if not os.path.exists(spi_geojson_path):
        st.error(f"The file {spi_geojson_path} does not exist. Please check the file path.")
    else:
        # Load the GeoJSON data
        spi_gdf = gpd.read_file(spi_geojson_path)

        # Display GeoJSON map
        st.header("Interactive SPI Map")
        spi_map_center = [spi_gdf.geometry.centroid.y.mean(), spi_gdf.geometry.centroid.x.mean()]
        spi_map = folium.Map(location=spi_map_center, zoom_start=10)

        # Add SPI GeoJSON layer to the map
        folium.GeoJson(spi_geojson_path, name="SPI").add_to(spi_map)
        st_folium(spi_map, width=700, height=500)



