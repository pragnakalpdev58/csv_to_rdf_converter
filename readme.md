```markdown
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
```

 1804  snap info docker
 1805  sudo apt install docker-compose
 1806  docker-compose build --build-arg JENA_VERSION=3.16.0
 1807  docker pull blankdots/jena-fuseki
 1808  docker run -p 3030:3030 blankdots/jena-fuseki
