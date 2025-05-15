import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pytz


eesti_timezone = pytz.timezone('Europe/Tallinn')
url  = "https://transport.tallinn.ee/gps.txt"


# Siin on suur range, sest siis see töötab ja kogub andmeid üle kahe tunni
for i in range(0,720):
    andmed = []
    eesti_kellaaeg = datetime.now(eesti_timezone).strftime('%H:%M:%S')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    time.sleep(10)

    pre_text = driver.find_element(By.TAG_NAME, "pre").text
    valmis = pre_text.splitlines()
    for rida in valmis:
        if rida.startswith("2,8,"):
            if rida not in andmed:
                print(eesti_kellaaeg)
                andmed.append(rida + " " + eesti_kellaaeg + " " + "15.05.25")
                print("Lisan")

    # Salvestame vajalikud andmed .csv faili
    df = pd.DataFrame(andmed)
    df.to_csv("C:\\Users\\PC\\Desktop\\andmed.csv", index=False, encoding="utf-8", mode='a', header=False)
    driver.quit()

