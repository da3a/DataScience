#https://medium.com/towards-data-science/simple-and-multiple-linear-regression-in-python-c928425168f9
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
from sklearn import linear_model

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

print("df.index is", df.index)

X = df

y = df['price.gbp']
print('value of y is: ',y)
df['Date'] = pd.to_datetime(df.index[0], unit='s')

newdf = pd.DataFrame(df['price.gbp'], index=df['Date'])

newdf.plot()
plt.show()
sys.exit(0)
lm = linear_model.LinearRegression()
model = lm.fit(X,y)

lm.score(X,y)

predictions = lm.predict(X)
print('predictions',predictions[0:5])

df['Date'] = pd.to_datetime(df.index[0], unit='s')

plt.scatter(df.index, df['price.gbp'],color='black')
plt.plot(df.index, predictions, color='blue', linewidth=3)

plt.xticks(())
plt.yticks(())
plt.show()

#print(lm.score(X,y))
#print(lm.coef_)
#print(lm.intercept_)



