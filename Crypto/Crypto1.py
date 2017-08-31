# https://coinmarketcap-nexuist.rhcloud.com/api/ltc
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
import pandas as pd
from pandas.io.json import json_normalize
import numpy

baseUrl = 'https://coinmarketcap-nexuist.rhcloud.com/api/{}'


def getCurrentPrice(currency):
    url = baseUrl.format(currency)
    print('calling:' + url)
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url, verify=False)
    return json.loads(response.text)['price']['gbp']

def getCurrentData(currency):
    url = baseUrl.format(currency)
    print('calling:' + url)
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url, verify=False)
    return response.text

#print(getCurrentPrice('ltc'))
data = getCurrentData('ltc')

doc = json.loads(data)

dfNew = json_normalize(doc)

#print(df.head(1))

dfNew = dfNew[['timestamp','price.gbp', 'change']]
dfNew.set_index('timestamp',inplace=True)
print(dfNew)
try:
    df = pd.read_pickle('ltc.pickle')
    #print('read pickle:', df)
    #print('timestamp is: ',dfNew['timestamp'])
    if (1  in df[0]) :
        df = df.append(dfNew)
except Exception as e:
    print('woops, an error occurred',e)
    df = dfNew

#print(df)
df.to_pickle('ltc.pickle')


# df = pd.read_json(data)
# df.set_index('timestamp',inplace=True)
# print(df.head(1))


# df = df.filter(like='gbp',axis=0)
# print(df.head(1))
# print(df.index)









