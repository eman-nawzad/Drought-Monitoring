import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import matplotlib.pyplot as plt

# Define dataset path
data_file = "data/SPIi (2).geojson"  # Replace with the correct path to your GeoJSON file

try:
    # Load the dataset
    gdf = gpd.read_file(data_file)

    # Reproject to EPSG:4326 to handle geometry CRS warnings
    gdf = gdf.to_crs("EPSG:4326")

    # Check for required column
    if "SPI" not in gdf.columns:
        st.error("The 'SPI' column is missing from the dataset. Please ensure the GeoJSON file contains an 'SPI' column.")
        st.stop()

    # Classify drought severity based on SPI
    spi_categories = {
        "Not a drought": {"min": 2.00, "max": float("inf")},
        "Very Wet": {"min": 1.50, "max": 1.99},
        "Moderately Wet": {"min": 1.00, "max": 1.49},
        "Near Normal": {"min": -0.99, "max": 0.99},
        "Moderately Dry": {"min": -1.00, "max": -1.49},
        "Severely Dry": {"min": -1.50, "max": -1.99},
        "Extremely Dry": {"min": float("-inf"), "max": -2.00},
    }

    def classify_drought_severity(spi_value):
        for category, range_ in spi_categories.items():
            if range_["min"] <= spi_value <= range_["max"]:
                return category
        return "Unknown"

    gdf["drought_severity"] = gdf["SPI"].apply(classify_drought_severity)

    # Sidebar
    st.sidebar.title("SPI Drought Severity Map Viewer")
    drought_filter = st.sidebar.selectbox(
        "Filter by Drought Category", ["All"] + list(spi_categories.keys())
    )

    # Filter data based on the selected drought category
    if drought_filter != "All":
        filtered_gdf = gdf[gdf["drought_severity"] == drought_filter]
    else:
        filtered_gdf = gdf

    if filtered_gdf.empty:
        st.sidebar.warning(f"No data available for the selected drought category '{drought_filter}'. Please try a different selection.")
        st.stop()

    # Display attribute table
    st.subheader("Filtered Attribute Table")
    st.write(filtered_gdf)

    # Map creation
    centroid = filtered_gdf.geometry.centroid
    avg_lat = centroid.y.mean()
    avg_lon = centroid.x.mean()
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

    # Define drought severity colors
    drought_severity_colors = {
        "Not a drought": "green",
        "Very Wet": "lightgreen",
        "Moderately Wet": "yellowgreen",
        "Near Normal": "yellow",
        "Moderately Dry": "orange",
        "Severely Dry": "red",
        "Extremely Dry": "darkred",
    }

    def get_style_function(feature):
        severity = feature['properties']['drought_severity']
        color = drought_severity_colors.get(severity, "gray")  # Default to gray if no matching class
        return {"color": color, "weight": 1, "fillOpacity": 0.6}

    def generate_popup(row):
        popup_content = f"<strong>Feature Information</strong><br>"
        popup_content += f"<b>Drought Severity:</b> {row['drought_severity']}<br>"
        popup_content += f"<b>SPI:</b> {row['SPI']:.2f}<br>"
        return popup_content

    # Add GeoJSON layer
    geo_json = folium.GeoJson(
        filtered_gdf,
        style_function=get_style_function,
        name="SPI Drought Severity"
    )
    for _, row in filtered_gdf.iterrows():
        popup = folium.Popup(generate_popup(row), max_width=300)
        geo_json.add_child(popup)
    geo_json.add_to(m)

    folium.LayerControl().add_to(m)

    # Display the map
    st_folium(m, width=700, height=500)

except FileNotFoundError:
    st.error("The specified GeoJSON file could not be found. Please check the file path.")
except Exception as e:
    st.error(f"An error occurred: {e}")































