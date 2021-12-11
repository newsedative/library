import sys
import sqlite3
from PyQt5 import uic, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mainScr.ui', self)
        self.pushButton.clicked.connect(self.findBook)
        self.comboBox.activated[str].connect(self.onChanged)
        self.text1 = 'Aвтор'

    def findBook(self):
        t = self.lineEdit.text()
        con = sqlite3.connect('books.db')
        cur = con.cursor()
        if self.text1 == 'Aвтор':
            self.result = cur.execute(f'SELECT * FROM books WHERE author like "{f"{t}%"}"').fetchall()
        else:
            self.result = cur.execute(f'SELECT * FROM books WHERE bookName like "{f"{t}%"}"').fetchall()
        con.close()
        self.widget = QWidget()
        layout = QVBoxLayout(self)
        for i in range(len(self.result)):
            a = self.result[i][1]
            self.btn = QPushButton(a, self)
            self.btn.clicked.connect(self.info)
            layout.addWidget(self.btn)
        self.widget.setLayout(layout)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.widget)
        vLayout = QVBoxLayout(self)
        vLayout.addWidget(self.scrollArea)
        self.setLayout(vLayout)

    def info(self):
        book = QWidget.sender(self).text()
        n = ''
        for i in range(len(self.result)):
            if self.result[i][1] == book:
                n = self.result[i]
        try:
            self.new = SecondScr(n)
            self.new.show()
        except Exception as e:
            print(e)

    def onChanged(self, text):
        self.text1 = text


class SecondScr(QMainWindow):
    def __init__(self, n):
        super().__init__()
        self.n = n
        uic.loadUi('findScr.ui', self)
        self.label_name.setText(self.n[1])
        self.label_autor.setText(self.n[2])
        self.label_year.setText(str(self.n[3]))
        self.label_type.setText(self.n[4])
        if self.n[-1]:
            self.pixmap = QPixmap(self.n[-1])
        else:
            self.pixmap = QPixmap('img/none_img.jpg')
        self.label_img.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())