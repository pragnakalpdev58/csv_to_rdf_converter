from imports import *
from rdf_generation import rdf_generation

def data_classification(csv_file_path, new_row):
    """
    Adds a new row at the top of the CSV file.

    Parameters:
    - csv_file_path (str): Path to the CSV file.
    - new_row (list): New row to be added.

    Raises:
    - FileNotFoundError: If the CSV file does not exist.
    """
    try:
        with open(csv_file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            data = list(reader)
        data.insert(0, new_row)
        with open(csv_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
    except FileNotFoundError as e:
        print(f"Error: {csv_file_path} not found. {e}")

def data_cleaning(csv_file_path):
    """
    Removes columns from the CSV file.

    Parameters:
    - csv_file_path (str): Path to the CSV file.

    Raises:
    - FileNotFoundError: If the CSV file does not exist.
    """
    try:
        df = pd.read_csv(csv_file_path)
        num_columns = min(len(df.columns), 5)
        df = df.iloc[:, :num_columns]
        df.to_csv(csv_file_path, index=False)
    except FileNotFoundError as e:
        print(f"Error: {csv_file_path} not found. {e}")

def remove_duplicates(csv_file_path):
    """
    Removes duplicate rows and rows with 'lat' equal to 0.0 from the CSV file.

    Parameters:
    - csv_file_path (str): Path to the CSV file.

    Raises:
    - FileNotFoundError: If the CSV file does not exist.
    """
    try:
        df = pd.read_csv(csv_file_path)

        # Keep the first instance of each duplicate row and remove the rest
        df = df[~df.duplicated(subset=['lat', 'lon'], keep='first')]

        # Keep rows where 'lat' is not equal to 0.0
        df = df[df['lat'] != 0.0]
        df = df[df['lat'] != 0.1]

        df.to_csv(csv_file_path, index=False)
    except FileNotFoundError as e:
        print(f"Error: {csv_file_path} not found. {e}")

def sliding_window(speed):
    """
    Calculates severity using a sliding window approach.

    Parameters:
    - speed (list): List of speed values.

    Returns:
    - list: List of severity values.
    """
    try:
        window_size = 5
        if len(speed) <= window_size:
            return [0] * len(speed)

        severities = []
        for i in range(len(speed) - window_size + 1):
            window = speed[i:i+window_size]
            mean_diff = sum((window[j] - window[j - 1]) for j in range(1, len(window))) / (window_size - 1)
            severities.append(mean_diff)

        severities.extend([round(speed[-1] - speed[-2])] * (len(speed) - len(severities)))
        return severities
    except Exception as e:
        print(f"Error in sliding_window: {e}")

def classification(csv_file_path, destination_path):
    """
    Adds MovementClassification column to the CSV file based on severity values.

    Parameters:
    - csv_file_path (str): Path to the CSV file.
    - destination_path (str): Path to save the modified CSV file.

    Raises:
    - FileNotFoundError: If the CSV file does not exist.
    """
    try:
        df = pd.read_csv(csv_file_path)
        speed = df['speed'].tolist()
        severities = sliding_window(speed)
        movement_classifications = [classify_movement(c) for c in severities]
        df['MovementClassification'] = movement_classifications

        df.to_csv(destination_path, index=False)
    except FileNotFoundError as e:
        print(f"Error: {csv_file_path} not found. {e}")

def classify_movement(severity):
    """
    Classifies movement based on severity.

    Parameters:
    - severity (float): Severity value.

    Returns:
    - str: Movement classification.
    """
    try:
        if severity > 3.0:
            return "High Acceleration"
        elif severity > 0.4:
            return "Normal Acceleration"
        elif severity == 0:
            return "Steady Speed"
        elif severity < -3.0:
            return "High Braking"
        elif severity < 0.4:
            return "Normal Braking"
        else:
            return ""
    except Exception as e:
        print(f"Error in classify_movement: {e}")

def csv_handling(column_labels, csv_folder, classified_csv):
    """
    Processes CSV files in a folder.

    Parameters:
    - column_labels (list): List of column labels.
    - csv_folder (str): Folder containing CSV files.
    - classified_csv (str): Folder to save processed CSV files.

    Raises:
    - FileNotFoundError: If a CSV file does not exist.
    """
    try:
        os.makedirs(classified_csv, exist_ok=True)
        for filename in os.listdir(csv_folder):
            if filename.lower().endswith((".csv", ".CSV")):
                csv_file_path = os.path.join(csv_folder, filename)
                destination_path = os.path.join(classified_csv, filename)

                # Copy the original file to the destination folder
                shutil.copy2(csv_file_path, destination_path)
                # Perform modifications on the copied file
                data_cleaning(destination_path)
                data_classification(destination_path, column_labels)
                remove_duplicates(destination_path)
                # classification(destination_path, destination_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")

def start_watching_csv_folder(column_labels, csv_folder, classified_csv, rdf_folder, no_change_detected_time=5):
    """
    Monitors a CSV folder for changes and processes the files accordingly.

    Parameters:
    - column_labels (list): List of column labels.
    - csv_folder (str): Folder containing CSV files.
    - classified_csv (str): Folder to save processed CSV files.
    - rdf_folder (str): Folder to save RDF files.
    - no_change_detected_time (int): Timeout duration for checking changes.

    Raises:
    - KeyboardInterrupt: If the user interrupts the program.
    """
    try:
        event_handler = MyHandler(column_labels, classified_csv)
        observer = Observer()
        observer.schedule(event_handler, path=csv_folder, recursive=False)
        observer.start()

        try:
            print(f'Watching for changes in {csv_folder}. Press Ctrl+C to stop.')
            last_change_time = time.time()

            while True:
                current_time = time.time()

                # Check for changes every second
                if current_time - last_change_time > no_change_detected_time:
                    print(f'No changes detected for {no_change_detected_time} seconds. Stopping the observer.')
                    break

                # Sleep for 1 second
                time.sleep(1)

                # Check if any changes have occurred
                if event_handler.has_changes():
                    last_change_time = current_time
                    event_handler.clear_changes()

        except KeyboardInterrupt:
            pass

        for filename in os.listdir(csv_folder):
            if filename.lower().endswith((".csv", ".CSV")):
                csv_file_path = os.path.join(csv_folder, filename)
                destination_path = os.path.join(classified_csv, filename)
                classification(destination_path, destination_path)
                rdf_generation(classified_csv, rdf_folder)
                event_handler.cleanup_original(csv_file_path)

        observer.stop()
        observer.join()
    except Exception as e:
        print(f"Error in start_watching_csv_folder: {e}")

class MyHandler(FileSystemEventHandler):
    """
    Custom event handler for monitoring changes in CSV files.
    """
    def __init__(self, column_labels, classified_csv):
        self.column_labels = column_labels
        self.classified_csv = classified_csv
        self.changes_detected = False

    def on_modified(self, event):
        """
        Called when a file is modified.

        Parameters:
        - event (FileSystemEvent): File system event.
        """
        try:
            if event.is_directory:
                return

            if event.event_type == 'modified':
                print(f'File {event.src_path} has been modified. Processing...')

                # Process the modified file
                csv_file_path = event.src_path
                destination_path = os.path.join(self.classified_csv, os.path.basename(csv_file_path))

                # Perform modifications on the copied file
                shutil.copy2(csv_file_path, destination_path)
                data_cleaning(destination_path)
                data_classification(destination_path, self.column_labels)
                remove_duplicates(destination_path)
                # classification(destination_path, destination_path)

                self.changes_detected = True
        except Exception as e:
            print(f"Error in MyHandler.on_modified: {e}")

    def has_changes(self):
        """
        Checks if changes have been detected.

        Returns:
        - bool: True if changes detected, False otherwise.
        """
        return self.changes_detected

    def clear_changes(self):
        """
        Clears the changes flag.
        """
        self.changes_detected = False

    def cleanup_original(self, csv_file_path):
        """
        Cleans up the original CSV file after processing.

        Parameters:
        - csv_file_path (str): Path to the original CSV file.
        """
        try:
            os.remove(csv_file_path)
            print(f'Original file {csv_file_path} deleted.')
        except Exception as e:
            print(f'Error deleting original file {csv_file_path}: {e}')
