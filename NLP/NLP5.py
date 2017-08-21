import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup

def getText(testURL):
    response = requests.get(testURL, verify=False)
    soup = BeautifulSoup(response.text,'lxml')
    return soup.find('div',{'class':'content__article-body'}).text # .encode('ascii', errors='replace').replace('?',' ')

articleURL = 'https://www.theguardian.com/tv-and-radio/2017/aug/21/game-of-thrones-the-best-show-on-tv-just-became-the-silliest'

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
text = getText(articleURL)

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from string import punctuation 

sents = sent_tokenize(text)
#print(sents)

word_sent = word_tokenize(text.lower())
print(word_sent)

stopWords=set(stopwords.words('english') + list(punctuation) + ['warning'])

word_sent = [word for word in word_sent if word not in stopWords]

print(word_sent)




