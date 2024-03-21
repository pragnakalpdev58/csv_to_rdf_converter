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