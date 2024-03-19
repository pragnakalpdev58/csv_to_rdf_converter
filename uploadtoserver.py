from imports import requests, os

# Function to upload a .ttl file to a Jena Fuseki server
def upload_ttl_to_fuseki(fuseki_url, file_path):
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
        print(f"If:{fuseki_url}")
    elif response.status_code == 201:
        print('File uploaded successfully!')
        print(f"Elif:{fuseki_url}")

    else:
        print('Error uploading file:', response.text)
        print(f"Else:{fuseki_url}")

if __name__ == "__main__":
    # Define the Fuseki server URL and folder containing .ttl files
    rdf_folder = 'rdf_folder'
    fuseki_url = 'http://localhost:3030/RoadSections/data'
    named_graph_uri = 'http://www.semanticweb.org/viren/ontologies/2024/0/RideQuality#'  # Specify the named graph URI

    for filename in os.listdir(rdf_folder):
        if filename.endswith(".ttl"):
            file_path = os.path.join(rdf_folder, filename)
            filename = os.path.splitext(filename)[0]
            upload_ttl_to_fuseki(fuseki_url=((f"{fuseki_url}?graph={filename}")), file_path=file_path)
