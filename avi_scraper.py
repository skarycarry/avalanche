import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import json
#from colo import colo
#from gall import gall
#from utah import utah
#from parse import parse

myfile = open("sites.txt", "r")
sites = myfile.read().split("\n")
myfile.close()

lists = []
for s in sites:
    myfile = open("data/DangerSites/{}.txt".format(s), "r")
    lists.append([s] + myfile.read().split("\n"))
    myfile.close()

#special_parsers = {"Colorado": colo,"Gallatin": gall,"Utah": utah}
uniques = {"Flathead": 125000}

year_range = [2018,2020]
years = range(year_range[0],year_range[1]+1)
months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
days = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
days_per_month = [31,28,31,30,31,30,31,31,30,31,30,31]

files = os.listdir("data/AviDanger") + os.listdir("data/AviDanger/no")

print(files)

for i in range(85000,125000):
    if i%100 == 0:
        print(i)
    if '{}.json'.format(i) in files:
        continue
    addr = "https://api.avalanche.org/v2/public/product/{}".format(i)
    try:
        page = requests.get(addr)
        jsn = page.json()
    except:
        print("Error: {}".format(i))
        dic = {"id": i, "bottom_line": None}
        with open("data/AviDanger/no/{}.json".format(i),"w") as f:
            json.dump(dic, f)
        continue
    
    if jsn['bottom_line'] == None:
        dic = {"id": i, "bottom_line": None}
        with open("data/AviDanger/no/{}.json".format(i),"w") as f:
            json.dump(dic, f)
        continue

    with open("data/AviDanger/{}.json".format(i),"w") as f:
        json.dump(jsn, f)