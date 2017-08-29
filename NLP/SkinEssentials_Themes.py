import requests
from bs4 import BeautifulSoup
import nltk

from requests.packages.urllib3.exceptions import InsecureRequestWarning


baseUrl = 'https://community.sephora.com/?pageNum={}&purpose=recent&onlyPhotos=false&trendingTag=&isMyPost=false&userId=-1'

def scrapeReviews(pageNo):
    url = baseUrl.format(pageNo)
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url,verify=False)
    soup = BeautifulSoup(response.text,'lxml')
    for div in soup.findAll('div',attrs={'class': 'message-body'}):
        print(div.text)
    print(url)

# from nltk.corpus import wordnet as wn
# for ss in wn.synsets('protection'):
#     print(ss, ss.definition(), ss.lemma_names())


from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
example_sentence = "David's home is currently 30 Edensor Drive, Belper."
stop_words = set(stopwords.words('english'), ['Edensor'])

print(stop_words)

words = word_tokenize(example_sentence)
filtered_sentence = []

for w in words:
    if w not in stop_words:
        filtered_sentence.append(w)


filtered_sentence = [w for w in words if not w in stop_words]

print(filtered_sentence)


#scrapeReviews(1)