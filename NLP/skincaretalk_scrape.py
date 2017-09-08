

import requests
from requests_ntlm import HttpNtlmAuth
import pickle

from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

maxPages = 1
reviews = []
baseurl = 'http://www.skincaretalk.com/{}'
skincareviewurl = 'http://www.skincaretalk.com/forum.php'
skincareFileName = 'skincaretalk.pickle'

def scrapeReviewsSkinCareTalk(pageNo, readThread = False):
    url = skincareviewurl #.format(pageNo)
    print("calling:",url)
    #requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url)
    with open('dump.txt','w') as f:
        f.write(response.text)
    return
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


getAllReviews(True)

for review in reviews:
    print(review)

print('found these reviews:',len(reviews))

