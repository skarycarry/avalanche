import pandas as pd
import json
import os
import re
import numpy as np

weather = os.listdir('data/WeatherStations')
danger = pd.read_csv('data/ratings_comb.csv')

times = 

for i,r in danger.iterrows():
    yr = r['Year']
    mo = r['Month']
    dy = r['Day']
    time = r['Time']
    