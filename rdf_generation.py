from imports import *  # Import necessary modules

def create_subject_and_triple(idx, row, patch):
    try:
        # Extract latitude, longitude, and movement classification from the row
        latitude = Literal(row['lat'])
        longitude = Literal(row['lon'])
        movement_classification = row["MovementClassification"]

        # Determine ride quality and corresponding patch
        if movement_classification in ("High Acceleration", "Normal Acceleration"):
            ride_quality = movement_classification
            sub = patch.PatchGoodToGo
        elif movement_classification == "Normal Braking":
            ride_quality = movement_classification
            sub = patch.PatchDriveCaution
        elif movement_classification == "High Braking":
            ride_quality = movement_classification
            sub = patch.PatchWithBumps
        else:
            ride_quality = movement_classification
            sub = patch.PatchGoodToGo

        return sub, ride_quality, latitude, longitude  # Return patch, ride quality, latitude, and longitude

    except Exception as e:
        print(f"Error in create_subject_and_triple: {e}")  # Log error
        return None, None, None, None  # Return None for all values in case of error

def csv_to_rdf(csv_file_path, rdf_folder):
    try:
        # rdf_file_name = os.path.splitext(filename)[0]
        df = pd.read_csv(csv_file_path)
        speed = df['speed'].tolist()
        if len(speed) > 0:
            first_index = 0
            last_index = len(speed) - 1

        # Create an RDF graph
        graph = Graph()
        # Define namespaces
        patch = Namespace("http://www.semanticweb.org/viren/ontologies/2024/0/RideQuality#")
        rq = Namespace("http://www.semanticweb.org/viren/ontologies/2024/0/RideQuality#RideQuality")
        graph.bind("patch", patch)
        graph.bind("rq", rq)

        # Open and read the CSV file
        with open(csv_file_path, newline='') as csvfile:
            csvreader = csv.DictReader(csvfile)
            triples_batch = []
            for idx, row in enumerate(csvreader):
                if idx != first_index and idx != last_index:
                    sub, ride_quality, latitude, longitude = create_subject_and_triple(idx, row, patch)
                    if sub is not None:
                        subject = patch[f"{idx + 1}"]
                        triples_batch.extend([(subject, RDF.type, sub),
                                              (subject, patch.latitude, latitude),
                                              (subject, patch.longitude, longitude),
                                              (subject, rq.PatchQuality, Literal(ride_quality))])

                elif idx == first_index:
                    sub, ride_quality, latitude, longitude = create_subject_and_triple(idx, row, patch)
                    if sub is not None:

                        subject = patch[f"{idx + 1}"]
                        triples_batch.extend([(subject, RDF.type, sub),
                                              (subject, patch.latitude, latitude),
                                              (subject, patch.longitude, longitude),
                                              (subject, rq.PatchQuality, Literal(ride_quality))])
                        latitude_value = latitude.value  # Extract the value from the RDFLib Literal
                        longitude_value = longitude.value  # Extract the value from the RDFLib Literal
                        test_tuple = (latitude_value,longitude_value)
                        res = str(test_tuple).replace(' ', '')
                        road_section_list.append(test_tuple)
                        # print((latitude_value,longitude_value))

                elif idx == last_index:
                    sub, ride_quality, latitude, longitude = create_subject_and_triple(idx, row, patch)
                    if sub is not None:
                        subject = patch[f"{idx + 1}"]
                        triples_batch.extend([(subject, RDF.type, sub),
                                              (subject, patch.latitude, latitude),
                                              (subject, patch.longitude, longitude),
                                              (subject, rq.PatchQuality, Literal(ride_quality))])
                        test_tuple = (latitude_value,longitude_value)
                        res = str(test_tuple).replace(' ', '')
                        road_section_list.append(test_tuple)
                        # print((latitude_value,longitude_value))

                else:
                    pass

            # Add the batch of triples to the graph
            graph += triples_batch
            # Serialize the entire graph to the RDF file
        rdf_file_path = os.path.join(rdf_folder, f"RoadSection_Start:{road_section_list[0]}_End:{road_section_list[1]}.ttl")
        # print(road_section_list)
        graph.serialize(rdf_file_path, format='turtle')

    except Exception as e:
        print(f"Error in csv_to_rdf: {e}")  # Log error

def process_file(csv_folder, rdf_folder, filename):
    try:
        csv_to_rdf(csv_file_path=os.path.join(csv_folder, filename), rdf_folder=rdf_folder)

    except Exception as e:
        print(f"Error in process_file for {filename}: {e}")  # Log error
road_section_list = []
def run_script(csv_folder, rdf_folder):
    try:
        start_time = time.time()
        os.makedirs(rdf_folder, exist_ok=True)

        # Process CSV files concurrently
        with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count()) as executor:
            futures = [executor.submit(process_file, csv_folder, rdf_folder, filename)
                       for filename in os.listdir(csv_folder) if filename.lower().endswith((".csv"))]

        concurrent.futures.wait(futures)
        end_time = time.time()
        print(f"Time taken for csv to rdf conversion: {end_time-start_time} seconds")

    except Exception as e:
        print(f"Error in run_script: {e}")  # Log error

if __name__ == "__main__":
    try:
        start_time = time.time()

        # Define input and output folders
        csv_folder = "classified_csv"
        rdf_folder = "rdf_files"

        # Run the script to convert CSV files to RDF
        run_script(csv_folder, rdf_folder)

        end_time = time.time()
        execution_time = end_time - start_time
        print("Start Time =", start_time)
        print("End Time =", end_time)
        print("Execution Time =", execution_time)

    except Exception as e:
        print(f"Error in main script: {e}")  # Log error
