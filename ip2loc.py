import requests
from bs4 import BeautifulSoup
import sys
import masscan
import subprocess
import pycountry as pc
from multiprocessing import Process, Queue


if len(sys.argv) != 3:
    print('Usage:' + sys.argv[0] + '<country>' + ' <ipverse || ip2location>')
    sys.exit(1)

country = sys.argv[1]
source = sys.argv[2]

def worker(input, output):
    print(input())
    print(output)


def runMasscan(ipranges):
    print('[+] STARTING MASSCAN')
    ipranges = ipranges.split()
    processNum = 5
    massTask = 'masscan --range'

    # Create queues
    taskQueue = Queue()
    doneQueue = Queue()

    # Submit tasks
    for task in massTask:
        taskQueue.put(task)

    # Start worker processes
    for i in range(processNum):
        Process(target=worker, args=(task_queue, done_queue)).start()

    # Get and print results

def getLines(soupObj):
    ipRanges = []
    if source == 'ip2location':
        tableContent = soupObj.find("table")
        for td in tableContent.findChildren('tr'):
            key = td.get_text()
            ipRanges.append(key)
    else:
        content = soupObj.get_text()
        for s in content.splitlines():
            if s.strip().startswith('#'):
                pass
            else:
                ipRanges.append(s.strip())
    return ipRanges

def parsePage(link):
    # Create a BeautifulSoup object
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup


def countryLink(source):
    if source.lower() == 'ip2location':
        link = ('https://lite.ip2location.com//' + str(country).lower() + '-ip-address-ranges')
        print('[+] Ip2Location setup')
    else:
        code = pc.countries.get(name=country.title()).alpha_2
        link = ('http://ipverse.net/ipblocks/data/countries/'+ str(code).lower() + '.zone')
        print('[+] IpVerse setup')
    print('[+] Opened ' + country.title())
    print('-' * 40)
    print('[+] STARTING CRAWLING')
    return link


if __name__ == "__main__":
    print('\n[+] STARTING')
    link = countryLink(source)
    soupObj = parsePage(link)
    ipRanges = getLines(soupObj)
    runMasscan(ipRanges)
