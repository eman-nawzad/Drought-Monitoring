# Drought Monitoring Map

This project provides an interactive web application for visualizing drought conditions based on Standardized Precipitation Index (SPI) data. The app is built using **Streamlit**, **Folium**, and related geospatial libraries, allowing users to upload and analyze GeoTIFF files or use default SPI data.

## Features

- Visualize SPI data on an interactive map.
- Support for default SPI GeoTIFF files and user-uploaded files.
- Automatic conversion of GeoTIFF to GeoJSON for mapping.
- Intuitive interface for drought analysis and decision-making.

## Repository Structure

```
drought-monitoring-app/
├── app/
│   ├── app.py                # Main Streamlit application script
│   ├── utils.py              # Helper functions (e.g., for processing GeoTIFF to GeoJSON)
│   ├── map_styles.py         # Optional: Custom styling for maps
├── data/
│   ├── processed_spi.geojson # Preprocessed GeoJSON file (optional for faster loading)
│   ├── sample_spi.tif        # Sample SPI GeoTIFF file (for testing)
├── assets/
│   ├── logo.png              # App logo (if applicable)
│   ├── styles.css            # Optional: Custom CSS for Streamlit
├── requirements.txt          # List of Python dependencies
├── README.md                 # Project documentation (this file)
├── .gitignore                # Files/folders to ignore in GitHub
├── LICENSE                   # Optional: License for your project
└── SPI_12_Month_2023.tif     # Default SPI GeoTIFF file
```

## Getting Started

### Prerequisites

Ensure you have Python 3.8 or later installed on your system. Install the required Python libraries:

```bash
pip install -r requirements.txt
```

### Running the App

1. Clone this repository:
   ```bash
   git clone https://github.com/eman-nawzad/drought-monitoring-app.git
   cd drought-monitoring-app
   ```

2. Run the Streamlit app:
   ```bash
   streamlit run app/app.py
   ```

3. Open the provided URL in your web browser (default: `http://localhost:8501`).

### Using the App

- **Default SPI Data**: Use the preprocessed `SPI_12_Month_2023.tif` file for visualization.
- **Upload Custom Data**: Upload a GeoTIFF file to visualize custom SPI data.

## Dependencies

The following Python libraries are required:

- `streamlit`
- `folium`
- `streamlit-folium`
- `geopandas`
- `rasterio`
- `shapely`

Install them using:
```bash
pip install -r requirements.txt
```

## Screenshots

_Include screenshots of the app here if available._

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes or suggestions.

---

If you encounter any issues or have feature requests, feel free to open an issue on the GitHub repository.



