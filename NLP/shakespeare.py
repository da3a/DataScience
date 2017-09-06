import nltk
import string
import os
import sys

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.cluster import KMeans
from nltk.probability import FreqDist
from heapq import nlargest

nClusters = 3
path = 'c:/dawa/corpora'
token_dict = {}
stemmer = PorterStemmer()

print(nltk.__file__)

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems

for subdir, dirs, files in os.walk(path):
    for file in files:
        file_path = subdir + os.path.sep + file
        shakes = open(file_path, 'r')
        text = shakes.read()
        lowers = text.lower()
        #no_punctuation = lowers.translate(None, string.punctuation)
        no_punctuation = lowers.translate(str.maketrans('','',string.punctuation))
        token_dict[file] = no_punctuation
        print(token_dict[file])
        
#this can take some time
tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
tfs = tfidf.fit_transform(token_dict.values())


sys.exit(0)
km = KMeans(n_clusters=nClusters,init='k-means++',max_iter=100,n_init=1, verbose=True)
km.fit(tfs)