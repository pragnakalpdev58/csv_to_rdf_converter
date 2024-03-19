from csv_handler import csv_handling, start_watching_csv_folder
from uploadtoserver import upload_ttl_to_fuseki
from imports import os

def csv_to_rdf_conversion(column_labels, csv_folder, classified_csv,rdf_folder):
    csv_handling(column_labels, csv_folder, classified_csv)
    # Start watching for changes in the original files
    start_watching_csv_folder(column_labels, csv_folder, classified_csv,rdf_folder)

if __name__ == "__main__":
    column_labels = ['time', 'speed', 'lat', 'lon']
    csv_folder = 'csv'
    classified_csv = 'classified_csv'
    os.makedirs(classified_csv, exist_ok=True)
    rdf_folder = 'rdf_folder'
    os.makedirs(rdf_folder, exist_ok=True)
    csv_to_rdf_conversion(column_labels, csv_folder, classified_csv,rdf_folder)
    fuseki_url = 'http://localhost:3030/test/data'
    named_graph_uri = 'http://www.semanticweb.org/viren/ontologies/2024/0/RideQuality'  # Specify the named graph URI

    for filename in os.listdir(rdf_folder):
        if filename.endswith(".ttl"):
            file_path = os.path.join(rdf_folder, filename)
            filename = os.path.splitext(filename)[0]
            filename = filename.replace(' ', '_')
            upload_ttl_to_fuseki(fuseki_url=((f"{fuseki_url}?graph={named_graph_uri}/{filename}")), file_path=file_path)
