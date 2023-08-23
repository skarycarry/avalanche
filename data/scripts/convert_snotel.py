import csv

# Open the input file for reading
with open('../inputs/snotel.txt', 'r') as infile:

    # Create a CSV writer for the output file
    with open('../inputs/snotel.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)

        # Initialize a flag to track whether we've found the column names yet
        found_column_names = False

        # Loop over the lines in the input file
        for line in infile:

            # Ignore lines that start with '#'
            if line.startswith('#'):
                continue

            # Split the line into fields
            fields = line.strip().split(',')

            # If this is the first line after any comments, treat it as the column names
            if not found_column_names:
                writer.writerow(fields)
                found_column_names = True

            # Otherwise, write the fields to the output file as a new row
            else:
                writer.writerow(fields)

