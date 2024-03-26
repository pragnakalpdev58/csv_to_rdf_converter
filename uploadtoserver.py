from imports import requests, os

# Function to upload a .ttl file to a Jena Fuseki server
def upload_ttl_to_fuseki(rdf_local_copy_path,rdf_local_copy_filename):
    jena_server_url = 'http://localhost:3030/RoadSections/data'
    ontology_uri = 'http://www.semanticweb.org/viren/ontologies/2024/0/RideQuality'  # Specify the named graph URI

    fuseki_url = f"{jena_server_url}?graph={ontology_uri}/{rdf_local_copy_filename}"
    # Read the .ttl file
    with open(rdf_local_copy_path, 'rb') as file:
        ttl_content = file.read()

    # Set the headers for the HTTP request
    headers = {
        'Content-Type': 'text/turtle',  # Specify the content type as Turtle
    }

    # Send the HTTP POST request to upload the file
    response = requests.post(fuseki_url, data=ttl_content, headers=headers)