from imports import *  # Import necessary modules

def create_subject_and_triple(idx, row, PATCH):
    try:
        # Extract latitude, longitude, and movement classification from the row
        latitude = Literal(row['lat'])
        longitude = Literal(row['lon'])
        movement_classification = row["MovementClassification"]

        # Determine ride quality and corresponding PATCH
        if movement_classification in ("High Acceleration", "Normal Acceleration"):
            ride_quality = movement_classification
            sub = PATCH.PatchGoodToGo
        elif movement_classification == "Normal Braking":
            ride_quality = movement_classification
            sub = PATCH.PatchDriveCaution
        elif movement_classification == "High Braking":
            ride_quality = movement_classification
            sub = PATCH.PatchWithBumps
        else:
            ride_quality = movement_classification
            sub = PATCH.PatchGoodToGo

        return sub, ride_quality, latitude, longitude  # Return PATCH, ride quality, latitude, and longitude

    except Exception as e:
        print(f"Error in create_subject_and_triple: {e}")  # Log error
        return None, None, None, None  # Return None for all values in case of error


road_section_list = []
def csv_to_rdf(csv_file_path, rdf_folder):
    try:
        # rdf_file_name = os.path.splitext(filename)[0]
        df = pd.read_csv(csv_file_path)
        lat = df['lat'].tolist()
        if len(lat) > 0:
            first_index = 0
            last_index = len(lat) - 1
            # print("last_index",last_index)

        # Create an RDF graph
        graph = Graph()
        # Define namespaces
        PATCH = Namespace("http://www.semanticweb.org/viren/ontologies/2024/0/RideQuality#")
        graph.bind("PATCH", PATCH)

        # Open and read the CSV file
        with open(csv_file_path, newline='') as csvfile:
            csvreader = csv.DictReader(csvfile)
            triples_batch = []
            idx = 0
            while True:
                rows = []
                while len(rows) < 5:
                    try:
                        row = next(csvreader)
                        rows.append(row)
                    except StopIteration:
                        break

                if not rows:
                    break  # No more rows left to read

                for row in rows:
                    sub, ride_quality, latitude, longitude = create_subject_and_triple(idx, row, PATCH)
                    latitude = Literal(row['lat'], datatype=XSD.decimal)
                    longitude = Literal(row['lon'], datatype=XSD.decimal)
                    subject = PATCH[f"{idx + 1}"]
                    triples_batch.extend([(subject, RDF.type, sub),
                                          (subject, PATCH["hasLatitude"], latitude),
                                          (subject, PATCH["hasLongitude"], longitude),
                                          (subject, PATCH["hasPatchQality"], Literal(ride_quality))])
                    idx += 1

            # Add the batch of triples to the graph
            graph += triples_batch

            rdf_file_path = os.path.join(rdf_folder, "temp.ttl")

        graph.serialize(rdf_file_path,format='turtle')

    except Exception as e:
        print(f"Error in csv_to_rdf: {e}")  # Log error

def process_file(csv_folder, rdf_folder, filename):
    try:
        csv_file_path=os.path.join(csv_folder, filename)
        rdf_folder=rdf_folder
        csv_to_rdf(csv_file_path,rdf_folder)

    except Exception as e:
        print(f"Error in process_file for {filename}: {e}")  # Log error

def rdf_generation(csv_folder, rdf_folder):
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
        print(f"Error in rdf_generation: {e}")  # Log error