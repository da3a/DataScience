import requests
#from requests_ntlm import HttpNtlmAuth
import pickle
import sys
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

maxPages = 1
reviews = []
baseurl = 'http://www.skincaretalk.com/{}'
skincareviewurl = baseurl.format('forumdisplay.php/5-Basic-Skin-Care/page{}')
skincareFileName = 'skincaretalk.pickle'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'}

def scrapeReviewsSkinCareTalk(pageNo, readThread = False):
    url = skincareviewurl.format(pageNo)
    print("calling:",url)
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(response.text,'lxml')
    for link in soup.findAll('a',attrs={'class':'title'}):     
        href = link.get('href')
        if href and readThread:
            #print(link.text) 
            print("calling inner:",baseurl.format(href))
            innerResponse = requests.get(baseurl.format(href),headers=headers,verify=False)
            soup = BeautifulSoup(innerResponse.text,'lxml')
            text = ""
            for divInner in soup.findAll('blockquote',attrs={'class': 'postcontent'}):
                if text == "":
                    text = "post:{} ".format(divInner.text)
                else:
                    text += "reply: {}".format(divInner.text)
            reviews.append(text)
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

with open('dump.txt','w') as f:
    for review in reviews:
        f.write(review)
        f.write("*"*50)


# for review in reviews:
#     print(review)



print('found these reviews:',len(reviews))

