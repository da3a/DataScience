import requests
from bs4 import BeautifulSoup

articleURL = "http://www.bbc.co.uk/news/amp/40745533"

def getTextWaPo(url):
    page = requests.get(articleURL, verify=False)
    soup = BeautifulSoup(response.text,'lxml')
    text = ' '.join(map(lambda p: p.text, soup.find('div',{'class','main_article_text '}).text))
    return text.encode('ascii', errors='replace').replace("?"," ")


response = requests.get(articleURL, verify=False)
soup = BeautifulSoup(response.text,'lxml')
#print(soup)

text = soup.find('div',{'class','main_article_text'}).text

#text.encode('ascii', errors='replace').replace("?"," ")
#print(getTextWaPo(articleURL))

from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from string import punctuation

sents = sent_tokenize(text)
print(sents)

word_sent = word_tokenize(text.lower())
_stopwords = set(stopwords.words('english') + list(punctuation) + ['bbc.co.uk', '``', "''", 'vars',"'s","'m"])
#print(_stopwords)

word_sent = [word for word in word_sent if word not in _stopwords]

from nltk.probability import FreqDist
freq = FreqDist(word_sent)

from heapq import nlargest

print(nlargest(10, freq, key=freq.get))

from collections import defaultdict

ranking = defaultdict(int)

for i,sent in enumerate(sents):
    for w in word_tokenize(sent.lower()):
        if w in freq:
            ranking[i] += freq[w]

sents_idx = nlargest(4,ranking,key=ranking.get)


#print([sents[j] for j in sorted(sents_idx)])
