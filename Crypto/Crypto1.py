# https://coinmarketcap-nexuist.rhcloud.com/api/ltc
import requests
import json
import pandas as pd
import numpy
import sys
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pandas.io.json import json_normalize
from matplotlib import style
from matplotlib import dates

baseUrl = 'https://coinmarketcap-nexuist.rhcloud.com/api/{}'
currencySymbol = 'ltc'
pickleFile = 'C:/Projects/DataScience/Crypto/' + currencySymbol + '.pickle'

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
data = getCurrentData(currencySymbol)
doc = json.loads(data)
dfNew = json_normalize(doc)

dfNew = dfNew[['timestamp','price.gbp', 'change']]
dfNew.set_index('timestamp',inplace=True)
#print(dfNew.iloc[0,0])
#print(dfNew.iloc[0,1])
newTimeStamp = dfNew.index[0]
#print('to datetime: ',newTimeStamp)
#print('to datetime: ',pd.to_datetime([newTimeStamp],unit='s')
try:
    df = pd.read_pickle(pickleFile)
    print(df)
    if (df.index[-1] != newTimeStamp): # compare last value
        print('new value!')
        df = df.append(dfNew)
    else:
        print('value not changed since last call')
except Exception as e:
    print('woops, an error occurred',e)
    df = dfNew
finally:
    df.to_pickle(pickleFile)

style.use('ggplot')
df.describe()

df['Date'] = pd.to_datetime(df.index[0], unit='s')
print(df['Date'])

print(df.head(10))
#df.plot(x="Date",y="price.gbp")
df.plot()

#plt.plot(df.index.to_pydatetimes(), df['Price.gbp'])
date_fmt = '%H:%M:%S'
formatter = dates.DateFormatter(date_fmt)
#ax = df['price.gbp'].plot()
#ax.xaxis.set_major_formatter(formatter)


# ax.xaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
#df.plot()

plt.xlabel('time')
plt.ylabel('price')
plt.show()
