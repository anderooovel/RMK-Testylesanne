import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime
import pytz

# Set Estonian timezone.
ESTONIAN_TIMEZONE = pytz.timezone('Europe/Tallinn')
URL = "https://transport.tallinn.ee/gps.txt"


# Loop through all URLs (currently 620 iterations).
# Chose 620 iterations because 1 loop takes about 15 seconds and so 620 is enough for like 620x15 ~ 2,5hrs.
for iteration in range(0, 620):
    records = []  # Store all valid bus data for this load.
    # Since the URL doesn't provide timestamp, get current time manually.
    estonian_time = datetime.now(ESTONIAN_TIMEZONE).strftime('%H:%M:%S')
    current_date = datetime.now(ESTONIAN_TIMEZONE).strftime('%d.%m.%y')

    # Probably could take service and driver out of the loop.
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(URL)  # Open URL
    time.sleep(10)  # Wait for page to load and refresh data (every 10 seconds).

    # Data is inside a <pre> tag on the page.
    pre_text = driver.find_element(By.TAG_NAME, "pre").text
    lines = pre_text.splitlines()  # Split text into lines

    for line in lines:
        # Check if line starts with unique code for bus number 8.
        # '2' indicates vehicle type, '8' is the bus number
        if line.startswith("2,8,"):
            if line not in records:
                print(estonian_time)
                # Append bus info along with timestamp and current date.
                records.append(line + " " + estonian_time + " " + current_date)
                print("Added!")

    # Convert records to a DataFrame and append to CSV file.
    df = pd.DataFrame(records)
    df.to_csv(
        "C:\\Users\\PC\\Desktop\\andmed.csv",
        index=False,
        encoding="utf-8",
        mode='a',
        header=False,
    )

    # Close the browser.
    driver.quit()
