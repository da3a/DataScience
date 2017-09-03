# https://coinmarketcap-nexuist.rhcloud.com/api/ltc
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
import pandas as pd
from pandas.io.json import json_normalize
import numpy
import sys
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.ticker as ticker
from matplotlib import dates
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
print(dfNew.iloc[0,0])

#print(dfNew.iloc[0,1])
newTimeStamp = dfNew.index[0]

try:
    df = pd.read_pickle('C:\Projects\DataScience\Crypto\\ltc.pickle')
    print('read pickle:', df)
    print('dfindex =',df.index[-1])
    print('newtimestamp', newTimeStamp)
    if (df.index[-1] != newTimeStamp):
        print('new value!')
        df = df.append(dfNew)
    else:
        print('value not changed since last call')
except Exception as e:
    print('woops, an error occurred',e)
    df = dfNew
finally:
    df.to_pickle('ltc.pickle')


style.use('ggplot')

df.describe()
#df.plot()

plt.plot(df.index.to_pydatetimes(), df['Price.gbp'])
date_fmt = '%H:%M:%S'
formatter = dates.DateFormatter(date_fmt)
#ax = df['price.gbp'].plot()
#ax.xaxis.set_major_formatter(formatter)


# ax.xaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
#df.plot()

plt.xlabel('time')
plt.ylabel('price')
plt.show()
