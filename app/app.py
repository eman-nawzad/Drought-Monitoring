import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd

# Define dataset paths
data_file = "data/SPI_.geojson"  # Replace with the correct path to your GeoJSON file

# Load the dataset
gdf = gpd.read_file(data_file)

# Display the full attribute table and column names
st.subheader("Attribute Table")
st.write(gdf)  # Display the entire GeoDataFrame to inspect column names
st.write("Columns available in the dataset:", gdf.columns)

# Check if 'drought_severity' exists in the dataset
if 'drought_severity' not in gdf.columns:
    st.error("The dataset does not contain a 'drought_severity' column. Please check the column names.")
else:
    # Display the updated GeoDataFrame with drought severity
    st.subheader("Drought Severity Information")
    st.write(gdf[['id', 'drought_severity']])  # Display 'id' and 'drought_severity' columns

    # Sidebar
    st.sidebar.title("SPI Drought Severity Map Viewer")
    show_all_layers = st.sidebar.checkbox("Show All Layers")

    # Drought severity classes and colors
    drought_severity_classes = {
        "Extreme Drought": "red",
        "Severe Drought": "orange",
        "Moderate Drought": "yellow",
        "Mild Drought": "blue",
        "Normal/Above": "green"
    }

    # Sidebar filter for drought severity
    drought_filter = st.sidebar.selectbox(
        "Filter by Drought Severity", ["All"] + list(drought_severity_classes.keys())
    )
    
    # Filter the dataset based on drought severity
    filtered_gdf = gdf.copy()
    if drought_filter != "All":
        filtered_gdf = gdf[gdf['drought_severity'] == drought_filter]

    # Sidebar warning message for no data
    if filtered_gdf.empty:
        st.sidebar.warning(f"No data available for the selected filter '{drought_filter}'. Please try a different selection.")
    else:
        st.sidebar.success(f"Displaying data for '{drought_filter}' severity.")

    # Create map centered on the centroid of the dataset
    centroid = filtered_gdf.geometry.centroid
    avg_lat = centroid.y.mean()
    avg_lon = centroid.x.mean()
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

    # Function to generate popups with drought severity
    def generate_popup(row):
        popup_content = f"<strong>Feature Information</strong><br>"
        severity_class = row['drought_severity']
        popup_content += f"<b>Drought Severity:</b> {severity_class}<br>"
        return popup_content

    # Function to set color based on drought severity
    def get_style_function(feature):
        severity = feature['properties']['drought_severity']
        color = drought_severity_classes.get(severity, "gray")  # Default to gray if no matching class
        return {"color": color, "weight": 1, "fillOpacity": 0.6}

    # Add GeoJSON layer with popups and colors
    def add_geojson_layer(gdf, map_obj):
        geo_json = folium.GeoJson(
            gdf,
            style_function=get_style_function,
            name="Drought Severity"  # Set the name for LayerControl
        )
        for _, row in gdf.iterrows():
            popup = folium.Popup(generate_popup(row), max_width=300)
            geo_json.add_child(popup)
        geo_json.add_to(map_obj)

    # Add the filtered GeoJSON layer
    add_geojson_layer(filtered_gdf, m)

    # Adjust the map view to the bounding box of the selected class
    if drought_filter != "All" and not filtered_gdf.empty:
        # Get the bounding box of the selected class
        bounds = filtered_gdf.geometry.total_bounds  # [minx, miny, maxx, maxy]
        # Zoom to the bounding box
        m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

    folium.LayerControl().add_to(m)

    # Display the map
    st_folium(m, width=700, height=500)




























