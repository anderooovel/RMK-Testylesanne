from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


fail = open("C:\\Users\\PC\\Desktop\\lõppandmed.csv", "r")
read = fail.readlines()[1:]

kodustBussipeatusesse = 300
bussipeatusestKohtumisele = 240
kohtumiseAeg = "09:05:00"
kohtumiseAbiAeg = datetime.strptime(kohtumiseAeg, "%H:%M:%S")
kohtumiseAegSekundites = kohtumiseAbiAeg.hour * 3600 + kohtumiseAbiAeg.minute * 60 + kohtumiseAbiAeg.second

zooAjad = [[] for _ in range(8)]
kulunudAjad = [[] for _ in range(8)]
abiMuutuja = 0


for rida in read:
    rida = rida.strip()

    if abiMuutuja == 8:
        abiMuutuja = 0

    if rida == "puudu":
        abiMuutuja = abiMuutuja + 1
        continue
    
    rida = rida.split(",")

    zooAeg = rida[0]
    zooAbiAeg = datetime.strptime(zooAeg, "%H:%M:%S")
    zooAegSekundites = zooAbiAeg.hour * 3600 + zooAbiAeg.minute * 60 + zooAbiAeg.second
    zooAjad[abiMuutuja].append(zooAegSekundites)

    kulunudAeg = rida[2]
    kulunudAbiAeg = datetime.strptime(kulunudAeg, "%H:%M:%S")
    kulunudAegSekundites = kulunudAbiAeg.hour * 3600 + kulunudAbiAeg.minute * 60 + kulunudAbiAeg.second
    kulunudAjad[abiMuutuja].append(kulunudAegSekundites)

    abiMuutuja = abiMuutuja + 1

def simuleeri(kodustVäljumine, simulatsioone=4000):

    kodustVäljumineAbi = datetime.strptime(kodustVäljumine, "%H:%M:%S")
    kodustVäljumineSekundites = kodustVäljumineAbi.hour * 3600 + kodustVäljumineAbi.minute * 60 + kodustVäljumineAbi.second

    hilinemisi = 0
    for i in range(simulatsioone):
        zooJõudmine = kodustVäljumineSekundites + kodustBussipeatusesse

        õigeBussiaeg = 0
        abiline = 0
        for zooAeg in zooAjad:
            bussiaeg = np.random.choice(zooAeg)
            if bussiaeg > zooJõudmine:
                õigeBussiaeg = bussiaeg
                abiline = zooAjad.index(zooAeg)
                break
        
        bussisõiduKestvus = np.random.choice(kulunudAjad[abiline])

        toomparkiJõudmine = õigeBussiaeg + bussisõiduKestvus

        lõppAeg = toomparkiJõudmine + bussipeatusestKohtumisele

        if lõppAeg > kohtumiseAegSekundites:
            hilinemisi += 1


    return hilinemisi / simulatsioone

kodust = []
väljumised = []
tõenäosused = []

for i in range (0,60):
    if i < 10:
        number = "0" + str(i)
    else:
        number = str(i)
    for j in range(0,6):
        kodust.append("08:" + number + ":" + str(j) + "0")

for t in kodust:
    p = simuleeri(t)
    ümardatud = round(p * 100, 1)
    print(f"Väljumine {t} → hilinemise tõenäosus: {ümardatud}%")
    väljumised.append(datetime.strptime("2025-05-23 " + t, "%Y-%m-%d %H:%M:%S"))
    tõenäosused.append(p)

plt.figure(figsize=(10, 5))
plt.plot(väljumised, tõenäosused)
plt.title("Hilinemise tõenäosus vastavalt kodust väljumise ajale")
plt.xlabel("Väljumise aeg")
plt.ylabel("Tõenäosus (0–1)")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()







