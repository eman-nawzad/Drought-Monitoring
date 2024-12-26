import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt

# Load your SPI GeoJSON data
def load_spi_data():
    # Use geopandas to load the SPI GeoJSON (file is in the same directory as app.py)
    gdf = gpd.read_file('SPI_12_GeoJSON.geojson')  # File is in the same directory as app.py
    return gdf

# Function to display SPI data on a map
def plot_spi_map():
    gdf = load_spi_data()
    
    # Create a simple map of SPI data
    fig, ax = plt.subplots(figsize=(10, 6))
    gdf.plot(ax=ax, cmap='viridis', legend=True)
    ax.set_title("SPI 12 Month (2023) - Drought Index")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    st.pyplot(fig)

# Function to display information and instructions
def display_info():
    st.title("Drought Monitoring Web Application")
    st.write(
        """
        This application displays the SPI data for monitoring drought conditions. The SPI data is used to assess precipitation deficit and drought severity. 
        The map above shows the SPI data for the year 2023. Higher values indicate wetter conditions, and lower values indicate drier conditions.
        """
    )

# Main application function
def main():
    display_info()
    plot_spi_map()

if __name__ == "__main__":
    main()

import streamlit as st

# Legend HTML and CSS
legend_html = """
<div style="
    position: fixed; 
    bottom: 10px; 
    left: 10px; 
    border:2px solid grey; 
    z-index:9999; 
    background-color:white; 
    padding:10px; 
    font-size:14px;">
    <b>Legend:</b>
    <ul style="list-style-type:none; padding-left: 0;">
      <li><span style="background-color:#1f78b4; color:white; padding:2px 5px;">&nbsp;&nbsp;</span> SPI > 2 (Very Wet)</li>
      <li><span style="background-color:#33a02c; color:white; padding:2px 5px;">&nbsp;&nbsp;</span> 1.5 < SPI <= 2 (Moderately Wet)</li>
      <li><span style="background-color:#ff7f00; color:white; padding:2px 5px;">&nbsp;&nbsp;</span> -1.5 < SPI <= -1.5 (Moderately Dry)</li>
      <li><span style="background-color:#e31a1c; color:white; padding:2px 5px;">&nbsp;&nbsp;</span> SPI <= -2 (Very Dry)</li>
    </ul>
</div>
"""

# Add the legend to the Streamlit app
st.components.v1.html(legend_html, height=200)
