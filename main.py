from csv_handler import *
from csv_handler import csv_handling, start_watching_csv_folder

def csv_to_rdf_conversion(column_labels, csv_folder, classified_csv,rdf_folder):
    csv_handling(column_labels, csv_folder, classified_csv)
    # Start watching for changes in the original files
    start_watching_csv_folder(column_labels, csv_folder, classified_csv,rdf_folder)

if __name__ == "__main__":
    column_labels = ['time', 'speed', 'lat', 'lon']
    csv_folder = 'csv'
    classified_csv = 'classified_csv'
    os.makedirs(classified_csv, exist_ok=True)
    rdf_folder = 'http://localhost:3030/#/dataset/rdf_data/upload'
    os.makedirs(rdf_folder, exist_ok=True)
    csv_to_rdf_conversion(column_labels, csv_folder, classified_csv,rdf_folder)