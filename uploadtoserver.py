from imports import requests

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
    else:
        print('Error uploading file:', response.text)

if __name__ == "__main__":
    # Define the Fuseki server URL and dataset name
    ttl_folder = 'rdf_folder'
    fuseki_url = 'http://localhost:3030/rdf_data/data'
    for filename in os.listdir(rdf_folder):
        if filename.endswith(".ttl"):
            file_path = os.path.join(rdf_folder, filename)
            upload_ttl_to_fuseki(fuseki_url, file_path)
