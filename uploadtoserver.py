# Import the necessary library
from imports import requests  # Assuming 'imports' is a module containing the 'requests' library

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
    else:
        print('Error uploading file:', response.text)

if __name__ == "__main__":
    # Define the Fuseki server URL and folder containing .ttl files
    rdf_folder = 'rdf_folder'  # Assuming 'rdf_folder' is the directory containing .ttl files
    fuseki_url = 'http://localhost:3030/rdf_data/data'  # URL for the Fuseki server and dataset
    for filename in os.listdir(rdf_folder):  # Iterate through files in the directory
        if filename.endswith(".ttl"):  # Check if the file is a .ttl file
            file_path = os.path.join(rdf_folder, filename)  # Get the full file path
            upload_ttl_to_fuseki(fuseki_url, file_path)  # Upload the .ttl file to Fuseki
