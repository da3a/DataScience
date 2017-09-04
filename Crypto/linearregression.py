from sklearn import datasets
from sklearn import linear_model
import sys
import pandas as pd

data = datasets.load_boston()

df = pd.DataFrame(data.data, columns=data.feature_names)

target = pd.DataFrame(data.target, columns=['MEDV'])

X = df
y = target['MEDV']

lm = linear_model.LinearRegression()
model = lm.fit(X,y)

lm.score(X,y)

predictions = lm.predict(X)
print(predictions[0:5])

print(lm.score(X,y))
print(lm.coef_)
print(lm.intercept_)
