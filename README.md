# RMK Internship Challenge 2025

This project is made for the RMK data team internship test challenge.  
The goal is to find out how likely it is that Rita will be late to her 9:05 AM meeting, depending on when she leaves home.

Rita takes Tallinn city bus number 8 from the Zoo stop to Toompark.  
She needs:
- 5 minutes to walk from home to the Zoo stop
- 4 minutes to walk from Toompark to her meeting room

So, the bus needs to arrive at Toompark no later than 09:01, or she’ll be late.

---

## What I did

- Collected real-time data about bus number 8 (from "https://transport.tallinn.ee/gps.txt")
- Logged when each bus left Zoo and arrived at Toompark
- Calculated how long the ride took
- Simulated different times when Rita might leave home (08:00 to 08:59)
- For each time, checked if there’s a bus she can take to arrive at Toompark before 09:01
- Counted how often that would happen to get the probability of being late

Right now the data is from eight days, but if I collect data for like a month then the results will be more accurate.

![Lateness Probability Plot](plots/lateness_plot.png)

---

## Project files

- 'andmed/raw_data.csv' – all the raw data collected over 8 days
- 'andmed/finished_data.csv' – processed data used in calculating probabilities
- 'Kood/data_collection.py' – script for collecting bus data
- 'Kood/process_bus_data.py' – script for processing the raw data
- 'Kood/lateness_simulation.py' – calculation and plotting
- 'plots/lateness_plot.png' – result graph
- 'requirements.txt' – required Python packages

---

## How to run

1. Install packages:
pip install -r requirements.txt

2. Prepare the data:
Download finished_data.csv
Place it somewhere accessible
Update the INPUT_PATH variable in lateness_simulation.py to point to the correct location

3. Run the simulation:
python src/lateness_simulation.py

---

## Data source

Live bus location data from Tallinn open data:  
https://avaandmed.eesti.ee/datasets/uhistranspordivahendite-asukohad-reaalajas

---

## What could be improved

- Collect data for more days to make the probabilities more realistic
- Investigate the possible delay between the actual bus location and when it's updated on the website. There may be a small buffer or lag (maybe 30–60 seconds), so adjusting the recorded times slightly earlier might improve accuracy

---

Made by Andero Öövel for RMK internship challenge 2025
