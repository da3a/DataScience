# https://coinmarketcap-nexuist.rhcloud.com/api/ltc
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json

baseUrl = 'https://coinmarketcap-nexuist.rhcloud.com/api/{}'


def getCurrentPrice(currency):
    url = baseUrl.format(currency)
    print('calling:' + url)
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url, verify=False)
    return json.loads(response.text)['price']['gbp']


print(getCurrentPrice('ltc'))

print(getCurrentPrice('eth'))






