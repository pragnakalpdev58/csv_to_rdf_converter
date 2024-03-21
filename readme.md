# CSV to RDF Conversion and Fuseki Server Integration

This project automates the process of converting CSV data into RDF format and integrating it with a Jena Fuseki server for advanced querying and reasoning capabilities.

## Table of Contents

- [Project Overview](#project-overview)
- [Components](#components)
- [How to Run](#how-to-run)

## Project Overview

The project consists of several Python scripts that handle CSV file operations, RDF generation, and uploading RDF files to a Jena Fuseki server. Here are the main components:

- `csv_handler.py`: Handles CSV file operations such as adding a row at the top, removing columns, removing duplicates, and classifying movement.
- `rdf_generation.py`: Converts CSV files to RDF format using RDFLib, calculates severity using a sliding window approach, classifies movement based on severity, and serializes RDF graphs into Turtle format.
- `uploadtoserver.py`: Provides functions to upload .ttl files to a Jena Fuseki server using HTTP POST requests, specifying the content type as Turtle.
- `main.py`: Orchestrates the overall process by calling functions from other modules, setting up necessary parameters, and executing the CSV to RDF conversion and server upload tasks.

## Components

### csv_handler.py

Handles CSV file operations such as:
- Adding a row at the top
- Removing columns
- Removing duplicates
- Classifying movement
- Monitoring the CSV folder for changes

### rdf_generation.py

Converts CSV files to RDF format using RDFLib and handles severity calculation and movement classification.

### uploadtoserver.py

Provides functions to upload .ttl files to a Jena Fuseki server using HTTP POST requests.

### main.py

Orchestrates the overall process by setting up parameters and executing the conversion and upload tasks.

## How to Run

1. Install Python on your system if not already installed.
2. Install required Python packages listed in the `requirements.txt` file using the following command:
   ```
   pip install -r requirements.txt
   ```
3. Set up a Jena Fuseki server and create a dataset for storing RDF data.
4. Modify the configuration parameters in `main.py` and other relevant scripts (e.g., server URL, folder paths).
5. Place your CSV files in the specified CSV folder.
6. Run the `main.py` script using the following command:
   ```
   python main.py
   ```
7. Monitor the console output for progress and status messages.
8. Access the Fuseki server to query and reason over the uploaded RDF data.