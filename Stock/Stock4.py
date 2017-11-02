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
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from operator import itemgetter
from heapq import nlargest

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'}
MARKET = "nasdaq"
MARKETDATA = '^NDX.csv'

def scrape_ticker_symbols(pageNo):
    print("scrape_ticker_symbols")
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    #response = requests.get('http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&pagesize50&page={}'.format(pageNo), headers=headers, verify=False)
    response = requests.get('http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&pagesize=200&page={}'.format(pageNo), headers=headers, verify=False)
    soup = bs.BeautifulSoup(response.text,'lxml')
    # with open('debug.txt', 'a', encoding='utf-8') as the_file:
    #     the_file.write(response.text)
    table = soup.find('table',id='CompanylistResults')
    tickers = []
    for row in table.findAll('tr')[1:]:
        if len(row.findAll('td')) > 1:
            ticker = row.findAll('td')[1].text.rstrip().lstrip()
            print('ticker found:{}'.format(ticker))
            tickers.append(ticker)
    return tickers

def save_ticker_symbols():
    print('save_tickers_symbols')
    cnt = 0
    pageTotal = 16
    while cnt < pageTotal:
        cnt = cnt+1
        pagedTickers = scrape_ticker_symbols(cnt)
        tickers.extend(pagedTickers)
    
    with open('{}.pickle'.format(MARKET),'wb') as f:
        pickle.dump(tickers,f)
    return tickers

def get_ticker_symbols(reload_tickers=False):
    print("get_ticker_symbols")
    if reload_tickers:
        tickers = save_ticker_symbols()
    else:
        with open('{}.pickle'.format(MARKET),'rb') as f:
            tickers = pickle.load(f)
    return tickers

def get_ticker_historical_data_from_web(ticker, startTime, endTime):
    try:
        df = web.DataReader(ticker,'google', startTime, endTime)
        df.to_csv('{}/{}.csv'.format(MARKET,ticker))
        return df
    except:
        return pd.DataFrame({'empty' : []})

def readFile(file_name):
    print('readFile {}'.format(file_name))
    data = pd.read_csv(file_name,sep=',',usecols=[0,4],names=['Date','Price'],header=1)
    returns = np.array(data['Price'][1:],np.float)/np.array(data['Price'][:-1],np.float)-1
    data['Returns'] = np.append(returns,np.nan)
    data.index = data['Date']
    return data

def get_ticker_data(ticker,startTime,endTime):
    print('get_ticker_data {} {} {}'.format(ticker, startTime, endTime))
    if not os.path.exists(MARKET):
        os.makedirs(MARKET)
    try:
        return readFile('{}/{}.csv'.format(MARKET,ticker))
    except:
        return pd.DataFrame({'empty' : []})


def load_market_data():
    marketdata = pd.read_csv(MARKETDATA,sep=',',usecols=[0,5],names=['Date','Price'],header=1)
    marketreturns = np.array(marketdata['Price'][1:],np.float)/np.array(marketdata['Price'][:-1],np.float)-1
    marketdata['Returns'] = np.append(marketreturns,np.nan)
    marketdata.index = marketdata['Date']
    return marketdata

def get_coefficients(tickers, top):
    ranking = {}
    #ranking[ticker] = coeff
    for ticker in tickers:
        df = get_ticker_data(ticker, startTime, endTime)
        if df.empty:
            continue
        if len(df) < 2:
            continue
        modeldata = pd.merge(marketdata,df,how='inner',on=['Date'])
        # if len(modeldata) == 0:
        #     continue
        year_xData = modeldata['Returns_x'][0:-1].values.reshape(-1,1)
        year_yData = modeldata['Returns_y'][0:-1]
        year_model = linear_model.LinearRegression()
        year_model.fit(year_xData,year_yData)
        print('coefficient for {} is {}'.format(ticker,year_model.coef_))
        ranking[ticker] = year_model.coef_

    return sorted(ranking.items(), key=itemgetter(1), reverse=True)[:top]

def plot_figures(tickers):
        fig, ax = plt.subplots(nrows=5, ncols=5)
        fig.tight_layout()
        ctr = 1
        for ticker in tickers:
            print('plot_figure:{}'.format(ticker))
            df = get_ticker_data(ticker, startTime, endTime)
            if df.empty:
                continue
            if len(df) < 2:
                continue

            modeldata = pd.merge(marketdata,df,how='inner',on=['Date'])

            if len(modeldata) < 2:
                continue

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
            plt.scatter(year_xData,year_yData, color='black')   
            plt.plot(year_xData,year_model.predict(year_xData),color='blue',linewidth=1)
            plt.plot(halfyear_xData,halfyear_model.predict(halfyear_xData),color='green',linewidth=1)
            plt.plot(month_xData,month_model.predict(month_xData),color='red',linewidth=1)
            plt.axis([min(modeldata['Returns_x']),max(modeldata['Returns_x']),min(modeldata['Returns_y']),max(modeldata['Returns_y'])])
            ctr = ctr+1
        plt.show()

marketdata = load_market_data()

print('getting the ticker symbols')
tickers = get_ticker_symbols(reload_tickers=False)

tickers = tickers[:50]
tickers = ['MSFT']
#print(tickers)
#sys.exit(0)

startTime = dt.datetime(2017,4,1)
endTime = dt.datetime(2017,10,1)

# for ticker in tickers:
#     get_ticker_cal_data_from_web(ticker,startTime,endTime)

print('getting coefficients for {} tickers'.format(len(tickers)))
chosen = get_coefficients(tickers[:100],25)

chosen_tickers = dict(chosen).keys()
#tickers = (x[0] for x in get_coefficients(tickers[:100],10))

plot_figures(chosen_tickers)
sys.exit(0)

for ticker in tickers[100:151]:
    print('getting ticker data for:{}'.format(ticker))
    get_ticker_data(ticker, startTime, endTime)

# sys.exit(0)


# for ticker in tickers:
#     print('getting ticker data for:{}'.format(ticker))
#     get_ticker_data(ticker, startTime, endTime)

#sys.exit(0)

for i in range(100, len(tickers)-26, 26):
    plot_figure(tickers[i:i+26])


    