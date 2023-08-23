import pandas as pd
import requests

def colo(addr):
    page = requests.get(addr)
    jsn = page.json()
    data = []
    for j in jsn:
        try:
            dr = j['dangerRatings']['days'][0]
            lst = [j['title'],j['avalancheSummary']['days'][0]['content'],dr['alp'],dr['tln'],dr['btl']]
            for d in j['avalancheProblems']['days']:
                for t in d:
                    data.append(lst + [t['type'],t['aspectElevations'],t['likelihood'],t['expectedSize']])
                    print(lst + [t['type'],t['aspectElevations'],t['likelihood'],t['expectedSize']])
        except:
            continue

    df = pd.DataFrame(data,columns=['title','avalancheSummary','alp','tln','btl','type','aspectElevations','likelihood','expectedSize'])
    return df