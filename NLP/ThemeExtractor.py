#ThemeExtractor - downloads articles and uses a KMeans Clustering algorithm to group artiules into n clusters
#  
from bs4 import BeautifulSoup
import pickle
import requests 
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

import numpy as numpy

reviewsFileName = 'reviews.pickle'
searchTerm = 'pg={}&q=VW%20Touran'
maxPages=100
reviews=[]
nClusters = 5

def scrapeReviews(pageNo):
    url = 'https://www.honestjohn.co.uk/Forum/Search?days=300&' + searchTerm.format(pageNo)
    print(url)
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text,'lxml')
    table = soup.find('table',{'class':'item_list'})
    for row in table.findAll('tr')[1:]:
        review = row.findAll('td')[0].text
        print(review)
        reviews.append(review)

    if pageNo < maxPages:
        scrapeReviews(pageNo = pageNo+1)
    
    with open(reviewsFileName,'wb') as f:
        pickle.dump(reviews,f)

def getReviews(reload = False):
    global reviews
    if reload:
        scrapeReviews(1)
    else:
        with open(reviewsFileName,'rb') as f:
            reviews = pickle.load(f)
        

getReviews(False)

vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words='english')
X = vectorizer.fit_transform(reviews)

km = KMeans(n_clusters=nClusters, init='k-means++', max_iter=100,n_init=1,verbose=True)
km.fit(X)

text = {}
for i, cluster in enumerate(km.labels_):
    oneDocument = reviews[i]
    if cluster not in text.keys():
        text[cluster] = oneDocument
    else:
        text[cluster] += oneDocument

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import nltk

_stopwords = set(stopwords.words('english') + list(punctuation))

keywords={}
counts={}
for cluster in range(nClusters):
    word_sent = word_tokenize(text[cluster].lower())
    word_sent = [word for word in word_sent if word not in _stopwords]
    freq = FreqDist(word_sent)
    keywords[cluster] = nlargest(10, freq, key=freq.get)
    counts[cluster]=freq

unique_keys = {}
for cluster in range(nClusters):
    other_clusters = list(set(range(nClusters))-set([cluster]))
    keys_other_clusters=set(keywords[other_clusters[0]]).union(set(keywords[other_clusters[1]]))
    unique=set(keywords[cluster])-keys_other_clusters
    unique_keys[cluster] = nlargest(10,unique, key=counts[cluster].get)

print(unique_keys)