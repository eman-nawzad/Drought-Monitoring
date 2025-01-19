import folium
import geopandas as gpd

# Load your GeoJSON files (LST and SPI)
lst_gdf = gpd.read_file('/path/to/LST.geojson')
spi_gdf = gpd.read_file('/path/to/SPI-J.geojson')

# Initialize a map centered around a specific latitude and longitude
m = folium.Map(location=[latitude, longitude], zoom_start=10)

# Add LST layer to the map
folium.GeoJson(
    lst_gdf,
    name='LST Layer',
    tooltip=folium.GeoJsonTooltip(fields=lst_gdf.columns, aliases=lst_gdf.columns)
).add_to(m)

# Add SPI layer to the map
folium.GeoJson(
    spi_gdf,
    name='SPI Layer',
    tooltip=folium.GeoJsonTooltip(fields=spi_gdf.columns, aliases=spi_gdf.columns)
).add_to(m)

# Add layer control to switch between layers
folium.LayerControl().add_to(m)

# Save the map to an HTML file
m.save('/path/to/interactive_map.html')









































