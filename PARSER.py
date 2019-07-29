import requests
from bs4 import BeautifulSoup as bs
from PyQt5 import QtWidgets
import  sys
import csv
import os

class ExampleApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        vbox = QtWidgets.QVBoxLayout()
        hbox = QtWidgets.QHBoxLayout()
        self.text2 = QtWidgets.QLabel("")
        self.line = QtWidgets.QLineEdit()
        self.but = QtWidgets.QPushButton("GO")
        self.text = QtWidgets.QLabel("Ввидите название товара для поиска минимальной стоимости")
        self.apt = QtWidgets.QCheckBox("365")
        self.goz = QtWidgets.QCheckBox("гоздрав")
        self.but.clicked.connect(self.run)
        hbox.addWidget(self.apt)
        hbox.addWidget(self.goz)
        vbox.addWidget(self.text)
        vbox.addWidget(self.line)
        vbox.addLayout(hbox)
        vbox.addWidget(self.but)
        vbox.addWidget(self.text2)
        self.setLayout(vbox)
        self.setGeometry(700, 450, 250, 50)
        self.show()


    def run(self):
        self.text2.setText("")
        try:
            os.remove("all.csv")
        except:
            pass

        if self.apt.isChecked():
            self.apteka666()
        if self.goz.isChecked():
            self.gozdrav()



    def apteka666(self):
        self.text = self.line.text()
        self.headers = {'accept': '*/*',
                        'user-agent': 'Mozilla/5.0(X11;Linux x86_64...)Geco/20100101 Firefox/60.0'}
        self.base_url = 'https://apteka366.ru/search/?text={}'.format(self.text)
        session = requests.session()
        request = session.get(self.base_url, headers=self.headers)
        if request.status_code == 200:
            soup = bs(request.content, 'lxml')

            """ТОВАР"""
            divs = soup.find_all('div', attrs={'class': 'c-prod-item__title'})
            divs1 = []
            for div in divs:
                div = div.text[25:]
                divs1.append(div)
            print(divs1)

            """ЦЕНА"""
            divs = soup.find_all('span', attrs={'class': 'b-price'})
            divs2 = []
            for div in divs:
                x = div.text[16:].split(" ")[0]
                if "," in x:
                    x = x.split(",")[0]
                    divs2.append(x)
                else:
                    divs2.append(x)

            print(divs2)


            with open("all.csv", "a", encoding='utf8') as file:
                text = csv.writer(file)
                text.writerow(("товар","цена","ссылка"))
                for i in range(len(divs1)):
                    text.writerow((divs1[i],divs2[i],'https://apteka366.ru/search/?text={}'.format(self.text)))

            mini = int(divs2[0])
            ind = 0
            for i in range(len(divs2)):
                print((int(divs2[i]), mini))
                if int(divs2[i]) < mini:
                    mini = int(divs2[i])
                    ind = i

            self.text2.setText("{} рублей 36,6".format(mini))

            """
            msg = QtWidgets.QMessageBox.question(self, 'Цена', "Минимальная цена {}\n{}\nоткрыть таблицу?".format(mini,self.base_url.split("/")[2]), QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if msg == QtWidgets.QMessageBox.Yes:
                os.startfile(r'all.csv')
            """


        else:
            print('ERROR')




    def gozdrav(self):
        self.text = self.line.text()
        self.headers = {'accept': '*/*',
                        'user-agent': 'Mozilla/5.0(X11;Linux x86_64...)Geco/20100101 Firefox/60.0'}
        self.base_url = 'https://gorzdrav.org/search/?text={}'.format(self.text)
        session = requests.session()
        request = session.get(self.base_url, headers=self.headers)
        if request.status_code == 200:
            soup = bs(request.content, 'lxml')

            """ТОВАР"""
            divs = soup.find_all('div', attrs={'class': 'c-prod-item__title'})
            divs1 = []
            for div in divs:
                if self.text in div.text:
                    div = div.text[25:]
                    divs1.append(div)
            print(divs1)

            """ЦЕНА"""
            divs = soup.find_all('meta', attrs={'itemprop': 'price'})
            divs2 = []
            for div in divs:
                x = str(div)[15:].split('"')[0]
                if "." in x:
                    x = x.split(".")[0]
                    divs2.append(x)
                else:
                    divs2.append(x)
            print(divs2)


            with open("all.csv", "a", encoding='utf8') as file:
                text = csv.writer(file)
                text.writerow(("товар", "цена", "ссылка"))
                for i in range(len(divs1)):
                    text.writerow((divs1[i], divs2[i], 'https://gorzdrav.org/search/?text={}'.format(self.text)))

                mini = int(divs2[0])
                ind = 0
                for i in range(len(divs2)):
                    print((int(divs2[i]), mini))
                    if int(divs2[i]) < mini:
                        mini = int(divs2[i])
                        ind = i

                if int(self.text2.text().split(" ")[0]) > mini:
                    self.text2.setText("{} рублей гоздрав".format(mini))

                """
                msg = QtWidgets.QMessageBox.question(self, 'Цена',"Минимальная цена {}\n{}\nоткрыть таблицу?".format(mini, self.base_url.split("/")[2]), QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                if msg == QtWidgets.QMessageBox.Yes:
                    os.startfile(r'all.csv')
                """

        else:
            print('ERROR')


app = QtWidgets.QApplication(sys.argv)
window = ExampleApp()
window.show()
app.exec_()