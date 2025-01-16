import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd

# Define dataset paths
data_file = "data/SPI_.geojson"  # Replace with the correct path to your GeoJSON file

# Load the dataset
gdf = gpd.read_file(data_file)

# Display the full attribute table
st.subheader("Attribute Table")
st.write(gdf)  # Display the entire GeoDataFrame to inspect column names

# Function to classify SPI into severity classes
def classify_severity(spi_value):
    if spi_value < -2.00:
        return "Extreme Drought"
    elif spi_value >= -2.00 and spi_value < -1.50:
        return "Severe Drought"
    elif spi_value >= -1.50 and spi_value < -1.00:
        return "Moderate Drought"
    elif spi_value >= -1.00 and spi_value < 0.00:
        return "Mild Drought"
    else:
        return "Normal/Above"

# Apply the classification function to SPI values (assuming SPI is in a column named 'SPI_12_month')
gdf['calculated_severity'] = gdf['SPI_12_month'].apply(classify_severity)

# Compare the actual severity with the calculated severity
gdf['match'] = gdf['calculated_severity'] == gdf['drought_severity']

# Display comparison table
st.subheader("Comparison of SPI Severity and Existing Severity")
st.write(gdf[['Month', 'SPI_12_month', 'calculated_severity', 'drought_severity', 'match']])

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

# Sidebar filter for drought severity
drought_severity_classes = {
    "Extreme Drought": 0,
    "Severe Drought": 1,
    "Moderate Drought": 2,
    "Mild Drought": 3,
    "Normal/Above": 4
}
drought_severity_colors = {
    "Extreme Drought": "red",
    "Severe Drought": "orange",
    "Moderate Drought": "yellow",
    "Mild Drought": "blue",
    "Normal/Above": "green"
}

drought_filter = st.sidebar.selectbox(
    "Filter by Drought Severity", ["All"] + list(drought_severity_classes.keys())
)
if drought_filter != "All":
    filtered_gdf = gdf[gdf['calculated_severity'] == drought_filter]
else:
    filtered_gdf = gdf

# Create map centered on the centroid of the dataset
centroid = filtered_gdf.geometry.centroid
avg_lat = centroid.y.mean()
avg_lon = centroid.x.mean()
m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

# Function to generate popups with drought severity
def generate_popup(row):
    popup_content = f"<strong>Feature Information</strong><br>"
    severity_class = row['calculated_severity']
    popup_content += f"<b>Drought Severity:</b> {severity_class}<br>"
    popup_content += f"<b>Average SPI (Selected Months):</b> {row['selected_months_avg']:.2f}<br>"
    return popup_content

# Function to set color based on drought severity
def get_style_function(feature):
    severity = feature['properties']['calculated_severity']
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
    bounds = filtered_gdf.geometry.total_bounds  # [minx, miny, maxx, maxy]
    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

folium.LayerControl().add_to(m)

# Display the map
st_folium(m, width=700, height=500)






























