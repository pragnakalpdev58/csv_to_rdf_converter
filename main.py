from csv_handler import csv_handling, start_watching_csv_folder,end_filename
from uploadtoserver import upload_ttl_to_fuseki
from imports import os, time,shutil

def csv_to_rdf_conversion(column_labels, csv_folder, classified_csv,rdf_folder):
    csv_handling(column_labels, csv_folder, classified_csv)
    # Start watching for changes in the original files
    start_watching_csv_folder(column_labels, csv_folder, classified_csv,rdf_folder)

def main():
    column_labels = ['time', 'speed', 'lat', 'lon']
    csv_folder = 'csv'
    os.makedirs(csv_folder, exist_ok=True)

    classified_csv = 'classified_csv'
    os.makedirs(classified_csv, exist_ok=True)

    rdf_folder = 'rdf_folder'
    os.makedirs(rdf_folder, exist_ok=True)

    csv_to_rdf_conversion(column_labels, csv_folder, classified_csv,rdf_folder)

    fuseki_url = 'http://localhost:3030/RoadSections/data'
    named_graph_uri = 'http://www.semanticweb.org/viren/ontologies/2024/0/RideQuality'  # Specify the named graph URI

    rdf_local_copy = "rdf_local_copy"
    os.makedirs(rdf_local_copy, exist_ok=True)

    for filename in os.listdir(rdf_folder):
        if filename.endswith(".ttl"):
            temp_file_path = os.path.join(rdf_folder, filename)
            road_section_list = end_filename(classified_csv)
            rdf_local_copy_filename = f"RoadSection_Start:{road_section_list[0]}_End:{road_section_list[1]}.ttl"
            rdf_local_copy_path = os.path.join(rdf_local_copy, rdf_local_copy_filename)
            shutil.move(temp_file_path,rdf_local_copy_path)
            rdf_local_copy_filename = rdf_local_copy_filename.replace(' ', '')
            upload_ttl_to_fuseki(fuseki_url=((f"{fuseki_url}?graph={named_graph_uri}/{rdf_local_copy_filename}")), file_path=rdf_local_copy_path)


if __name__ == "__main__":
    main()
