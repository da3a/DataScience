#https://matplotlib.org/users/pyplot_tutorial.html
import matplotlib.pyplot as plt
from sklearn import linear_model
import sys
import numpy


X = [0,1,2,3,4]
Y = [4,5,7,8,7]

plt.plot(X,Y,'ro')
plt.ylabel('some numbers')

lm = linear_model.LinearRegression()

print(type(numpy.ndarray(X)))

model = lm.fit(numpy.ndarray(X),Y)


sys.exit(0)

sys.exit(0)
predictions = lm.predict(X)

plt.plot(X, predictions, color='blue', linewidth=3)

plt.show()

