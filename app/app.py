import streamlit as st
import geopandas as gpd
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import shape
from io import BytesIO

# Load your SPI GeoTIFF data
def load_spi_data():
    # Use rasterio to load your SPI GeoTIFF
    with rasterio.open('SPI_12_Month_2023.tif') as src:
        data = src.read(1)  # Reading the first band (assuming it's single-band)
        transform = src.transform
    return data, transform

# Function to display SPI data on a map
def plot_spi_map():
    data, transform = load_spi_data()
    
    # Create a simple map of SPI data
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(data, cmap='viridis', origin='upper', extent=(transform[2], transform[2] + transform[0] * data.shape[1], transform[5] + transform[4] * data.shape[0], transform[5]))
    ax.set_title("SPI 12 Month (2023) - Drought Index")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    plt.colorbar(ax.imshow(data, cmap='viridis'), ax=ax, label="SPI Value")

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


