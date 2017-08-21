import csv
import numpy as np
from sklearn.svm    import SVR
import matplotlib.pyplot as plt

dates = []
prices = []

def get_data(filename):
    with open(filename,'r') as csvfile:
        csvFileReader=csv.reader(csvfile)
        next(csvFileReader)
        ctr=250
        for row in csvFileReader:
            dates.append(ctr)
            prices.append(float(row[1]))
            ctr=ctr-1
    return

def predict_prices(dates, prices, x):
    dates=np.reshape(dates, (len(dates),1))
    svr_lin =SVR(kernel='linear',C=10)
    svr_lin.fit(dates, prices)

    plt.scatter(dates,prices,color='black', label='Data')
    plt.plot(dates, svr_lin.predict(dates),color='green', label='linear_model')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Support Vector Regression')
    plt.legend()

    plt.show()
    return svr_lin.predict(x)[0]

get_data('C:\\Scripts\\Python\\DataScience\\data\\brk.b.csv')

print('dates read %s' % dates)
print('\n')
print('prices %s' % prices)

predicted_prices = predict_prices(dates, prices, 250)
print(predicted_prices)


