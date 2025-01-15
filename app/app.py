import streamlit as st
import geopandas as gpd
import folium
from folium import Choropleth
from branca.colormap import linear
import pandas as pd

# Set up the Streamlit app layout
st.title("SPI Drought Severity Map")

# Upload SPI GeoJSON file (vectorized)
uploaded_file = st.file_uploader("Upload your vectorized SPI GeoJSON file", type=["geojson"])

if uploaded_file is not None:
    # Read the GeoJSON file into a GeoDataFrame
    gdf = gpd.read_file(uploaded_file)

    # Display the attribute table
    st.subheader("Attribute Table")
    st.write(gdf)

    # Create a Folium map centered around the region of interest
    m = folium.Map(location=[36.325735, 43.993215], zoom_start=8)  # Example coordinates for Arbil

    # Define the color scale for drought severity (from extreme to normal)
    color_scale = linear.YlOrRd_09.scale(0, 4)  # Color scale for severity

    # Add the vectorized SPI data to the map as a Choropleth layer
    Choropleth(
        geo_data=gdf,
        data=gdf,
        columns=["drought_severity", "drought_severity"],  # Mapping severity to the color scale
        key_on="feature.properties.drought_severity",
        fill_color=color_scale,
        fill_opacity=0.6,
        line_opacity=0.2,
        legend_name="Drought Severity",
    ).add_to(m)

    # Add a color legend
    color_scale.caption = "Drought Severity"
    color_scale.add_to(m)

    # Display the map
    st.subheader("Drought Severity Map")
    st.markdown("**Legend:**")
    st.markdown("""
        - 0: Extreme Drought (Red)
        - 1: Severe Drought (Orange)
        - 2: Moderate Drought (Yellow)
        - 3: Mild Drought (Light Yellow)
        - 4: Normal/Above (Light Green)
    """)
    st_folium = st.components.v1.html(m._repr_html_(), height=600)

# Display some information about the uploaded file
else:
    st.write("Please upload the GeoJSON file containing the vectorized SPI data.")


















