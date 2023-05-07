import pandas as pd
import json
import os
import re
import numpy as np

include_text = False
separate = False

files = os.listdir("data/AviDanger")
files.remove("no")

data = []
types = {}

multi = []

CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

if separate:

    for f in files:
        ls = []
        with open("data/AviDanger/{}".format(f)) as json_file:
            jsn = json.load(json_file)
            time = jsn["published_time"]
            year = time[0:4]
            month = time[5:7]
            day = time[8:10]
            for p in jsn["forecast_avalanche_problems"]:
                ls = []
                ls.append(year)
                ls.append(month)
                ls.append(day)
                if include_text:
                    ls.append(re.sub(CLEANR,'',jsn["bottom_line"]))
                ls.append(p["avalanche_problem_id"])
                ls.append(p["rank"])
                ls.append(p["likelihood"])
                ls.append(p["location"])
                ls.append(p["size"])
                
                if include_text:
                    if p["discussion"] == None:
                        ls.append("")
                    else:
                        ls.append(re.sub(CLEANR,'',p["discussion"]))
                if p["name"] not in types.keys():
                    types[p["name"]] = p["problem_description"]
                data.append(ls)
    data = pd.DataFrame(data)
    data = data.sort_values([0,1,2])
    if include_text:
        data.to_csv("data/ratings_data_text.csv",index=None,header=['Year','Month','Day','Bottom Line','Problem ID','Rank','Likelihood','Location','Size','Discussion'])
    else:
        data.to_csv("data/ratings_data_wo.csv",index=None,header=['Year','Month','Day','Problem ID','Rank','Likelihood','Location','Size'])

else:
    data = np.empty((len(files),52),dtype=object)
    data.fill(np.NaN)
    for i,f in enumerate(files):
        with open("data/AviDanger/{}".format(f)) as json_file:
            jsn = json.load(json_file)
            for j,z in enumerate(jsn["forecast_zone"]):
                time = jsn["published_time"]
                data[i,0] = time[0:4]
                data[i,1] = time[5:7]
                data[i,2] = time[8:10]
                data[i,3] = time[11:13]
                data[i,4] = z["name"]
                data[i,5] = z["id"]
                data[i,6] = z["zone_id"]
                for p in jsn["forecast_avalanche_problems"]:
                    id = p["avalanche_problem_id"]
                    val = (id - 1) * 5 + 7
                    data[i,val] = id
                    data[i,val+1] = p["rank"]
                    data[i,val+2] = p["likelihood"]
                    data[i,val+3] = p["location"]
                    data[i,val+4] = p["size"]

    print(sorted(multi))
    data = pd.DataFrame(data)
    data = data.sort_values([0,1,2])
    sup_cols = ["Problem ID","Rank","Likelihood","Location","Size"] * 9
    data.to_csv("data/ratings_comb.csv",index=False,header=['Year','Month','Day','Time','Mountain(s)','ID','Zone ID']+sup_cols)
