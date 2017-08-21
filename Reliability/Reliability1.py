import bs4 as bs
import pickle
import requests
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

import pandas as pd
import matplotlib.pyplot as plt


n_topics = 5
n_top_words = 10
max_pages = 20
search_term = 'VW%20Touran'

# conda config --set ssl_verify False
# pip install -U requests[security] 
def scrape_reviews(pageNo):
    response = requests.get('https://www.honestjohn.co.uk/Forum/Search?days=300&pg={}&q=' + search_term.format(pageNo), verify=False)
    soup = bs.BeautifulSoup(response.text,'lxml')
    table = soup.find('table',{'class','item_list'})
    reviews = []
    for row in table.findAll('tr')[1:]:
        review = row.findAll('td')[0].text
        reviews.append(review.rstrip().lstrip())
    return reviews

def save_reviews():
    reviews = []
    cnt = 0
    while cnt < max_pages:
        cnt = cnt+1
        pagedReviews = scrape_reviews(cnt)
        reviews.extend(pagedReviews)
    
    with open('reviews.pickle','wb') as f:
        pickle.dump(reviews,f)
    return reviews

def get_reviews(reload_reviews=False):
    if reload_reviews:
        reviews = save_reviews()
    else:
        with open('reviews.pickle','rb') as f:
            reviews = pickle.load(f)
    return reviews

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()

reviews = get_reviews(reload_reviews=True)

print("reviews loaded:", len(reviews))   

tfidf_vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words='english')
tfidf = tfidf_vectorizer.fit_transform(reviews)
km = KMeans(n_clusters=n_topics, init='k-means++', max_iter=100, n_init=1, verbose=True)
km.fit(tfidf)

nmf = NMF(n_components=n_topics, random_state=1,
          alpha=.1, l1_ratio=.5).fit(tfidf)

tfidf_feature_names = tfidf_vectorizer.get_feature_names()
print(tfidf_feature_names)
print_top_words(nmf, tfidf_feature_names, n_top_words)

