# Project Execution Instructions

## Prerequisites
Ensure that the sensor data is logged into a CSV file. If the logging device is unavailable, place an existing CSV file with the required data in the project's root folder. Adjust the path in the 'autoadd' script, and specify the target file path accordingly.

## Installation
1. Create and activate a virtual environment.
2. Install the necessary dependencies by executing the following command:
   ```bash
   pip install -r requirements.txt
   ```

## Execution
Run the main script, `main.py`. If logging device is not available , run `autoadd.py` after executing `main.py`.
Note: Adjust the length of the list in the code to match your preferences. If emulating a sensor, set the list value to 1.

Upon completion, the script will automatically terminate, providing classified CSV and an RDF/XML file as output.

Follow these instructions for a seamless execution of the project.