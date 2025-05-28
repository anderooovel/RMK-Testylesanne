import csv
import pandas as pd

INPUT_PATH = "C:\\Users\\PC\\Desktop\\andmed.csv"
OUTPUT_PATH = "C:\\Users\\PC\\Desktop\\lõppandmed.csv"

# Open the file that contains the data we got from data_collection.py
with open(INPUT_PATH, "r") as infile:
    lines = infile.readlines()

# Coordinate boundaries for Zoo and Toompark bus stops
ZOO_LAT_MIN = 24657068
ZOO_LAT_MAX = 24660115
ZOO_LON_MIN = 59425287
ZOO_LON_MAX = 59426727

TOOMPARK_LAT_MIN = 24732689
TOOMPARK_LAT_MAX = 24733727
TOOMPARK_LON_MIN = 59436552
TOOMPARK_LON_MAX = 59437158

# Make lists to memorize necessary data.
zoo_arrivals = []
zoo_IDs = []
toompark_arrivals = []
toompark_IDs = []
finished_data = []

# Go through all the lines in the file.
for line in lines:
    # Clean up the line and extract useful information.
    line = line.strip('"')
    data = next(csv.reader([line]))
    latitude = int(data[2])
    longitude = int(data[3])
    degrees = int(data[5]) # Which direction the bus is facing 0-359.
    bus_ID = int(data[6] + data[8]) # This is unique for every bus and helps identify if the same bus has already been in the bus stop.

    # Check if the bus data is exactly in zoo bus stop and if the bus_ID has already been there.
    if (
        ZOO_LON_MIN < longitude < ZOO_LON_MAX and
        ZOO_LAT_MIN < latitude < ZOO_LAT_MAX and
        30 < degrees < 120 and
        bus_ID not in zoo_IDs
    ):
        zoo_arrivals.append(line)
        zoo_IDs.append(bus_ID)
    
    # Check if the bus data is exactly in toompark bus stop and if the bus_ID has already been there.
    if (
        TOOMPARK_LON_MIN < longitude < TOOMPARK_LON_MAX and
        TOOMPARK_LAT_MIN < latitude < TOOMPARK_LAT_MAX and
        bus_ID in zoo_IDs and
        bus_ID not in toompark_IDs
    ):
        toompark_IDs.append(bus_ID)
        toompark_arrivals.append(line)

# Go through all the fetched times from zoo bus stop and pair them with the times from toompark bus stop.
for zoo_bus in zoo_arrivals:
    # Clean up the data and store useful information.
    zoo_bus = zoo_bus.split(",")
    zoo_bus_ID = int(zoo_bus[6] + zoo_bus[8])

    # Go through all the toompark bus stop times and find the ID that matches the zoo ID.
    for toompark_bus in toompark_arrivals:
        # Clean up the data and store useful information.
        toompark_bus = toompark_bus.split(",")
        toompark_bus_ID = int(toompark_bus[6] + toompark_bus[8])

        # If the IDs match then clean the data and add it to finished_data.
        if zoo_bus_ID == toompark_bus_ID:
            row = [] # Placeholder to store the data that we add to finished_data.
            zoo_time = zoo_bus[9].split(" ")[1].split(":")
            toompark_time = toompark_bus[9].split(" ")[1].split(":")
            difference_minutes = int(toompark_time[1]) - int(zoo_time[1])
            difference_seconds = int(toompark_time[2]) - int(zoo_time[2])

            # Change the difference times to be correct.
            if difference_minutes < 0:
                difference_minutes += 60
            if difference_seconds < 0:
                difference_seconds += 60
                difference_minutes -= 1
            if difference_seconds < 10:
                difference_seconds = "0" + str(difference_seconds)
            if difference_minutes < 10:
                difference_minutes = "0" + str(difference_minutes)
            
            # Add all the data to row and then to finished_data.
            row.append(zoo_bus[9].split(" ")[1])
            row.append(toompark_bus[9].split(" ")[1])
            row.append("00:" + str(difference_minutes) + ":" + str(difference_seconds))
            row.append(zoo_bus[9].split(" ")[2].strip('"\n'))

            finished_data.append(row)

# Convert records to a DataFrame and append to CSV file.
df = pd.DataFrame(finished_data)
df.to_csv(
    OUTPUT_PATH,
    index=False, 
    encoding="utf-8", 
    mode='a', 
    header=False,
)

        
