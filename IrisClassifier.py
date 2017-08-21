import tensorflow.contrib.learn as skflow
#import tensorflow.contrib.learn.python.learn as learn
from sklearn import datasets, metrics

print("Iris Classifier")

iris = datasets.load_iris()

feature_columns = skflow.infer_real_valued_columns_from_input(iris.data)

#classifier= skflow.Tens

classifier = skflow.SKCompat(skflow.LinearClassifier(n_classes=3, feature_columns=feature_columns))

classifier.fit(iris.data, iris.target)

score = metrics.accuracy_score(iris.target, classifier.predict(iris.data))
print("Accuracy: %f" % score)