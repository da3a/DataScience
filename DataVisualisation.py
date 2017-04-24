import pandas as pd
import numpy as np
from sklearn.manifold import TSNE
from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

dataframe_all = pd.read_csv('https://d396qusza40orc.cloudfront.net/predmachlearn/pml-training.csv',low_memory=False)
#dataframe_all = pd.read_csv('c:/scripts/python/datascience/pml-training.csv', low_memory=False)
num_rows = dataframe_all.shape[0]
print(num_rows)

counter_nan = dataframe_all.isnull().sum()
#print(dataframe_all.isnull().sum())
counter_without_nan=counter_nan[counter_nan==0]
#print(counter_without_nan.keys())
dataframe_all = dataframe_all[counter_without_nan.keys()]
dataframe_all = dataframe_all.ix[:, 7:]
columns = dataframe_all.columns
print("printing columns")

print("Apply a scaler")
x = dataframe_all.ix[:,:-1].values
standard_scaler = StandardScaler()
x_std = standard_scaler.fit_transform(x)

print("Encode labels")
y=dataframe_all.ix[:,-1].values
class_labels=np.unique(y)
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

print("Train Test Split")
test_percentage=0.1
x_train, x_test, y_train, y_test = train_test_split(x_std, y, test_size=test_percentage, random_state=0)

print("Apply TSNE")
tsne = TSNE(n_components=2, random_state=0)
x_test_2d = tsne.fit_transform(x_test)

print("Plot")
markers=('s','d','o','^','v')
color_map = {0:'red', 1:'blue', 2:'lightgreen', 3:'purple',4:'cyan'}
plt.figure()
for idx, cl in enumerate(np.unique(y_test)):
    plt.scatter(x=x_test_2d[y_test==cl,0], y=x_test_2d[y_test==cl,1],c=color_map[idx],marker=markers[idx],label=cl)

plt.xlabel('X in t-SNE')
plt.ylabel('Y in t-SNE')
plt.legend(loc='upper left')
plt.title('t-SNE visualisation of test data')
plt.show()