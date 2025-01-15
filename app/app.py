import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd

# Define dataset paths
data_files = {
    "SPI Drought Severity": "data/SPI_12_2023.geojson"  # Replace with the correct path to your GeoJSON file
}

# Drought severity classes
drought_severity_classes = {
    0: "Extreme Drought (Red)",
    1: "Severe Drought (Orange)",
    2: "Moderate Drought (Yellow)",
    3: "Mild Drought (Light Yellow)",
    4: "Normal/Above (Green)"
}

# Sidebar
st.sidebar.title("SPI Drought Severity Map Viewer")
show_all_layers = st.sidebar.checkbox("Show All Layers")
selected_file = st.sidebar.selectbox("Choose a dataset", list(data_files.keys()))

# Load the selected dataset
gdf = gpd.read_file(data_files[selected_file])

# Filter the dataset based on drought severity
filtered_gdf = gdf.copy()

# Sidebar filter for drought severity
drought_filter = st.sidebar.selectbox(
    "Filter by Drought Severity", ["All"] + list(drought_severity_classes.values())
)
if drought_filter != "All":
    class_value = list(drought_severity_classes.values()).index(drought_filter)  # Mapping to numeric values
    filtered_gdf = gdf[gdf['drought_severity'] == class_value]

# Sidebar warning message for no data
if filtered_gdf.empty:
    st.sidebar.warning(f"No data available for the selected severity in the '{selected_file}' dataset. Please try a different selection.")
else:
    st.sidebar.success(f"Displaying data from the '{selected_file}' dataset.")

# Create map
m = folium.Map(location=[filtered_gdf.geometry.centroid.y.mean(), filtered_gdf.geometry.centroid.x.mean()], zoom_start=12)

# Function to generate popups with drought severity
def generate_popup(row):
    popup_content = f"<strong>Feature Information</strong><br>"
    severity_class = drought_severity_classes.get(row['drought_severity'], "Unknown")
    popup_content += f"<b>Drought Severity:</b> {severity_class}<br>"
    return popup_content

def get_style_function():
    return lambda x: {"color": "blue", "weight": 1}  # Default styling for SPI data

# Add GeoJSON layer with popups
def add_geojson_layer(gdf, map_obj):
    geo_json = folium.GeoJson(
        gdf.geometry,
        style_function=get_style_function(),
        name="SPI Drought Severity"  # Set the name for LayerControl
    )
    for _, row in gdf.iterrows():
        popup = folium.Popup(generate_popup(row), max_width=300)
        geo_json.add_child(popup)
    geo_json.add_to(map_obj)

# Add layers
if show_all_layers:
    for file_name, file_path in data_files.items():
        layer_gdf = gpd.read_file(file_path)
        add_geojson_layer(layer_gdf, m)
else:
    add_geojson_layer(filtered_gdf, m)

folium.LayerControl().add_to(m)

# Display the map
st_folium(m, width=700, height=500)

# Display the attribute table
st.subheader("Attribute Table")
st.dataframe(filtered_gdf)



















