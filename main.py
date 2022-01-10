import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("screen1.ui", self)
        self.pushButton.clicked.connect(self.gotoScreen2)


    def gotoScreen2(self):
        widget.addWidget(screen2)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Screen2(QDialog):
    def __init__(self):
        super(Screen2, self).__init__()
        loadUi("screen2.ui",self)
        self.pushButton.clicked.connect(self.gotoMainWindow)


    def gotoMainWindow(self):
        mainwindow = MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)


app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
mainwindow = MainWindow()
screen2 = Screen2()

widget.addWidget(mainwindow)

widget.setFixedHeight(300)
widget.setFixedWidth(400)
widget.show()


try:
    sys.exit(app.exec_())
except:
    print('Exiting')