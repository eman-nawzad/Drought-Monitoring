# Repository for Drought Monitoring Application

This repository contains the implementation of a drought monitoring application using Python and Streamlit. The application is designed to visualize and analyze drought data, specifically focusing on the Standardized Precipitation Index (SPI).

## Repository Structure

```
- app/
  - app.py           # Main Streamlit application file
- .gitignore          # Git ignore file
- LICENSE             # License for the project
- README.md           # Project documentation (this file)
- SPI_12_GeoJSON.geojson  # GeoJSON file for SPI visualization
- requirements.txt    # Python dependencies
```

## Features

- Interactive drought monitoring map
- Visualizes the SPI data in GeoJSON format
- User-friendly interface built with Streamlit

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   ```

2. Navigate to the repository:
   ```bash
   cd <repository-folder>
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

Run the Streamlit application:
```bash
streamlit run app/app.py
```

The application will open in your default web browser.

## Data

The SPI data is provided as a GeoJSON file (`SPI_12_GeoJSON.geojson`) and is visualized in the app.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for any changes.

## License

This project is licensed under the terms of the LICENSE file in this repository.

## Contact

For any questions or feedback, please open an issue or reach out to the repository owner.





