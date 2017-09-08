#links
#http://www.nltk.org/book/ch07.html
#http://www.cs.duke.edu/courses/spring14/compsci290/assignments/lab02.html

import requests
import nltk
import pickle
import sys
import numpy as np

from bs4 import BeautifulSoup
from string import punctuation
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import wordnet as wn
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.probability import FreqDist
from heapq import nlargest
#nltk.help.upenn_tagset()


baseUrl = 'https://community.sephora.com{}'
reviewUrl = baseUrl.format('/?pageNum={}&purpose=recent&onlyPhotos=false&trendingTag=&isMyPost=false&userId=-1')

baseSkincareTalkUrl = 'http://www.skincaretalk.com/{}'
skincareReviewUrl = baseSkincareTalkUrl.format('forumdisplay.php/5-Basic-Skin-Care/Page{}')


maxPages = 1
reviews = []
filtered_reviews = []
fileName = 'sephora.pickle'
skincareFileName = 'skincare.pickle'
nClusters = 3
_stopwords = set(stopwords.words('english') + list(punctuation) + ['\'s', '\'m', 'n\'t', '...','\'ve', '’'])

token_dict = {}
stemmer = PorterStemmer()

def scrapeReviewsSephora(pageNo, readThread = False):
    url = reviewUrl.format(pageNo)
    print("calling:",url)
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url,verify=False)
    soup = BeautifulSoup(response.text,'lxml')   
    for div in soup.findAll('div',attrs={'class': 'message-body'}):
        readmoreUrl = soup.find('a',attrs={'class':'read-more'})
        if readmoreUrl and readThread: 
            href = readmoreUrl.get('href')
            print("calling inner:",baseUrl.format(href))
            innerResponse = requests.get(baseUrl.format(href),verify=False)
            soup = BeautifulSoup(innerResponse.text,'lxml')
            for divInner in soup.findAll('div',attrs={'class': 'lia-message-body-content'}):
                reviews.append(divInner.text)
        else:
            reviews.append(div.text)
    if pageNo < maxPages:
            scrapeReviews(pageNo = pageNo + 1)
    with open(fileName,'wb') as f:
        pickle.dump(reviews,f)

def scrapeReviewsV1(pageNo, readThread = False):
    url = reviewUrl.format(pageNo)
    print("calling:",url)
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url,verify=False)
    post = ''
    soup = BeautifulSoup(response.text,'lxml')   
    for div in soup.findAll('div',attrs={'class': 'message-body'}):
        readmoreUrl = soup.find('a',attrs={'class':'read-more'})
        if readmoreUrl and readThread: 
            href = readmoreUrl.get('href')
            print("calling inner:",baseUrl.format(href))
            innerResponse = requests.get(baseUrl.format(href),verify=False)
            soup = BeautifulSoup(innerResponse.text,'lxml')
            for divInner in soup.findAll('div',attrs={'class': 'lia-message-body-content'}):
                post += divInner.text
        else:
            post += div.text
        reviews.append(post)
    if pageNo < maxPages:
            scrapeReviewsV1(pageNo = pageNo + 1)
    with open(fileName,'wb') as f:
        pickle.dump(reviews,f)

def scrapeReviewsSkinCareTalk(pageNo, readThread = False):
    url = skincareReviewUrl.format(pageNo)
    print("calling:",url)
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url,verify=False)
    with open('dump.txt','w') as f:
        f.write(response.text)
    soup = BeautifulSoup(response.text,'lxml')
    for link in soup.findAll('a',attrs={'class':'title'}):     
        print('found title')
        href = link.get('href')
        if href and readThread:
            print(link.text) 
            print("calling inner:",baseSkincareTalkUrl.format(href))
            innerResponse = requests.get(baseSkincareTalkUrl.format(href),verify=False)
            soup = BeautifulSoup(innerResponse.text,'lxml')
            for divInner in soup.findAll('div',attrs={'class': 'content'}):
                reviews.append(divInner.text)
    if pageNo < maxPages:
            scrapeReviewsSkinCareTalk(pageNo = pageNo + 1)
    with open(skincareFileName,'wb') as f:
        pickle.dump(reviews,f)


def getAllReviews(reload = False):
    global reviews
    if reload:
        scrapeReviewsSkinCareTalk(1,readThread=True)
    else:
        with open(skincareFileName,'rb') as f:
            reviews = pickle.load(f)

def extract_Tokens(tokens, review):
    sents = sent_tokenize(review)
    for i in sents:
        words = nltk.word_tokenize(i)
        tagged = nltk.pos_tag(words)
        for pair in tagged:
            tag = pair[1]
            if not set(tokens).isdisjoint([tag]):
                nouns.append(pair[0])
    
def parse_np(psent):
  for subtree in psent.subtrees():
      if subtree.label() == 'NP':
        yield ' '.join(word for word, tag in subtree.leaves())

def extract_nounPhrases(review):
    grammar = 'NP: {<JJ><NN>}' # 'NP: {<DT>?<JJ>*<NN>}'
    nounPhrases = []
    sents = sent_tokenize(review)
    for i in sents:
        words = nltk.word_tokenize(i)
        tagged = nltk.pos_tag(words)
        cp = nltk.RegexpParser(grammar)
        result = cp.parse(tagged)
        for npstr in parse_np(result):
            nounPhrases.append(npstr.replace(' ', '-'))
    return ' '.join(nounPhrases)

def preProcessReviews():
    print("will remove stopwords etc")
    _stopwords = set(stopwords.words('english') + list(punctuation) + ['\'s', '@ '])
    for i, review in enumerate(reviews):
        review = review.lower()
        all_words = word_tokenize(review)
        all_words = [word for word in all_words if word not in _stopwords]
        token_dict[i] = ' '.join(all_words)

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    _stopwords = set(stopwords.words('english') + list(punctuation) + ['\'s', '@ ','sephora'])   
    tokens = nltk.word_tokenize(text)
    tokens = [word for word in tokens if word not in _stopwords]
    stems = stem_tokens(tokens,stemmer)
    return stems
    #return tokens

def tokenize_NounPhrases(text):
    grammar = 'NP: {<JJ><NN>}' # 'NP: {<DT>?<JJ>*<NN>}'
    nounPhrases = []
    sentences = sent_tokenize(text)
    for sent in sentences:
        words = nltk.word_tokenize(sent)
        tagged = nltk.pos_tag(words)
        cp = nltk.RegexpParser(grammar)
        result = cp.parse(tagged)
        for npstr in parse_np(result):
            nounPhrases.append(npstr.replace(' ', '-'))
    print('nounPhrases', "".join(nounPhrases))
    return nounPhrases 

def getClusterText(labelledClusters):
    text = {}
    for i, cluster in enumerate(labelledClusters):
        oneDocument = reviews[i]
        if cluster not in text.keys():
            text[cluster] = oneDocument
        else:
            text[cluster] += oneDocument
    return text

def getFreqDistFromClusteredText(clusteredText):
    counts = {}
    for cluster in range(nClusters):
        word_sent = word_tokenize(clusteredText[cluster].lower())
        word_sent = [word for word in word_sent if word not in _stopwords]
        freq = FreqDist(word_sent)
        counts[cluster]=freq
    return counts

def getTopWordsFromClusteredText(clusteredText, nWords):
    keywords = {}
    for cluster in range(nClusters):
        word_sent = word_tokenize(clusteredText[cluster].lower())
        word_sent = [word for word in word_sent if word not in _stopwords]
        freq = FreqDist(word_sent)
        keywords[cluster] = nlargest(nWords, freq, key=freq.get)
    return keywords


def filterOnAnySearchTerms(articles, searchTerms):
    filteredArticles = []
    for article in articles:
        if not set(word_tokenize(article)).isdisjoint(searchTerms):
            filteredArticles.append(article)
    return filteredArticles

def filterOnAllSearchTerms(articles, searchTerms):
    filteredArticles = []
    for article in articles:
        if set(searchTerms).issubset(set(word_tokenize(article))):
            filteredArticles.append(article)
    return filteredArticles

#############################################

nounPhraseList = []
nouns = []
getAllReviews(True)



for review in reviews:
    print(review)
print('found these reviews:',len(reviews))

sys.exit(0)

#sys.exit(0)
# for review in filterOnAllSearchTerms(reviews, ['sensitive','oily']):
#     print('article:', review)

# sys.exit(0)

# for review in reviews:
#     nps = extract_nounPhrases(review)
#     if len(nps) > 0:
#         #print(nps)
#         nounPhraseList.append(nps)

# preProcessReviews()

#print(list(token_dict.values()))


#vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words='english')
vectorizer = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
X =  vectorizer.fit_transform(reviews)
#X = vectorizer.fit_transform(list(token_dict.values()))
#X = vectorizer.fit_transform(nounPhraseList)

print(X)
km = KMeans(n_clusters=nClusters,init='k-means++',max_iter=100,n_init=1, verbose=True)
km.fit(X)
print(np.unique(km.labels_,return_counts=True))# indicates cluster numbers and counts in each cluster

# text_file = open("skin.txt", "w", encoding="utf8")
# for i, cluster in enumerate(km.labels_):
#     if cluster==2:
#         text_file.write("REVIEW:" + reviews[i])
#         print("REVIEW:",reviews[i])
# text_file.close()

# vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words='english')
# X = vectorizer.fit_transform(reviews)

# km = KMeans(n_clusters=nClusters,init='k-means++',max_iter=100,n_init=1, verbose=True)
# km.fit(X)
# print(np.unique(km.labels_,return_counts=True))

clusteredText = getClusterText(km.labels_)

keywords = getTopWordsFromClusteredText(clusteredText, 10)
counts = getFreqDistFromClusteredText(clusteredText)


for cluster in range(nClusters):
    word_sent = word_tokenize(clusteredText[cluster].lower())
    word_sent = [word for word in word_sent if word not in _stopwords]
    freq = FreqDist(word_sent)
    keywords[cluster] = nlargest(10, freq, key=freq.get)
    counts[cluster]=freq

# for cluster in range(nClusters):
#     print(keywords[cluster])


unique_keys = {}
for cluster in range(nClusters):
    other_clusters = list(set(range(nClusters))-set([cluster]))
    keys_other_clusters=set(keywords[other_clusters[0]]).union(set(keywords[other_clusters[1]]))
    unique=set(keywords[cluster])-keys_other_clusters
    unique_keys[cluster] = nlargest(10,unique, key=counts[cluster].get)

print("printing unique keys: ", unique_keys)

# for i, (k,v) in unique_keys:
#     print(i,k,v)

sys.exit(0)

# print("*"*50)
# count=0
# for i in range(len(reviews)):
#     if count > 3:
#         break
#     if km.labels_[i]==0:
#         print(reviews[i])
#         count+=1



# text = {}
# for i, cluster in enumerate(km.labels_):
#     print(i,cluster)

    # oneDocument = reviews[i]
    # if cluster not in text.keys():
    #     text[cluster] = oneDocument
    # else:
    #     text[cluster] += oneDocument



sys.exit(0)

for ss in wn.synsets('protect'):
    for sim in ss.similar_tos():
        print('    {}'.format(sim))




synonyms =[]
antonyms = []


for syn in wordnet.synsets('protect'):
    for l in syn.lemmas():
        print(l)
        synonyms.append(l.name())
        if l.antonyms():
            for a in l.antonyms():
                antonyms.append(a.name())

print(synonyms)




# from nltk.corpus import wordnet as wn
# for ss in wn.synsets('protection'):
#     print(ss, ss.definition(), ss.lemma_names())

sentence = "David's home is currently 30 Edensor Drive, Belper."
all_words = word_tokenize(sentence)
print(all_words)
_stopwords = set(stopwords.words('english') + list(punctuation) + ['\'s'])
all_words = [word for word in all_words if word not in _stopwords]

print(all_words)

sys.exit(0)

sents = sent_tokenize(all_words)

words = word_tokenize(all_words)
filtered_sentence = []

# for w in words:
#     if w not in _stopwords:
#         filtered_sentence.append(w)


# filtered_sentence = [w for w in words if not w in stop_words]

print(filtered_sentence)


#scrapeReviews(1)