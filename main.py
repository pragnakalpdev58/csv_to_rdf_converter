from csv_handler import csv_handling, start_watching_csv_folder
from imports import os, time,shutil

def csv_to_rdf_conversion(column_labels, csv_folder, classified_csv,rdf_folder, rdf_local_copy):
    csv_handling(column_labels, csv_folder, classified_csv)
    # Start watching for changes in the original files
    start_watching_csv_folder(column_labels, csv_folder, classified_csv,rdf_folder, rdf_local_copy)

def main():
    column_labels = ['time', 'speed', 'lat', 'lon']
    csv_folder = 'csv'
    os.makedirs(csv_folder, exist_ok=True)

    classified_csv = 'classified_csv'
    os.makedirs(classified_csv, exist_ok=True)

    rdf_folder = 'rdf_folder'
    os.makedirs(rdf_folder, exist_ok=True)

    rdf_local_copy = "rdf_local_copy"
    os.makedirs(rdf_local_copy, exist_ok=True)

    csv_to_rdf_conversion(column_labels, csv_folder, classified_csv, rdf_folder, rdf_local_copy)

if __name__ == "__main__":
    main()
