#AutoSummarizer - select n sentences fromn an article that best describe that article. 
# Sentences are ranked by term frequency - capture how often every word occurs in a document and for each sentence create a sum total. 
# 
#pip install nltk
#nltk.download() to pull supporting libraries
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from string import punctuation
from collections import defaultdict
from heapq import nlargest

#request article at url, parse html and return text from div with attributes attr
def getArticle(url, attrs):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup.find('div',attrs).text

#return n sentences that best summarizes the text
# break text into sentences and words. Sentences are identified by ". "
# remove stopwords from words
# for each word count number of times that word appears in text
# rank sentences by adding up the freq count for each word in that sentence
# return the top n ranked sentences 
def summarize(text, numberOfSentences):
    sents = sent_tokenize(text)
    assert numberOfSentences <= len(sents)

    word_sent = word_tokenize(text.lower())
    _stopwords = set(stopwords.words('english') + list(punctuation))
    word_sent = [word for word in word_sent if word not in _stopwords]
    freq = FreqDist(word_sent)

    ranking = defaultdict(int)

    for i,sentence in enumerate(sents):
        for w in word_tokenize(sentence.lower()):
            if w in freq:
                ranking[i] += freq[w]
    
    sents_idx = nlargest(numberOfSentences, ranking, key=ranking.get)
    return [sents[j] for j in sorted(sents_idx)]

articleURL= 'https://www.theguardian.com/technology/2017/aug/20/two-year-olds-should-learn-to-code-says-computing-pioneer'

article = getArticle(articleURL, {'class' : 'content__article-body'})
summary = summarize(article, 3)
print(summary)

