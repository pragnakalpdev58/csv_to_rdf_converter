from imports import requests

# Define the Fuseki server URL and dataset name
fuseki_url = 'http://localhost:3030/rdf_data/data'
file_path = '/home/pragnakalp-l-12/Desktop/viren/gitHub/csv_to_rdf_converter/rdf_files/test.ttl'

# Read the .ttl file
with open(file_path, 'rb') as file:
    ttl_content = file.read()

# Set the headers for the HTTP request
headers = {
    'Content-Type': 'text/turtle',  # Specify the content type as Turtle
}

# Send the HTTP POST request to upload the file
response = requests.post(fuseki_url, data=ttl_content, headers=headers)

# Check if the upload was successful
if response.status_code == 200:
    print('File uploaded successfully!')
else:
    print('Error uploading file:', response.text)
