import nltk
import random
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
from string import punctuation
import pickle
from nltk.classify.scikitlearn import SklearnClassifier
import sys
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode

from nltk.tokenize import word_tokenize, sent_tokenize

class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))      
        conf = choice_votes / len(votes)
        return conf


short_pos = open('c:/dawa/pos.txt','r').read()
short_neg = open('c:/dawa/neg.txt','r').read()

documents = []

short_pos_words = word_tokenize(short_pos)
short_neg_words = word_tokenize(short_neg)

for r in short_pos.split('\n'):
    documents.append((r, 'pos'))

for r in short_neg.split('\n'):
    documents.append((r, 'neg'))

all_words = []

for w in short_pos_words:
    all_words.append(w.lower())
for w in short_neg_words:
    all_words.append(w.lower())

_stopwords = set(stopwords.words('english') + list(punctuation) + ['\'s', 'n\'t', '--', '``'])
all_words = [word for word in all_words if word not in _stopwords]
all_words = nltk.FreqDist(w.lower() for w in all_words)

#word_features = list(all_words.keys())[:10]
word_features =[w for (w,c) in all_words.most_common(3000)]

#print(word_features)

def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features


#print((find_features(movie_reviews.words('neg/cv000_29416.txt'))))


#each document is a tuple of words and whether the document is pos ot neg
#featuresets only includes a word if it was in the top 3000 words across all documents
featuresets = [(find_features(rev),category) for (rev,category) in documents]

random.shuffle(featuresets)

#print(len(featuresets))

training_set = featuresets[:10000]
testing_set = featuresets[10000:]

classifier = nltk.NaiveBayesClassifier.train(training_set)
# classifier_f = open('naivebayes.pickle','rb')
# classifier = pickle.load(classifier_f)
# classifier_f.close()

print('Naive Bayes Algo accuracy precent:', (nltk.classify.accuracy(classifier, testing_set)) * 100)
classifier.show_most_informative_features(20)

save_classifier = open('naivebayes.pickle','wb')
pickle.dump(classifier, save_classifier)
save_classifier.close()


MNB_classifier =  SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print('MNB Algo accuracy precent:', (nltk.classify.accuracy(MNB_classifier, testing_set)) * 100)

B_classifier =  SklearnClassifier(BernoulliNB())
B_classifier.train(training_set)
print('Bernoulli Algo accuracy precent:', (nltk.classify.accuracy(B_classifier, testing_set)) * 100)

# G_classifier =  SklearnClassifier(GaussianNB())
# G_classifier.train(training_set)
# print('Gaussian Algo accuracy precent:', (nltk.classify.accuracy(G_classifier, testing_set)) * 100)

LogisticRegression_classifier =  SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print('Logistic Regression Algo accuracy precent:', (nltk.classify.accuracy(LogisticRegression_classifier, testing_set)) * 100)

SGDC_classifier =  SklearnClassifier(SGDClassifier())
SGDC_classifier.train(training_set)
print('SGDC Algo accuracy precent:', (nltk.classify.accuracy(SGDC_classifier, testing_set)) * 100)

# SVC_classifier =  SklearnClassifier(SVC())
# SVC_classifier.train(training_set)
# print('SVC Algo accuracy precent:', (nltk.classify.accuracy(SVC_classifier, testing_set)) * 100)

LinearSVC_classifier =  SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print('LinearSVC Algo accuracy precent:', (nltk.classify.accuracy(LinearSVC_classifier, testing_set)) * 100)

NuSVC_classifier =  SklearnClassifier(NuSVC())
NuSVC_classifier.train(training_set)
print('NuSVC Algo accuracy precent:', (nltk.classify.accuracy(NuSVC_classifier, testing_set)) * 100)

voted_classifier = VoteClassifier(classifier,
                                     MNB_classifier,
                                     B_classifier, 
                                     LogisticRegression_classifier,
                                     SGDC_classifier, 
                                     LinearSVC_classifier, 
                                     NuSVC_classifier )
print('Voted_Classifier NuSVC Algo accuracy percent:', (nltk.classify.accuracy(voted_classifier, testing_set)) * 100)

# print('"Classification', voted_classifier.classify(testing_set[0][0]), '%Confidence:', voted_classifier.confidence(testing_set[0][0]))
# print('"Classification', voted_classifier.classify(testing_set[1][0]), '%Confidence:', voted_classifier.confidence(testing_set[1][0]))
# print('"Classification', voted_classifier.classify(testing_set[2][0]), '%Confidence:', voted_classifier.confidence(testing_set[2][0]))
# print('"Classification', voted_classifier.classify(testing_set[3][0]), '%Confidence:', voted_classifier.confidence(testing_set[3][0]))

sys.exit()