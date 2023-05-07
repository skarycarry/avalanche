# https://avalanche.state.co.us/observations/field-reports
# https://avalanche.state.co.us/forecasts/help/observation-avalanche
# https://classic.avalanche.state.co.us/caic/obs_stns/zones.php?date=2023-02-28+16&stnlink=hourly&unit=e&flag=on&area=caic&span=6&caldate=2023-02-27

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

c_y = "2023"
c_m = "02"
c_d = "28"
time = "16"
t_y = "2023"
t_m = "02"
t_d = "27"

width = 18

mtn_range = ""

data = []

provider = ["CDOT","APRSWXNET","RAWS","HADS","SNOTEL","USGS","RMRS","CAIC","METAR","MesoWest","PWS","VailResort","A-BasinSA","ColoMtnCol","MonarchSA","AspenSkiCo","IrwinGuide","CLOUDSEED","TELLURIDE","MTNSTUDIES","CSAS"]

years = [2020,2021,2022]
months = ['01','02','03','04','05','06','07','08','09','10','11','12']
days = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
days_per_month = [31,28,31,30,31,30,31,31,30,31,30,31]
times = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']

c_y = 2023
c_m = '03'
c_d = '01'

dirs = os.listdir("data/WeatherStations")

cols = ['Station','Elev','Temp','MaxTemp','MinTemp','DewPoint','RH','Spd','Dir','Gst','Pcp1','Pcp24','PcpAc','Sno24','SWE24','SnoHt','SWE','Provider','Range']

for y in years:
    t_y = str(y)
    print(t_y)
    for m in range(len(months)):
        t_m = months[m]
        print(t_m)
        for d in range(days_per_month[m]):
            t_d = days[d]
            for time in times:
                if "{}_{}_{}_{}.csv".format(t_y,t_m,t_d,time) in dirs:
                    continue
                addr = "https://classic.avalanche.state.co.us/caic/obs_stns/zones.php?date={}-{}-{}+{}&stnlink=hourly&unit=e&flag=on&area=caic&span=6&caldate={}-{}-{}".format(c_y,c_m,c_d,time,t_y,t_m,t_d)
                page = requests.get(addr)
                soup = BeautifulSoup(page.content, 'html.parser')
                f = soup.find_all('p')
                for p in f:
                    for t in p:
                        ls = []
                        try:
                            if t.h4.text != "Station":
                                mtn_range = t.h4.text
                        except:
                            for th in t:
                                try:
                                    if th.th.text != "Station":
                                        mtn_range = th.th.text
                                    continue
                                except:
                                    pass
                                
                                for td in th:
                                    try:
                                        txt = td.text
                                        if txt != "" and txt != " " and '\n' not in txt:
                                            ls.append(txt)
                                        if len(ls) == 18:
                                            ls.append(mtn_range)
                                            data.append(ls)
                                            ls = []
                                    except:
                                        pass
                data = pd.DataFrame(data,columns=cols,index=None)
                data.to_csv("data/WeatherStations/{}_{}_{}_{}.csv".format(t_y,t_m,t_d,time),index=False)
                data = []