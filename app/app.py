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

# Check if 'SPI_12_month' exists in the dataset
if 'SPI_12_month' not in gdf.columns:
    st.error("The dataset does not contain an 'SPI_12_month' column. Please check the column names.")
else:
    # Calculate severity for SPI values
    def classify_severity(spi_value):
        if spi_value < -2.00:
            return "Extreme Drought"
        elif -1.50 <= spi_value < -2.00:
            return "Severe Drought"
        elif -1.00 <= spi_value < -1.50:
            return "Moderate Drought"
        elif -0.99 <= spi_value < 0.00:
            return "Mild Drought"
        else:
            return "Normal/Above"

    # Apply classification based on SPI value
    gdf['calculated_severity'] = gdf['SPI_12_month'].apply(classify_severity)

    # Display the updated GeoDataFrame with calculated severity
    st.subheader("Drought Severity Calculation")
    st.write(gdf[['SPI_12_month', 'calculated_severity']])  # Display SPI values and their calculated severity

    # Sidebar
    st.sidebar.title("SPI Drought Severity Map Viewer")
    show_all_layers = st.sidebar.checkbox("Show All Layers")

    # Identify columns corresponding to months
    month_columns = [
        col for col in gdf.columns
        if col.lower() in ["january", "february", "march", "april", "may", "june", 
                           "july", "august", "september", "october", "november", "december"]
    ]

    # Allow users to select months
    selected_months = st.sidebar.multiselect("Select Months", month_columns, default=month_columns)

    # Aggregate data based on selected months
    if selected_months:
        gdf["selected_months_avg"] = gdf[selected_months].mean(axis=1)
    else:
        gdf["selected_months_avg"] = 0

    # Drought severity classes and colors
    drought_severity_classes = {
        0: "Extreme Drought",
        1: "Severe Drought",
        2: "Moderate Drought",
        3: "Mild Drought",
        4: "Normal/Above"
    }

    # Drought severity colors
    drought_severity_colors = {
        0: "red",
        1: "orange",
        2: "yellow",
        3: "blue",
        4: "green"
    }

    # Filter the dataset based on drought severity
    filtered_gdf = gdf.copy()

    # Sidebar filter for drought severity
    drought_filter = st.sidebar.selectbox(
        "Filter by Drought Severity", ["All"] + list(drought_severity_classes.values())
    )
    if drought_filter != "All":
        class_value = list(drought_severity_classes.values()).index(drought_filter)  # Mapping to numeric values
        filtered_gdf = gdf[gdf['calculated_severity'] == drought_filter]

    # Sidebar warning message for no data
    if filtered_gdf.empty:
        st.sidebar.warning(f"No data available for the selected filters in the '{data_file}' dataset. Please try a different selection.")
    else:
        st.sidebar.success(f"Displaying data from the '{data_file}' dataset.")

    # Create map centered on the centroid of the dataset
    centroid = filtered_gdf.geometry.centroid
    avg_lat = centroid.y.mean()
    avg_lon = centroid.x.mean()
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

    # Function to generate popups with drought severity
    def generate_popup(row):
        popup_content = f"<strong>Feature Information</strong><br>"
        severity_class = drought_severity_classes.get(row['calculated_severity'], "Unknown")
        popup_content += f"<b>Drought Severity:</b> {severity_class}<br>"
        popup_content += f"<b>Average SPI (Selected Months):</b> {row['selected_months_avg']:.2f}<br>"
        return popup_content

    # Function to set color based on drought severity
    def get_style_function(feature):
        severity = feature['properties']['calculated_severity']
        if drought_filter == "All":  # If 'All' is selected, use a neutral color (gray)
            return {"color": "gray", "weight": 1, "fillOpacity": 0.6}
        color = drought_severity_colors.get(severity, "gray")  # Default to gray if no matching class
        return {"color": color, "weight": 1, "fillOpacity": 0.6}

    # Add GeoJSON layer with popups and colors
    def add_geojson_layer(gdf, map_obj):
        geo_json = folium.GeoJson(
            gdf,
            style_function=get_style_function,
            name="SPI Drought Severity"  # Set the name for LayerControl
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




























