import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import os

# Set page configuration
st.set_page_config(
    page_title="SPI Web App",
    layout="wide"
)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "SPI Map", "About", "Help", "Feedback"])

# Function to load GeoJSON data
def load_spi_data(file_path):
    if not os.path.exists(file_path):
        st.error(f"The file {file_path} does not exist. Please check the file path.")
        return None
    return gpd.read_file(file_path)

# Function to display SPI data on a map
def display_spi_map(file_path):
    gdf = load_spi_data(file_path)
    if gdf is None:
        return

    # Calculate map center
    map_center = [gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()]
    m = folium.Map(location=map_center, zoom_start=10)

    # Add GeoJSON layer
    folium.GeoJson(file_path, name="SPI").add_to(m)

    # Add layer control
    folium.LayerControl().add_to(m)

    # Display the map
    st.header("Interactive SPI Map")
    st_folium(m, width=900, height=500)

# Navigation logic
if page == "Home":
    st.title("Drought Monitoring Web Application")
    st.write(
        """
        Welcome to the SPI Web App! This platform provides an interactive map for exploring the Standardized 
        Precipitation Index (SPI) data. Use the navigation menu on the left to switch between the map 
        and other sections.
        """
    )

elif page == "SPI Map":
    st.title("Standardized Precipitation Index (SPI) Map")
    st.write(
        """
        The SPI map provides insights into drought severity by analyzing precipitation deficits. 
        Higher SPI values indicate wetter conditions, while lower values indicate drier conditions.
        """
    )
    spi_geojson_path = "SPI_12_GeoJSON.geojson"  # Update this path if needed
    display_spi_map(spi_geojson_path)

elif page == "About":
    st.title("About This Application")
    st.write(
        """
        This web application was designed to provide an interactive platform for visualizing 
        Standardized Precipitation Index (SPI) data. The SPI is a key metric for monitoring drought 
        severity and precipitation deficits.
        """
    )

elif page == "Help":
    st.title("Help Section")
    st.write(
        """
        Need assistance? Use the navigation menu to access the SPI map or contact support. 
        For documentation, visit:
        - [Streamlit Documentation](https://docs.streamlit.io/)
        - [Folium Documentation](https://python-visualization.github.io/folium/)
        """
    )

elif page == "Feedback":
    st.title("Feedback")
    st.write("We value your feedback! Please fill out the form below:")
    with st.form("feedback_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        feedback = st.text_area("Your Feedback")
        submit_button = st.form_submit_button("Submit")
        if submit_button:
            if name and email and feedback:
                st.success("Thank you for your feedback!")
            else:
                st.error("Please fill out all fields.")

