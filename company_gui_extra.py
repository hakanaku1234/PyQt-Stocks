#GTID 903246579
#gquintas3
#Gabriel Quintas

import sqlite3
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from PyQt5.QtCore import (
    Qt,
    QAbstractTableModel,
    QVariant
)
from PyQt5.QtSql import (
    QSqlDatabase,
    QSqlQuery,
    QSqlQueryModel
)


class popup(QWidget):  ## Company info
    def __init__(self):
        QWidget.__init__(self)
class popup2(QWidget):  ## Sector popup
    def __init__(self):
        QWidget.__init__(self)
class popup3(QWidget):   #Stock price popup
    def __init__(self):
        QWidget.__init__(self)
class popup4(QWidget):   ##Company editing
    def __init__(self):
        QWidget.__init__(self)
class popup5(QWidget):   ## add a company button
    def __init__(self):
        QWidget.__init__(self)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("SQLite Database Browser")

        #SET WINDOW GEOMETRY
        left, top, width, height = 200, 200, 500, 100
        self.setGeometry(left, top, width, height)

        #CREATE BUTTONS
        self.btn3 = QPushButton("Stock Prices",self)

        #CONNECT BUTTONS
        self.acb = QPushButton("New Company...", self)
        self.acb.clicked.connect(self.addcomp)

        #Layout Creation
        self.btn3.clicked.connect(self.btn3f)
        self.buttons = QHBoxLayout()
        self.buttons2 = QHBoxLayout()
        self.buttons3 = QHBoxLayout()
        #self.buttons.addWidget(btn1)

        ### Connecting to DB to fetch company names
        conn = sqlite3.connect('company.db')
        curs = conn.cursor()
        curs.execute("select name from sqlite_master where type='table'")
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('company.db')
        db.open()

        # Create ComboBox for Company
        self.comboBox = QComboBox(self)
        self.comboBox.addItem("")

        ## Adds the company names to the ComboBox ######################
        curs.execute("SELECT * FROM COMPANY")
        for data in curs:
            compn = data[1]
            self.comboBox.addItem(str(compn))

        # Add the Show button next to Company Drop Down
        self.btn4 = QPushButton("Show", self)
        self.btn4.clicked.connect(self.showcompany)
        self.w = None
        self.btn4.setEnabled(False)

        #Enable SHow button when user selects a company name
        self.comboBox.activated[str].connect(self.turnoncompany)
        # Send the company name to the showcompany function
        #self.comboBox.activated[str].connect(self.showcompany)

        # Create ComboBox for Sector
        self.comboBox2 = QComboBox(self)
        self.comboBox2.addItem("")

        ## Adds the Sector names to the ComboBox ######################
        curs.execute("SELECT * FROM SECTOR")
        for data in curs:
            sectorn = data[1]
            self.comboBox2.addItem(str(sectorn))

        # Add the Show button next to Sector Drop Down
        self.btn5 = QPushButton("Show", self)
        self.btn5.clicked.connect(self.showsector)
        self.btn5.setEnabled(False)

        #Enable SHow button when user selects a Sector name
        self.comboBox2.activated[str].connect(self.turnonsector)

        self.buttons.addWidget(self.comboBox)
        self.buttons.addWidget(self.btn4)
        self.buttons.addWidget(self.acb)
        self.buttons2.addWidget(self.comboBox2)
        self.buttons2.addWidget(self.btn5)
        self.buttons3.addWidget(self.btn3)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.buttons)
        self.vbox.addLayout(self.buttons2)
        self.vbox.addLayout(self.buttons3)
        #self.setLayout(vbox)

        screen = QWidget()
        screen.setLayout(self.vbox)
        self.setCentralWidget(screen)

    def turnoncompany(self):
        if self.comboBox.currentText() != "":
            self.btn4.setEnabled(True)
        else:
            self.btn4.setEnabled(False)
    def turnonsector(self):
        if self.comboBox2.currentText() != "":
            self.btn5.setEnabled(True)
        else:
            self.btn5.setEnabled(False)

    def showcompany(self, textt):
        #Company Name
        company_name = self.comboBox.currentText()

        #Ticker & other stuff
        conn = sqlite3.connect('company.db')
        curs = conn.cursor()
        curs.execute("select name from sqlite_master where type='table'")
        # db = QSqlDatabase.addDatabase('QSQLITE')
        # db.setDatabaseName('company.db')
        # db.open()
        curs.execute(f"SELECT * from company where name = \'{company_name}\'")
        for data in curs:
            ticker = data[0]
            sic = data[2]
            addr = str(data[3]+", " + data[4]+", " +data[5]+", " +data[6]+", " +data[7])

        curs.execute(f"SELECT * from company join sector using(sic) where company.name = \'{company_name}\'")
        for data in curs:
            sector_name = data[8]

        #Adding the text to the popup
        q1 = QLabel()
        q1.setText("Company Name: ")
        w1 = QLabel()
        w1.setText(str(company_name))

        line1 = QHBoxLayout()
        line1.addWidget(q1)
        line1.addWidget(w1)

        q2 = QLabel()
        q2.setText("Ticker Symbol: ")
        w2 = QLabel()
        w2.setText(str(ticker))

        line2 = QHBoxLayout()
        line2.addWidget(q2)
        line2.addWidget(w2)

        q3 = QLabel()
        q3.setText("Sector: ")
        w3 = QLabel()
        w3.setText(str(sector_name)+" ("+str(sic)+")")

        line3 = QHBoxLayout()
        line3.addWidget(q3)
        line3.addWidget(w3)

        q4 = QLabel()
        q4.setText("Address: ")
        w4 = QLabel()
        w4.setText(str(addr))

        line4 = QHBoxLayout()
        line4.addWidget(q4)
        line4.addWidget(w4)

        q5 = QLabel()
        q5.setText("Date,     Open,     High,     Low,     Close,     Adj. Close,     Volume")
        line5 = QHBoxLayout()
        line5.addWidget(q5)

        listw = QListWidget()
        curs.execute(f"SELECT * FROM COMPANY JOIN STOCK_PRICE USING(ticker) where company.name =\'{company_name}\'")
        for row in curs:
            item = str(str(row[8])+", "+str(row[9])+", "+str(row[10])+", "+str(row[11])+", "+str(row[12])+", "+str(row[13])+", "+str(row[14]))
            listw.addItem(item)

        line6 = QHBoxLayout()
        line6.addWidget(listw)

        line7 = QHBoxLayout()
        editbtn = QPushButton("Edit", self)
        editbtn.clicked.connect(self.editor)
        line7.addWidget(editbtn)

        content = QVBoxLayout()
        content.addLayout(line1)
        content.addLayout(line2)
        content.addLayout(line3)
        content.addLayout(line4)
        content.addLayout(line5)
        content.addLayout(line6)
        content.addLayout(line7)

        self.w = popup()
        self.w.setGeometry(800,200,400,500)
        self.w.setWindowTitle("Company Information")

        self.w.setLayout(content)
        self.w.show()

    def showsector(self):
        sector_name = self.comboBox2.currentText()

        conn = sqlite3.connect('company.db')
        curs = conn.cursor()
        curs.execute("select name from sqlite_master where type='table'")

        listv = QListWidget()
        curs.execute(f"select company.name,company.ticker from company join sector using(sic) where sector.name=\"{sector_name}\"")
        for row in curs:
            item = str(str(row[0])+", "+str(row[1]))
            listv.addItem(item)

        k6 = QLabel()
        k6.setText("Company Name,   Ticker")
        line5  = QHBoxLayout()
        line5.addWidget(k6)

        line6 = QHBoxLayout()
        line6.addWidget(listv)
        content = QVBoxLayout()
        content.addLayout(line5)
        content.addLayout(line6)
        self.v = popup2()
        self.v.setGeometry(200,350,400,200)
        self.v.setWindowTitle("Sector")
        self.v.setLayout(content)
        self.v.show()


    def editor(self):
        conn = sqlite3.connect('company.db')
        curs = conn.cursor()

        company_name = self.comboBox.currentText()

        line1 = QHBoxLayout()
        filler = QLabel()
        filler.setText("After applying changes to company, re-open the window to see changes. MUST SELECT AN ITEM FROM SECTOR!")
        line1.addWidget(filler)

        curs.execute(f"SELECT * FROM COMPANY WHERE NAME=\'{company_name}\'")
        for row in curs:
            ticker = row[0]
            addr1 = row[3]
            addr2 = row[4]
            city = row[5]
            state = row[6]
            zipp = row[7]

        line2 = QHBoxLayout()
        l2 = QLabel()
        l2.setText("Ticker:  ")
        line2.addWidget(l2)
        self.e2 = QLineEdit()
        self.e2.setText(ticker)
        line2.addWidget(self.e2)
        # e2.textChanged.connect(self.textc)
        #e2.setText(e2.text())

        line3 = QHBoxLayout()
        l3 = QLabel()
        l3.setText("Name:  ")
        line3.addWidget(l3)
        self.e3 = QLineEdit()
        self.e3.setText(company_name)
        line3.addWidget(self.e3)

        line4 = QHBoxLayout()
        l4 = QLabel()
        l4.setText("SIC:  ")
        line4.addWidget(l4)
        self.comboBox3 = QComboBox()
        self.comboBox3.addItem("")
        curs.execute("SELECT * FROM SECTOR")
        for data in curs:
            sicc = data[0]
            sectorn = data[1]
            self.comboBox3.addItem(str(sectorn)+" ("+str(sicc)+")")
        line4.addWidget(self.comboBox3)

        line5 = QHBoxLayout()
        l5 = QLabel()
        l5.setText("Address 1:  ")
        line5.addWidget(l5)
        self.e5 = QLineEdit()
        self.e5.setText(addr1)
        line5.addWidget(self.e5)

        line6 = QHBoxLayout()
        l6 = QLabel()
        l6.setText("Address 2:  ")
        line6.addWidget(l6)
        self.e6 = QLineEdit()
        self.e6.setText(addr2)
        line6.addWidget(self.e6)

        line7 = QHBoxLayout()
        l7 = QLabel()
        l7.setText("City:  ")
        line7.addWidget(l7)
        self.e7 = QLineEdit()
        self.e7.setText(city)
        line7.addWidget(self.e7)

        line8 = QHBoxLayout()
        l8 = QLabel()
        l8.setText("State:  ")
        line8.addWidget(l8)
        self.e8 = QLineEdit()
        self.e8.setText(state)
        line8.addWidget(self.e8)

        line9 = QHBoxLayout()
        l9 = QLabel()
        l9.setText("Zip:  ")
        line9.addWidget(l9)
        self.e9 = QLineEdit()
        self.e9.setText(zipp)
        line9.addWidget(self.e9)

        line10 = QHBoxLayout()
        okbtn = QPushButton("Ok",self)
        cancel = QPushButton("Cancel", self)
        okbtn.clicked.connect(self.okc)
        cancel.clicked.connect(self.canc)
        line10.addWidget(okbtn)
        line10.addWidget(cancel)
        # Need to add the OK and Cancel Buttons

        content = QVBoxLayout()
        content.addLayout(line1)
        content.addLayout(line2)
        content.addLayout(line3)
        content.addLayout(line4)
        content.addLayout(line5)
        content.addLayout(line6)
        content.addLayout(line7)
        content.addLayout(line8)
        content.addLayout(line9)
        content.addLayout(line10)
        self.y = popup4()
        self.y.setGeometry(800,350,400,200)
        self.y.setWindowTitle("Company Editor")
        self.y.setLayout(content)
        self.y.show()

    def okc(self): # if user clicks ok, retrieve text from QLINesEdits and commit to the DB
        company_name = self.comboBox.currentText()
        ticker = self.e2.text()
        name = self.e3.text()
        sic = self.comboBox3.currentText()[len(self.comboBox3.currentText())-5:len(self.comboBox3.currentText())-1]
        addr1 = self.e5.text()
        addr2 = self.e6.text()
        city = self.e7.text()
        state = self.e8.text()
        zipp = self.e9.text()

        conn = sqlite3.connect('company.db')
        curs = conn.cursor()

        curs.execute(f"UPDATE COMPANY SET ticker=\'{ticker}\', sic=\'{sic}\', addr1=\'{addr1}\',  addr2=\'{addr2}\',  city=\'{city}\',  state=\'{state}\',  zip=\'{zipp}\', name=\'{name}\' where name=\'{company_name}\'")
        conn.commit()

    def canc(self):
        self.y.close()

    def addcomp(self):
        pass

    def btn3f(self):
        conn = sqlite3.connect('company.db')
        curs = conn.cursor()

        curs.execute("select name from sqlite_master where type='table'")
        tabs = QTabWidget()

        table_name = 'stock_price'
        table_model = QSqlQueryModel()

        for i, column_data in enumerate(curs.description):
            table_model.setHeaderData(i, Qt.Horizontal, column_data[0])

        table_model.setQuery(f"select * from {table_name}")
        table_view = QTableView()
        table_view.setModel(table_model)
        tabs.addTab(table_view, table_name)

        screen = QWidget()
        content = QVBoxLayout()

        line1 = QHBoxLayout()
        line1.addWidget(tabs)

        content.addLayout(line1)

        self.k = popup3()
        self.k.setGeometry(800,350,400,200)
        self.k.setWindowTitle("Stock Prices")
        self.k.setLayout(content)
        self.k.show()

if __name__=='__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
