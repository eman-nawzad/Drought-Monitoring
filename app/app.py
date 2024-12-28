import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium


# Load the SPI GeoJSON data
def load_spi_data():
    try:
        # Use geopandas to load the SPI GeoJSON file
        gdf = gpd.read_file('SPI_12_GeoJSON.geojson')
        
        # Debug: Display the column names and first few rows
        st.write("GeoJSON Columns:", gdf.columns.tolist())
        st.write("Sample Data:", gdf.head())
        
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
    
    # Ensure the GeoDataFrame has valid geometries
    gdf = gdf[gdf.geometry.notnull()]
    
    # Initialize the folium map at the center of the GeoDataFrame
    centroid = gdf.geometry.unary_union.centroid
    m = folium.Map(location=[centroid.y, centroid.x], zoom_start=6, tiles='OpenStreetMap')

    # Get a list of all available fields in the GeoJSON data
    fields = gdf.columns.tolist()
    
    # Update these field names based on your GeoJSON file structure
    style_field = "SPI_value"  # Replace with the actual field for SPI values
    tooltip_fields = fields[:3]  # Display the first 3 fields as tooltips (customize as needed)

    # Validate the field used for styling
    if style_field not in gdf.columns:
        st.error(f"The field '{style_field}' is not available in the data. Choose from: {fields}")
        return None

    # Add SPI GeoJSON data to the map
    folium.GeoJson(
        gdf,
        name="SPI Data",
        style_function=lambda feature: {
            "fillColor": "blue" if feature["properties"][style_field] > 0 else "red",
            "color": "black",
            "weight": 0.5,
            "fillOpacity": 0.6,
        },
        tooltip=folium.GeoJsonTooltip(fields=tooltip_fields, aliases=[f"{field}:" for field in tooltip_fields]),
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



