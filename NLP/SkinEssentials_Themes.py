#links
#http://www.nltk.org/book/ch07.html

import requests
import nltk
import pickle
import sys

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
maxPages = 10
reviews = []
filtered_reviews = []
fileName = 'sephora.pickle'
nClusters = 3
_stopwords = set(stopwords.words('english') + list(punctuation) + ['\'s', '\'m', 'n\'t', '...'])

def scrapeReviews(pageNo, readThread = False):
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
    else:
        print('Nothing found....')
    if pageNo < maxPages:
            scrapeReviews(pageNo = pageNo + 1)
    with open(fileName,'wb') as f:
        pickle.dump(reviews,f)


def getAllReviews(reload = False):
    global reviews
    if reload:
        scrapeReviews(1,readThread=True)
    else:
        with open(fileName,'rb') as f:
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
            nounPhrases.append(npstr)
    return nounPhrases

nounPhraseList = []
nouns = []
getAllReviews(False)
print('found these reviews:',len(reviews))

for review in reviews[:10]:
    nps = extract_nounPhrases(review)
    if len(nps) > 0:
        print(nps)
        nounPhraseList.append(nps)


token_dict = {}
stemmer = PorterStemmer()

def preProcessReviews():
    print("will remove stopwords etc")
    _stopwords = set(stopwords.words('english') + list(punctuation) + ['\'s'])
    for i, review in enumerate(reviews):
        review = review.lower()
        all_words = word_tokenize(review)
        all_words = [word for word in all_words if word not in _stopwords]
        token_dict[i] = all_words

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    tokens = nltk.tokenize(text)
    stems = stem_tokens(tokens,stemmer)
    return stems

preProcessReviews()

vectorizer = TfidfVectorizer(tokenizer=tokenize, stop_words='english')

print(token_dict.values())
sys.exit(0)
X = vectorizer.fit_transform(token_dict.values())

sys.exit(0)

# for review in reviews:
#     print(review)

#print(nouns)

# nounFreq = FreqDist(nounPhraseList)

# from heapq import nlargest
# print(nlargest(50, nounFreq, key=nounFreq.get))

#nltk.help.upenn_tagset()

#filter down reviews

# for review in reviews:
#     if set(word_tokenize(review)).intersection(['protect']):
#         filtered_reviews.append(review)
# print(len(filtered_reviews))
# for review in filtered_reviews:
#     print(review)
# sys.exit(0)

vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words='english')
X = vectorizer.fit_transform(reviews)

km = KMeans(n_clusters=nClusters,init='k-means++',max_iter=100,n_init=1, verbose=True)
km.fit(X)

print(km.labels_)

text = {}
for i, cluster in enumerate(km.labels_):
    oneDocument = reviews[i]
    if cluster == 1:
        print(oneDocument)
    if cluster not in text.keys():
        text[cluster] = oneDocument
    else:
        text[cluster] += oneDocument

keywords={}
counts={}
for cluster in range(nClusters):
    word_sent = word_tokenize(text[cluster].lower())
    word_sent = [word for word in word_sent if word not in _stopwords]
    freq = FreqDist(word_sent)
    keywords[cluster] = nlargest(10, freq, key=freq.get)
    counts[cluster]=freq

for cluster in range(nClusters):
    print(keywords[cluster])

sys.exit(0)


# unique_keys = {}
# for cluster in range(nClusters):
#     other_clusters = list(set(range(nClusters))-set([cluster]))
#     keys_other_clusters=set(keywords[other_clusters[0]]).union(set(keywords[other_clusters[1]]))
#     unique=set(keywords[cluster])-keys_other_clusters
#     unique_keys[cluster] = nlargest(10,unique, key=counts[cluster].get)

# print(unique_keys)


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