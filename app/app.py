import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from app.utils import convert_geotiff_to_geojson

# App
 title and description
st.title("Drought Monitoring Map")
st.markdown("Explore and visualize drought conditions using SPI data.")

# Sidebar: File upload and data source selection
st.sidebar.header("Data Source")
data_source = st.sidebar.radio(
    "Select Data Source:",
    ("Default SPI Data", "Upload Custom GeoTIFF")
)

# Process default SPI file or uploaded file
if data_source == "Default SPI Data":
    st.sidebar.info("Using default SPI data: SPI_12_Month_2023.tif")
    geojson_path = "data/processed_spi.geojson"
else:
    uploaded_file = st.sidebar.file_uploader("Upload SPI GeoTIFF file", type=["tif", "tiff"])
    if uploaded_file:
        st.sidebar.info("Processing uploaded file...")
        geojson_path = convert_geotiff_to_geojson(uploaded_file)
    else:
        st.warning("Please upload a GeoTIFF file to proceed.")
        st.stop()

# Load GeoJSON data
def render_map(geojson_path):
    gdf = gpd.read_file(geojson_path)

    m = folium.Map(location=[33.3, 44.4], zoom_start=6, tiles="cartodbpositron")
    folium.GeoJson(
        gdf,
        name="SPI Data",
        style_function=lambda feature: {
            'fillColor': feature['properties'].get('color', '#FFEDA0'),
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0.6,
        },
    ).add_to(m)

    folium.LayerControl().add_to(m)
    return m

st.markdown("### SPI Data Visualization")
map_object = render_map(geojson_path)
st_folium(map_object, width=700, height=500)

