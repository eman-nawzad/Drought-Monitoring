import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd

# Define dataset paths
data_file = "data/spi.geojson"  # Replace with the correct path to your GeoJSON file

# Load the dataset
gdf = gpd.read_file(data_file)

# Display the full attribute table
st.subheader("Attribute Table")
st.write(gdf)  # Display the entire GeoDataFrame to inspect column names

# Sidebar
st.sidebar.title("SPI Drought Severity Map Viewer")
show_all_layers = st.sidebar.checkbox("Show All Layers")

# Define SPI range categories and corresponding drought severity
spi_categories = {
    "Not a drought": {"min": 2.00, "max": float("inf")},
    "Very Wet": {"min": 1.50, "max": 1.99},
    "Moderately Wet": {"min": 1.00, "max": 1.49},
    "Near Normal": {"min": -0.99, "max": 0.99},
    "Moderately Dry": {"min": -1.00, "max": -1.49},
    "Severely Dry": {"min": -1.50, "max": -1.99},
    "Extremely Dry": {"min": float("-inf"), "max": -2.00},
}

# Function to classify drought severity based on SPI
def classify_drought_severity(spi_value):
    for category, range_ in spi_categories.items():
        if range_["min"] <= spi_value <= range_["max"]:
            return category
    return "Unknown"  # In case no category matches

# Allow users to select months
month_columns = [
    col for col in gdf.columns
    if col.lower() in ["january", "february", "march", "april", "may", "june", 
                       "july", "august", "september", "october", "november", "december"]
]

selected_months = st.sidebar.multiselect("Select Months", month_columns, default=month_columns)

# Ensure the selected_months list is not empty before computing the average
if selected_months:
    gdf["selected_months_avg"] = gdf[selected_months].mean(axis=1)
else:
    gdf["selected_months_avg"] = 0

# Apply drought severity classification based on selected months average
gdf["drought_severity"] = gdf["selected_months_avg"].apply(classify_drought_severity)

# Sidebar filter for drought severity categories
drought_filter = st.sidebar.selectbox(
    "Filter by Drought Category", ["All"] + list(spi_categories.keys())
)

# Filter the dataset based on the drought category
if drought_filter != "All":
    filtered_gdf = gdf[gdf["drought_severity"] == drought_filter]
else:
    filtered_gdf = gdf

# Sidebar warning message for no data
if filtered_gdf.empty:
    st.sidebar.warning(f"No data available for the selected drought category '{drought_filter}'. Please try a different selection.")
else:
    st.sidebar.success(f"Displaying data for the selected drought category '{drought_filter}'.")

# Create map centered on the centroid of the dataset
centroid = filtered_gdf.geometry.centroid
avg_lat = centroid.y.mean()
avg_lon = centroid.x.mean()
m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

# Function to generate popups with drought severity
def generate_popup(row):
    popup_content = f"<strong>Feature Information</strong><br>"
    severity_class = row["drought_severity"]
    popup_content += f"<b>Drought Severity:</b> {severity_class}<br>"
    popup_content += f"<b>Average SPI (Selected Months):</b> {row['selected_months_avg']:.2f}<br>"
    return popup_content

# Function to set color based on drought severity
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































