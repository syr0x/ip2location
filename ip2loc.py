import requests
from bs4 import BeautifulSoup
import sys

if len(sys.argv) != 2:
    print('Usage:' + sys.argv[0] + '<country>')
    sys.exit(1)

country = sys.argv[1]

def parsePage(link):
    # Create a BeautifulSoup object
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup


# def runMasscan(iprange):
#     print("masscan --range "+ ip1 +" - ")



def getLines(soupObj):
    tableContent = soupObj.find("table")
    for td in tableContent.findAll('tr'):
        key = td.get_text()
        print(key)
    return



def countryLink():
    link = ('https://lite.ip2location.com//'+ str(country).lower() + '-ip-address-ranges')
    print('[+] Opened '+ country)
    print('-' * 40)
    print('[+] STARTING CRAWLING')
    return link



if __name__ == "__main__":
    print('\n[+] STARTING')
    link = countryLink()
    soupObj = parsePage(link)
    getLines(soupObj)



