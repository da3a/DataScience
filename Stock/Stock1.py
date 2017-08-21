import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web 

style.use('ggplot')

start = dt.datetime(2017,1,1)
end = dt.datetime(2017,5,21)

df = web.DataReader('MSFT','google',start,end)

print(df.head())

# df['Close'].plot()
# plt.show()

df['20ma'] = df['Close'].rolling(window=20,min_periods=0).mean()

print(df.head())

ax1 = plt.subplot2grid((6,1),(0,0),rowspan=5,colspan=1)
ax2 = plt.subplot2grid((6,1),(5,0),rowspan=1,colspan=1,sharex=ax1)
ax1.plot(df.index,df['Close'])
ax1.plot(df.index,df['20ma'])
ax2.bar(df.index,df['Volume'])

plt.show()
