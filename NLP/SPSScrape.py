
import requests
from requests_ntlm import HttpNtlmAuth
import getpass
from bs4 import BeautifulSoup
import html


url = "http://amersp1.lubrizol.com/sites/IS/SiteDirectory/ADETeam/blog/_api/web/lists/GetByTitle('Posts')/items"

print('test scripts...')

USERNAME = 'lubrizol\\dawa'
response = requests.get(url, auth=HttpNtlmAuth(USERNAME, getpass.getpass()))

#print(html.unescape(response.text))

soup = BeautifulSoup(html.unescape(response.text), 'lxml')
divs = soup.findAll('d', {'':'Title'})

for div in divs:
    print(div.text)


