import bs4 as bs
import pickle
import requests
import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import os
import matplotlib.pyplot as plt

def scrape_tickers(pageNo):
    response = requests.get('http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/summary/summary-indices-constituents.html?index=ASX&page={}'.format(pageNo))
    soup = bs.BeautifulSoup(response.text,'lxml')
    table = soup.find('table',{'class','table_dati'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
    return tickers

def save_ftse_tickers():
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
    if reload_tickers:
        tickers = save_ftse_tickers()
    else:
        with open('ftse.pickle','rb') as f:
            tickers = pickle.load(f)
    return tickers

def get_ticker_data(startTime, endTime):
    if not os.path.exists('ftse'):
        os.makedirs('ftse')
    try:
        df = web.DataReader(ticker,'google', startTime, endTime)
        df.to_csv('ftse/{}.csv'.format(ticker))
    except:
        print('error getting data for {}'.format(ticker))


tickers = get_ftse_tickers(reload_tickers=False)

startTime = dt.datetime(2012,1,1)
endTime = dt.datetime(2017,5,1)

for ticker in tickers:
    #get_ticker_data(startTime, endTime)
    try:
        df = pd.read_csv('ftse/{}.csv'.format(ticker))
        df.plot()
        plt.show()
        break
    except:
        print('cannot load data for {}'.format(ticker))
    