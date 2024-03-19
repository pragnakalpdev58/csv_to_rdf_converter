from imports import *

# Function to read data from the original CSV file
def read_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header
        data = [row for row in reader]  # Read the remaining rows
    return header, data

# Function to write data to the target CSV file
def write_csv(file_path, header, rows):
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Check if the file is empty
            writer.writerow(header)
        for row in rows:
            writer.writerow(row)

# Main function
def main():
    original_file_path = 'csv_randomfiles/0jJ4OteJ.csv'
    target_file_path = 'csv/test.csv'

    header, data = read_csv(original_file_path)

    entries_to_write = []  # List to store entries before writing

    for row in data:
        entries_to_write.append(row)

        if len(entries_to_write) == 1000:  # Check if 5 entries are accumulated
            write_csv(target_file_path, header, entries_to_write)
            entries_to_write = []  # Reset the list
            time.sleep(1)  # Insert one batch at a time with a 1-second interval

    # Write any remaining entries (less than 5) at the end
    if entries_to_write:
        write_csv(target_file_path, header, entries_to_write)

if __name__ == "__main__":
    main()