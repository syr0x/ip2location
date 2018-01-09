import requests
from bs4 import BeautifulSoup
import sys
import masscan
import pycountry as pc

if len(sys.argv) != 3:
    print('Usage:' + sys.argv[0] + '<country>' + ' <ipverse || ip2location>')
    sys.exit(1)

country = sys.argv[1]
source = sys.argv[2]


def parsePage(link):
    # Create a BeautifulSoup object
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup


# def runMasscan(iprange):
#     masscan.
#     print("masscan --range "+ ip1 +" - ")


def getLines(soupObj):
    tableContent = soupObj.find("table")
    for td in tableContent.findChildren('tr'):
        key = td.get_text()
#        runMasscan(key)
    return


def countryLink(source):
    if source.lower() == 'ip2location':
        link = ('https://lite.ip2location.com//' + str(country).lower() + '-ip-address-ranges')
    else:
        code = pc.countries.get(name=country.title()).alpha_2
        link = ('http://ipverse.net/ipblocks/data/countries/'+ str(code).lower() + '.zone')
    print('[+] Opened ' + country)
    print('-' * 40)
    print('[+] STARTING CRAWLING')
    return link


if __name__ == "__main__":
    print('\n[+] STARTING')
    link = countryLink(source)
    soupObj = parsePage(link)
    getLines(soupObj)
