import sys
import csv
import sqlite3

if __name__ == '__main__':
    filein = sys.argv[1]
    fileout = sys.argv[2]

conn = sqlite3.connect(str(fileout)) #fileout has been created but it's empty.
c = conn.cursor()

with open(filein,"r") as compfile:
    #complist = compfile.readlines()
    reader = csv.reader(compfile)
    reader = list(reader)[1:]

tickerlist = []

for linee in reader:
    ticker = linee[0]
    tickerlist.append(ticker)
    name = linee[1]
    sic = linee[2]
    sector = linee[3]
    addr1 = linee[4]
    addr2 = linee[5]
    city = linee[6]
    state = linee[7]
    zipp = linee[8].strip()
    params = (ticker, sic, name, addr1, addr2, city, state, zipp)
    c.execute("INSERT OR REPLACE INTO company VALUES(?, ?, ?, ?, ?, ?, ?, ?)", params)
    params2 = (sic, sector)
    c.execute("INSERT OR REPLACE INTO sector VALUES(?, ?)", params2)
conn.commit()

for ticker in tickerlist:
    try:
        with open(ticker+".csv","r") as stockfile:
            stocklines = stockfile.readlines()
            for line in stocklines[1:]:
                te = line.split(",")
                if len(te) == 7:
                    date = te[0]
                    openn = te[1]
                    high = te[2]
                    low = te[3]
                    close = te[4]
                    adjclose = te[5]
                    volume = te[6].strip()
                    params = (ticker, date, openn, high, low, close, adjclose, volume)
                    c.execute("INSERT OR IGNORE INTO stock_price VALUES(?, ?, ?, ?, ?,? ,?,?)", params)
        conn.commit()
    except:
        print(str(ticker)+" does not have stock data in the same directory!")

conn.close()
