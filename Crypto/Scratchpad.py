
#https://pandas.pydata.org/pandas-docs/stable/10min.html


import sys
import numpy as np
import pandas as pd

dates = pd.date_range('20130101', periods=6)

#print(dates)


df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))

print(df)

#print(df.values)
#print(df.T)

#print(df[0:2])

print(df.loc[dates[1]])

print(df.loc['2013-01-02'])