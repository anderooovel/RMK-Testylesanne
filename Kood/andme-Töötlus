import csv
import pandas as pd
fail = open("C:\\Users\\PC\\Desktop\\andmed.csv", "r")

read = fail.readlines()

# 24657068-24660115 ja 59425287-59426727 (UUS Õige Zoo bussipeatuse koordinaadid)
# 24732689-24733727 ja 59436552-59437158 (Toomparki bussipeatuse koordinaaid)

ZooVäljumised = []
ZooTähistused = []
ToomparkTähistused = []
ToomparkVäljumised = []
lõppAndmed = []

# See for loop on mõeldud selleks et käia läbi kõik varasemalt kogutud andmed ning alles jätta vaid vajalikud andmed ehk need, mis on bussipeatuste Zoo ja Toomparki ümbruses.
for rida in read:
    rida = rida.strip('"')
    andmed = next(csv.reader([rida]))
    latitude = int(andmed[2])
    longitude = int(andmed[3])
    suund = int(andmed[5])
    tähistus = int(andmed[6] + andmed[8])
    if longitude > 59425287 and longitude < 59426727 and latitude > 24657068 and latitude < 24660115 and suund > 30 and suund < 120:
        if tähistus not in ZooTähistused:
            ZooVäljumised.append(rida)
            ZooTähistused.append(tähistus)
    if longitude > 59436552 and longitude < 59437158 and latitude > 24732689 and latitude < 24733727 and tähistus in ZooTähistused and tähistus not in ToomparkTähistused:
        ToomparkTähistused.append(tähistus)
        ToomparkVäljumised.append(rida)

# See for-loop on mõeldud selleks on kombineerida bussiajad ning arvutada nende vahe ja lisada need lõppAndmetesse.
for ZooBuss in ZooVäljumised:
    ZooBuss = ZooBuss.split(",")
    tähistusZoo = int(ZooBuss[6] + ZooBuss[8])
    for ToomparkBuss in ToomparkVäljumised:
        ToomparkBuss = ToomparkBuss.split(",")
        tähistusToompark = int(ToomparkBuss[6] + ToomparkBuss[8])
        if tähistusZoo == tähistusToompark:
            objekt = []
            kellaaegZoo = ZooBuss[9].split(" ")[1].split(":")
            kellaaegToompark = ToomparkBuss[9].split(" ")[1].split(":")
            vaheMinutid = int(kellaaegToompark[1]) - int(kellaaegZoo[1])
            vaheSekundid = int(kellaaegToompark[2]) - int(kellaaegZoo[2])
            if vaheMinutid < 0:
                vaheMinutid = 60 + vaheMinutid
            if vaheSekundid < 0:
                vaheSekundid = 60 + vaheSekundid
                vaheMinutid = vaheMinutid - 1
            if vaheSekundid < 10:
                vaheSekundid = "0" + str(vaheSekundid)
            if vaheMinutid < 10:
                vaheMinutid = "0" + str(vaheMinutid)
            #print(str(vaheMinutid) + "minutit ja " + str(vaheSekundid) + "sekundit")
            #print(ZooBuss)
            #print(ToomparkBuss)
            objekt.append(ZooBuss[9].split(" ")[1])
            objekt.append(ToomparkBuss[9].split(" ")[1])
            objekt.append("00:" + str(vaheMinutid) + ":" + str(vaheSekundid))
            objekt.append(ZooBuss[9].split(" ")[2].strip('"\n'))
            lõppAndmed.append(objekt)

# Salvestan lõppandmed .csv faili.
df = pd.DataFrame(lõppAndmed)
df.to_csv("C:\\Users\\PC\\Desktop\\lõppandmed.csv", index=False, encoding="utf-8", mode='a', header=False)

        
