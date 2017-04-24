from sklearn import tree


# https://github.com/llSourcell/gender_classification_challenge


clf = tree.DecisionTreeClassifier()
clf1 = tree.ExtraTreeClassifier()


# [height, weight, shoe_size]
X = [[181, 80, 44], [177, 70, 43], [160, 60, 38], [154, 54, 37], [166, 65, 40],
     [190, 90, 47], [175, 64, 39],
     [177, 70, 40], [159, 55, 37], [171, 75, 42], [181, 85, 43]]

Y = ['male', 'male', 'female', 'female', 'male', 'male', 'female', 'female',
     'female', 'male', 'male']

# CHALLENGE - ...and train them on our data
clf = clf.fit(X, Y)

clf1 = clf1.fit(X,Y)

prediction = clf.predict([[159, 55, 42]])

prediction1 = clf1.predict([159,55,42])

# CHALLENGE compare their reusults and print the best one!

print(prediction)
print(prediction1)