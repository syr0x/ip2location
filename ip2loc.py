import requests
from bs4 import BeautifulSoup
import sys
import subprocess
import pycountry as pc
import multiprocessing
import time
import glob
import os
import tqdm

if len(sys.argv) != 4:
    print('Usage:' + sys.argv[0] + ' <country>' + ' <ipverse||ip2location> ' + '<process>')
    sys.exit(1)

# set args
country = sys.argv[1]
source = sys.argv[2]
processNum = sys.argv[3]

# Function run by worker processes
def runMasscan(iprange):
    savedFile = str(iprange)+'.txt'
    process = subprocess.Popen(["masscan","-p22", str(iprange), "--rate=4000", '-oG', savedFile], stdout=subprocess.PIPE)
    #output, error = process.communicate()
    status = process.wait()
    return status


def worker(work, function, return_dict):
    while not work.empty():
        try:
            candidate = work.get()
        except:
            continue
        if candidate:
            ret = function(candidate)
            if ret:
                return_dict[candidate] = ret


class Multiprocessing:
    @staticmethod
    # Create queues
    def main(workers, work_set, my_function):
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        work = manager.Queue()

        # Submit tasks
        for w in work_set:
            work.put(w)

        pbar = tqdm.tqdm(total=work.qsize())
        processes = []
        for unused_index in range(workers):
            process = multiprocessing.Process(target=worker, args=(work, my_function, return_dict,))
            processes.append(process)
            process.start()

        total = work.qsize() + 1
        while not work.empty():
            if total != work.qsize():
                pbar.update(1)
                time.sleep(0.1)
                total = work.qsize()
            continue


        alive_process = True
        while alive_process:
            for process in processes:
                process.terminate()
                if process.is_alive():
                    alive_process = True
                    continue
                alive_process = False
        return return_dict


def copyFile():
    os.makedirs(country, exist_ok=True)
    outFilename = (country + "//" + country + '.txt')
    with open(outFilename, 'wb') as outfile:
        for filename in glob.glob('*.txt'):
            with open(filename, 'rb') as readfile:
                for line in readfile:
                    line = (line.strip().decode()) + "\n"
                    outfile.write(line.encode())
    return outFilename




def runUpdate(path):
    os.system("rm *.txt -f")
    print("[+] FINISH PARSE COUNTRY FILES ")
    os.system("grep -oP '(?<=Host: )\S*' "+ path +".txt > mfu.txt")
    print("[+] FINISHED RUN ./UPDATE OR ./GO TO BRUTE THEM --------------")
    return False


def getLines(soupObj):
    ipRanges = []
    try:
        if source == 'ip2location':
            tableContent = soupObj.find("table")
            for td in tableContent.findChildren('tr'):
                key = td.get_text().split('\n')
                if key[1] == "Begin IP Address":
                    continue
                elif int(key[3].replace(',', '')) > 256:
                    key = (key[1] + "-" + key[2])
                    ipRanges.append(key)

        else:
            content = soupObj.get_text()
            for s in content.splitlines():
                if s.strip().startswith('#'):
                    pass
                else:
                    ipRanges.append(s.strip())

        return ipRanges

    except Exception as inst:
        print(inst)


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
    ret = Multiprocessing.main(int(processNum), ipRanges, runMasscan)
    out = copyFile()
    runUpdate(out)
