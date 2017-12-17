from bs4 import BeautifulSoup
import re
import requests
import csv
import urllib
import os
urll = "https://www.sec.gov/cgi-bin/browse-edgar?CIK="
tickerlist = []
tuplist = []
def main(filename):
    with open(filename, 'r') as fin:
        reader = csv.reader(fin)
        for row in reader:
            tickerlist.append(row[0])
    return tickerlist
def scraper2(ticker):
    urll2 = urll+str(ticker)
    req = urllib.request.Request(urll2)
    response = urllib.request.urlopen(req)
    bytess = response.read()
    text = bytess.decode()
    name = re.findall(r'<span class="companyName">(.+)<acronym title="Central Index Key">', text)
    sic = re.findall(r'SIC=([0-9]{4})', text)
    sector = re.findall(r' - (.+)<br />State', text)
    addr1 = re.findall(r'<div class="mailer">Mailing Address\n +<span class="mailerAddress">(.+)<\/span>\n +<span', text)
    addr2 = re.findall(r'<\/span>\n +<span class="mailerAddress">(.+)<\/span>\n +<span', text)
    city = re.findall(r'<span class="mailerAddress">\n([A-Z]+.+[A-Z]+) [A-Z]{2} .+<\/span>\n', text)
    state = re.findall(r'<span class="mailerAddress">\n.+ ([A-Z]{2}) .+<\/span>\n', text)
    zipp = re.findall(r'<span class="mailerAddress">\n.+[A-Z]{2} (.+) .+<\/span>\n', text)
    if len(city) > 0:
        city= city[0]
    if len(city) == 0:
        city = re.findall(r'<span class="mailerAddress">\n([A-Z]+).+<\/span>', text)
        city = city[0]
    if len(state) > 0:
        state = state[0]
    else:
        state = re.findall(r'<span class="mailerAddress">\n[A-Z]+ ([\w]{2}).+<\/span>', text)
        state = state[0]
    if len(zipp)>0:
        zipp = zipp[0].strip()
        if zipp == "":
            zipp = re.findall(r'<span class="mailerAddress">\n[A-Z]+ [\w]{2} (.+) +<\/span>', text)
            zipp = zipp[0].strip()
    name = name[0].strip()

    sic = sic[0]
    sector= sector[0]
    addr1 = addr1[0]
    if len(addr2) == 1:
        addr2 =""
    if len(addr2) == 2:
        addr2=addr2[1]
    if ticker == "CSCO":
        name = "\"CISCO SYSTEMS, INC.\""
    if ticker == "FB" or ticker =="GOOG":
        sector = "\"SERVICES-COMPUTER PROGRAMMING, DATA PROCESSING, ETC.\""
    if addr2 == []:
        addr2 = ""
    tup = (ticker, name, sic, sector, addr1, addr2, city, state, zipp)
    return(tup)
def writer(outfile):
    outf = open(outfile, 'w')
    introstr = "Ticker,Name,SIC,Sector,Addr1,Addr2,City,State,Zip\n"
    outf.write(introstr)
    first=""
    for i in list(tuplist[0]):
        first += str(i)+","
    outf.write(first+"\n")
    outf.close()
    for i in tuplist[1:]:
        x = ""
        for z in list(i):
            x += str(z)+","
        outf = open(outfile, 'a')
        outf.write(x+"\n")
        outf.close()
if __name__ == '__main__':
    import sys
    main(sys.argv[1])
    for i in tickerlist:
        tupa = scraper2(i)
        tuplist.append(tupa)
    writer(sys.argv[2])
    han = open(sys.argv[2], "r")
    masterl = han.readlines()
    final = []
    for line in masterl:
        line = line.replace("&amp;", "&")
        line = line.replace(",\n", "\n")
        final.append(line)
    han.close()
    han = open(sys.argv[2], "w")
    for item in final:
        han.write(item)
    han.close()
