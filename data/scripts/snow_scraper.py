# https://avalanche.state.co.us/observations/field-reports
# https://avalanche.state.co.us/forecasts/help/observation-avalanche
# https://classic.avalanche.state.co.us/caic/obs_stns/zones.php?date=2023-02-28+16&stnlink=hourly&unit=e&flag=on&area=caic&span=6&caldate=2023-02-27
# https://classic.avalanche.state.co.us/caic/obs_stns/snow.php?date=2023-05-10+11&stnlink=hourly&unit=e&flag=on&area=caic&span=6

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

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
c_m = '05'
c_d = '11'

folder_path = os.getcwd()+'/WeatherStations'
if os.path.exists(folder_path) and os.path.isdir(folder_path):
  dirs = os.listdir(folder_path+"/no")
else:
  os.mkdir(folder_path)
  os.mkdir(folder_path+'/snow')
  dirs = []

cols = ['Station','Elev','Delta SWE since 5','Delta SWE 24h','Delta SWE 48h','Delta SWE 72h','Delta SWE 7d','Delta SWE 1 month','Delta HS since 5','Delta HS 24h','Delta HS 48h','Delta HS 72h','Delta HS 7d','Delta HS 1 month','Provider','Range']

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
                addr = "https://classic.avalanche.state.co.us/caic/obs_stns/snow.php?date={}-{}-{}+{}&stnlink=hourly&unit=e&flag=on&area=caic&span=6".format(t_y,t_m,t_d,time)
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
                                        if len(ls) == len(cols) - 1:
                                            ls.append(mtn_range)
                                            data.append(ls)
                                            ls = []
                                    except:
                                        pass
                data = pd.DataFrame(data,columns=cols,index=None)
                data.to_csv("WeatherStations/snow/{}_{}_{}_{}.csv".format(t_y,t_m,t_d,time),index=False)
                data = []
