import requests
from bs4 import BeautifulSoup

def getAllPosts(url, links):
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text,'lxml')
    for a in soup.findAll('a'):
        try:
            url =a['href']
            title =a['title']
            if title == "Older Posts":
                print(title, url)
                links.append(url)
                getAllPosts(url, links)
        except:
            title=""
    return


def getText(testUrl):
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text,'lxml')
    myDivs = soup.findAll("div",{"class":"post-body"})

    posts =[]
    for div in myDivs:
        posts+=map(lambda p:p.text.encode('ascii',errors.replace("?"," "),div.findAll("li")))
    return posts

blogUrl = "http://doxydonkey.blogspot.co.uk/"
links = []
getAllPosts(blogUrl, links)

posts = []
for link in links:
    posts+=getText(link)
    
print(posts)
