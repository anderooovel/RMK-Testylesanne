from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

INPUT_PATH = "C:\\Users\\PC\\Desktop\\lõppandmed.csv"
SIMULATIONS = 10000

# Open the processed data file
with open(INPUT_PATH, "r") as file:
    lines = file.readlines()[1:]

# Time from home to zoo stop
home_to_stop = 300

# Time from Toompark stop to meeting
stop_to_meeting = 240

# Time of the meeting
meeting_time = "09:05:00"
meeting_helper_time = datetime.strptime(meeting_time, "%H:%M:%S")
meeting_time_seconds = (
    meeting_helper_time.hour * 3600 +
    meeting_helper_time.minute * 60 +
    meeting_helper_time.second
)

# Lists to store zoo stop times and durations for each weekday
zoo_times = [[] for _ in range(8)]
elapsed_times = [[] for _ in range(8)]
helper_index = 0

# Go through all the data and extract what is necessary
for line in lines:
    line = line.strip()

    if helper_index == 8:
        helper_index = 0

    if line == "puudu":
        helper_index = helper_index + 1
        continue

    line = line.split(",")

    zoo_time = line[0]
    zoo_helper_time = datetime.strptime(zoo_time, "%H:%M:%S")
    zoo_time_seconds = (
        zoo_helper_time.hour * 3600 +
        zoo_helper_time.minute * 60 +
        zoo_helper_time.second
    )
    zoo_times[helper_index].append(zoo_time_seconds)

    elapsed_time = line[2]
    elapsed_helper_time = datetime.strptime(elapsed_time, "%H:%M:%S")
    elapsed_time_seconds = (
        elapsed_helper_time.hour * 3600 +
        elapsed_helper_time.minute * 60 +
        elapsed_helper_time.second
    )
    elapsed_times[helper_index].append(elapsed_time_seconds)

    helper_index = helper_index + 1

# Simulation function
def simulate(home_departure, simulations=SIMULATIONS):
    home_helper_time = datetime.strptime(home_departure, "%H:%M:%S")
    home_departure_seconds = (
        home_helper_time.hour * 3600 +
        home_helper_time.minute * 60 +
        home_helper_time.second
    )

    late_count = 0
    for i in range(simulations):
        arrival_at_zoo = home_departure_seconds + home_to_stop

        correct_bus_time = 0
        helper = 0
        for zoo_day in zoo_times:
            bus_time = np.random.choice(zoo_day)
            if bus_time > arrival_at_zoo:
                correct_bus_time = bus_time
                helper = zoo_times.index(zoo_day)
                break

        bus_duration = np.random.choice(elapsed_times[helper])
        arrival_at_toompark = correct_bus_time + bus_duration
        final_arrival = arrival_at_toompark + stop_to_meeting

        if final_arrival > meeting_time_seconds:
            late_count += 1

    return late_count / simulations

home_departures = []
departures = []
probabilities = []

for i in range(0, 60):
    if i < 10:
        minute = "0" + str(i)
    else:
        minute = str(i)
    for j in range(0, 6):
        home_departures.append("08:" + minute + ":" + str(j) + "0")

last_p = 0
for t in home_departures:
    if last_p != 1:
        p = simulate(t)
    else:
        p = 1
    last_p = p
    rounded = round(p * 100, 1)
    print("Departure " + t + " -> probability of being late: " + str(rounded) + "%")
    departures.append(datetime.strptime("2025-05-23 " + t, "%Y-%m-%d %H:%M:%S"))
    probabilities.append(p)

plt.figure(figsize=(10, 5))
plt.plot(departures, probabilities)
plt.title("Probability of being late depending on home departure time")
plt.xlabel("Departure time")
plt.ylabel("Probability (0–1)")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
