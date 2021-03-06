import sys
import bs4 as bs
import pickle
import requests
import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn import datasets, linear_model

def scrape_tickers(pageNo):
    print("scrape_tickers")
    response = requests.get('http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/summary/summary-indices-constituents.html?index=ASX&page={}'.format(pageNo))
    soup = bs.BeautifulSoup(response.text,'lxml')
    table = soup.find('table',{'class','table_dati'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
    return tickers

def save_ftse_tickers():
    print("save_ftse_tickers")
    tickers = []
    cnt = 0
    pageTotal = 32
    while cnt < pageTotal:
        cnt = cnt+1
        pagedTickers = scrape_tickers(cnt)
        tickers.extend(pagedTickers)
    
    with open('ftse.pickle','wb') as f:
        pickle.dump(tickers,f)
    return tickers

def get_ftse_tickers(reload_tickers=False):
    print("get_ftse_tickers")
    if reload_tickers:
        tickers = save_ftse_tickers()
    else:
        with open('ftse.pickle','rb') as f:
            tickers = pickle.load(f)
    return tickers

def get_ticker_data_from_web(ticker, startTime, endTime):
    try:
        df = web.DataReader(ticker,'google', startTime, endTime)
        df.to_csv('ftse/{}.csv'.format(ticker))
        return df
    except:
        return pd.DataFrame({'empty' : []})

def get_ticker_data(ticker,startTime,endTime):
    print('get_ticker_data {} {} {}'.format(ticker, startTime, endTime))
    if not os.path.exists('ftse'):
        os.makedirs('ftse')
    try:
        return readFile('ftse/{}.csv'.format(ticker))
    except:
        print('ticker file not found will reload')
        df = get_ticker_data_from_web(ticker, startTime, endTime)
        if not df.empty:
            return readFile('ftse/{}.csv'.format(ticker))
        else:
            return df

def readFile(file_name):
    print('readFile {}'.format(file_name))
    data = pd.read_csv(file_name,sep=',',usecols=[0,4],names=['Date','Price'],header=1)
    returns = np.array(data['Price'][1:],np.float)/np.array(data['Price'][:-1],np.float)-1
    data['Returns'] = np.append(returns,np.nan)
    data.index = data['Date']
    return data

#def getCoef(data):
# get_ftse_tickers(reload_tickers=True)
# sys.exit(0)

startTime = dt.datetime(2017,4,1)
endTime = dt.datetime(2017,10,1)
tickers = get_ftse_tickers(reload_tickers=False)

# for ticker in tickers:
#     print('getting ticker data for:{}'.format(ticker))
#     get_ticker_data(ticker, startTime, endTime)

# sys.exit(0)


# for ticker in tickers:
#     print('getting ticker data for:{}'.format(ticker))
#     get_ticker_data(ticker, startTime, endTime)

#sys.exit(0)

ftsedata = pd.read_csv('ftse/^FTSE_1.csv',sep=',',usecols=[0,5],names=['Date','Price'],header=1)
ftsereturns = np.array(ftsedata['Price'][1:],np.float)/np.array(ftsedata['Price'][:-1],np.float)-1
ftsedata['Returns'] = np.append(ftsereturns,np.nan)
ftsedata.index = ftsedata['Date']
#print(ftse.describe())

def plot_figure(tickers):
        fig, ax = plt.subplots(nrows=5, ncols=5)
        fig.tight_layout()
        ctr = 1
        for ticker in tickers:
            print('ticker:{}'.format(ticker))
            df = get_ticker_data(ticker, startTime, endTime)
            if df.empty:
                continue
            modeldata = pd.merge(ftsedata,df,how='inner',on=['Date'])
            print(modeldata)
            year_xData = modeldata['Returns_x'][0:-1].values.reshape(-1,1)
            year_yData = modeldata['Returns_y'][0:-1]
            halfyear_yData = modeldata['Returns_y'][-180:-1]
            halfyear_xData = modeldata['Returns_x'][-180:-1].values.reshape(-1,1)
            month_xData = modeldata['Returns_x'][-30:-1].values.reshape(-1,1)
            month_yData = modeldata['Returns_y'][-30:-1]

            year_model = linear_model.LinearRegression()
            halfyear_model = linear_model.LinearRegression()
            month_model = linear_model.LinearRegression()
            year_model.fit(year_xData,year_yData)
            halfyear_model.fit(year_xData,year_yData)
            month_model.fit(month_xData,month_yData)
            print('ticker:{} slope is{}'.format(ticker,year_model.coef_))
            ax = plt.subplot(5,5, ctr)
            ax.set_title(ticker + " " + str(year_model.coef_))
            plt.scatter(month_xData,month_yData, color='black')   
            plt.plot(year_xData,year_model.predict(year_xData),color='blue',linewidth=1)
            plt.plot(halfyear_xData,halfyear_model.predict(halfyear_xData),color='green',linewidth=1)
            plt.plot(month_xData,month_model.predict(month_xData),color='red',linewidth=1)
            plt.axis([min(modeldata['Returns_x']),max(modeldata['Returns_x']),min(modeldata['Returns_y']),max(modeldata['Returns_y'])])
            ctr = ctr+1

        plt.show()

for i in range(1, len(tickers)-26, 26):
    plot_figure(tickers[i:i+26])

# for ticker in tickers:
#     try:
#         df = readFile('ftse/{}.csv'.format(ticker))
#         df.plot()
#         plt.show()
#     except:
#         print('cannot load data for {}'.format(ticker))
    