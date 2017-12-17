import datetime as dt
import csv

def dates(strg):
    xv = dt.datetime.strptime(strg, "%Y-%m-%d")
    #xv = xv.strftime("%Y-%m-%d")
    return strg
    #creates a datetime obj when the date is inputted as a string in the m/d/y format
def passed_dates(strg):
    xv = dt.datetime.strptime(strg, "%Y-%m-%d")
    xv = xv.strftime("%Y-%m-%d")
    # creates a datetime obj when the date is inputted as a string in the y-m-d
    return strg

class StockData:
    def __init__(self, list):
        self.open_price = float(list[1])
        self.high = float(list[2])
        self.low = float(list[3])
        self.close = float(list[4])
        self.adj_close = float(list[5])
        self.volume = int(list[6])
    def __lt__(self, other):
        if self.adj_close < other.adj_close:
            return True
        else:
            return False

class Company:
    def __init__(self, symbol, name=None, sector=None):
        self.symbol = str(symbol)
        self.name = str(name)
        self.sector = str(sector)
        self.stock_data = {}
    def __str__(self):
        return (self.name + " (" + self.symbol + ")" )
    def __repr__(self):
        return f"<Company: name={self.name}, symbol={self.symbol}, sector={self.sector}"
    def last_date(self):
        filename = str(self.symbol)+".csv"
        myfile = open(filename, "r")
        lines = myfile.readlines()
        lastdate = lines[(len(lines)-1)][0:10]
        myfile.close()
        return str(lastdate)
    def populate(self):
        filename = str(self.symbol)+".csv"
        with open(filename) as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                self.stock_data[dates(row[0])] = StockData(row)
    def performance(self, firstdate=None, enddate=None):
        if firstdate==None and enddate == None:
            with open(self.symbol+".csv") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    firstt = dates(row[0])
                    break
                #for row in reader:
                    #final =  dates(row[0])
                final = self.last_date()
                    #break need to figure out how to get the last date in the csv file
            performance = (100*((self.stock_data[final].adj_close)/(self.stock_data[firstt].open_price)) - 100)
            return ("Stock performance of "+str(self)+" from "+str(firstt)+" to "+str(final)+": "+str(round(performance,1))+"%.")

        if firstdate!=None and enddate == None: #firstdate specified
            firstt = (firstdate)
            final = self.last_date()
            self.populate()
            if firstt in self.stock_data.keys():
                performance = (100*((self.stock_data[final].adj_close)/(self.stock_data[firstt].open_price)) - 100)
                return ("Stock performance of "+str(self)+" from "+str(firstt)+" to "+str(final)+": "+str(round(performance,1))+"%.")
            if firstt not in self.stock_data.keys():
                newfirst = firstt.split("-")
                newfirst[2] = int(newfirst[2])
                newfirst[2] += 1
                if len(str(newfirst[2]))==1:
                    newfirst[2] = str("0"+ str(newfirst[2]))
                x = "-".join(newfirst)
                if x in self.stock_data.keys():
                    performance = (100*((self.stock_data[final].adj_close)/(self.stock_data[x].open_price)) - 100)
                    return ("Stock performance of "+str(self)+" from "+str(x)+" to "+str(final)+": "+str(round(performance,1))+"%.")
                if x not in self.stock_data.keys():
                    newx = x.split("-")
                    newx[2] = int(newx[2])
                    newx[2] += 2
                    if len(str(newx[2]))==1:
                        newx[2] = str("0"+ str(newx[2]))
                    z = "-".join(newx)
                    performance = (100*((self.stock_data[final].adj_close)/(self.stock_data[z].open_price)) - 100)
                    return ("Stock performance of "+str(self)+" from "+str(z)+" to "+str(final)+": "+str(round(performance,1))+"%.")

        if firstdate!=None and enddate!=None: #start and end date specified
            firstt = firstdate
            final = enddate
            if firstt in self.stock_data.keys() and final in self.stock_data.keys():
                performance = (100*((self.stock_data[final].adj_close)/(self.stock_data[firstt].open_price)) - 100)
                return ("Stock performance of "+str(self)+" from "+str(firstt)+" to "+str(final)+": "+str(round(performance,1))+"%.")
            if firstt not in self.stock_data.keys() and final in self.stock_data.keys():
                newfirst = firstt.split("-")
                newfirst[2] = int(newfirst[2])
                newfirst[2] += 1
                if len(str(newfirst[2]))==1:
                    newfirst[2] = str("0"+ str(newfirst[2]))
                x = "-".join(newfirst)
                if x in self.stock_data.keys():
                    performance = (100*((self.stock_data[final].adj_close)/(self.stock_data[x].open_price)) - 100)
                    return ("Stock performance of "+str(self)+" from "+str(x)+" to "+str(final)+": "+str(round(performance,1))+"%.")
                if x not in self.stock_data.keys():
                    newx = x.split("-")
                    newx[2] = int(newx[2])
                    newx[2] += 1
                    if len(str(newx[2]))==1:
                        newx[2] = str("0"+ str(newx[2]))
                    z = "-".join(newx)
                    performance = (100*((self.stock_data[final].adj_close)/(self.stock_data[z].open_price)) - 100)
                    return ("Stock performance of "+str(self)+" from "+str(z)+" to "+str(final)+": "+str(round(performance,1))+"%.")

            if final not in self.stock_data.keys() and firstt in self.stock_data.keys():
                newlast = final.split("-")
                newlast[2] = int(newlast[2])
                newlast[2] += 2
                if len(str(newlast[2]))==1:
                    newlast[2] = str("0"+ str(newlast[2]))
                y = "-".join(newlast)
                performance = (100*((self.stock_data[y].adj_close)/(self.stock_data[firstt].open_price)) - 100)
                return ("Stock performance of "+str(self)+" from "+str(firstt)+" to "+str(y)+": "+str(round(performance,1))+"%.")

def main(symbol, firstdate=None, enddate=None):
    obj = Company(symbol)
    filename = str(symbol)+".csv"
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            obj.stock_data[dates(row[0])] = StockData(row)
            #Up to this point, the dic is fully populated
    print(obj.performance(firstdate, enddate),sep=' ',end='')
if __name__ == '__main__':
    import sys
    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    if len(sys.argv) == 2:
        main(sys.argv[1])
