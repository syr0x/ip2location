import requests
from bs4 import BeautifulSoup
import sys

if len(sys.argv) != 1:
    print('Usage:' + sys.argv[0] + '<country>')
    sys.exit(1)

country = sys.argv[1]

page = requests.get('https://lite.ip2location.com/ip-address-ranges-by-country')

# Create a BeautifulSoup object
soup = BeautifulSoup(page.text, 'html.parser')
countryList = soup.find(class_='content-page')
countryName = countryList.find_all('li')

for country in countryName:
    names = country.contents[2]
    links = 'https://lite.ip2location.com/' + str(country.get('href'))
    print(names)
    print(links)
