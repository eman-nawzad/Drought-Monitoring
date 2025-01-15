import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd

# Define dataset paths
data_file = "data/SPI.geojson"  # Replace with the correct path to your GeoJSON file

# Load the dataset
gdf = gpd.read_file(data_file)

# Display the full attribute table
st.subheader("Attribute Table")
st.write(gdf)  # This will display the entire GeoDataFrame to inspect column names

# Sidebar
st.sidebar.title("SPI Drought Severity Map Viewer")
show_all_layers = st.sidebar.checkbox("Show All Layers")

# Check if 'drought_severity' column exists in the data
if 'drought_severity' not in gdf.columns:
    st.error("The dataset does not contain a 'drought_severity' column.")
else:
    # Drought severity classes
    drought_severity_classes = {
        0: "Extreme Drought (Red)",
        1: "Severe Drought (Orange)",
        2: "Moderate Drought (Yellow)",
        3: "Mild Drought (Light Yellow)",
        4: "Normal/Above (Green)"
    }

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
        st.sidebar.warning(f"No data available for the selected severity in the '{data_file}' dataset. Please try a different selection.")
    else:
        st.sidebar.success(f"Displaying data from the '{data_file}' dataset.")

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

    # Add the filtered GeoJSON layer
    add_geojson_layer(filtered_gdf, m)

    folium.LayerControl().add_to(m)

    # Display the map
    st_folium(m, width=700, height=500)





















