import bs4 as bs
import pickle
import requests
import datetime as dt
import os
import pandas as pd
import pandas_datareader as web


def save_sp500_tickers():
    response = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies', verify=False)
    soup = bs.BeautifulSoup(response.text,'lxml').encode('ascii')
    table = soup.find('table',{'class':'wikitable sortable'})
    print(table)
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)

    with open('sp500tickers.pickle','wb') as f:
        pickle.dump(tickers,f)

    return tickers
    
save_sp500_tickers()


