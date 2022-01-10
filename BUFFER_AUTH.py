# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import serial.tools.list_ports
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout, QMessageBox
import sys
from MAIN_WINDOW import MAIN_window
from GLOBAL_FUNCTIONS import create_modbus_connection, serial_ports, message_box_info


class AUTH_window(QtWidgets.QDialog):
    def __init__(self):
        super(AUTH_window, self).__init__()
        loadUi("AUTH.ui", self)

        self.label_only_COM_FIRST = self.findChild(QtWidgets.QLabel, 'label_only_COM_FIRST')
        self.comboBox_COM_FIRST = self.findChild(QtWidgets.QComboBox, 'comboBox_COM_FIRST')
        self.label_COM_FIRST = self.findChild(QtWidgets.QLabel, 'label_COM_FIRST')

        self.label_only_COM_SECOND = self.findChild(QtWidgets.QLabel, 'label_only_COM_SECOND')
        self.comboBox_COM_SECOND = self.findChild(QtWidgets.QComboBox, 'comboBox_COM_SECOND')
        self.label_COM_SECOND = self.findChild(QtWidgets.QLabel, 'label_COM_SECOND')

        self.pushButton = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.available_ports = serial_ports()

        self.comboBox_COM_FIRST.addItems(self.available_ports)
        self.comboBox_COM_SECOND.addItems(self.available_ports)

        self.comboBox_COM_FIRST.currentTextChanged.connect(self.combo_selected)
        self.comboBox_COM_SECOND.currentTextChanged.connect(self.combo_selected)
        self.pushButton.clicked.connect(self.open_main_window)

        # self.setGeometry(200, 200, 700, 250)
        self.setWindowTitle("Дальномер")

        self.main_window = MAIN_window()

    def open_main_window(self):

        current_COM_FIRST, current_COM_SECOND = self.current_com()
        print('Current COMS', current_COM_FIRST, current_COM_SECOND)

        try:
            connection1 = create_modbus_connection(current_COM_FIRST, 1, 9600, 8, 1, 1)
            print(connection1.instrument.read_float(registeraddress=0, functioncode=3, number_of_registers=2, ))

            connection2 = create_modbus_connection(current_COM_SECOND, 1, 9600, 8, 1, 1)
            print(connection2.instrument.read_float(registeraddress=0, functioncode=3, number_of_registers=2, ))

            self.main_window.set_COM_value(current_COM_FIRST, current_COM_SECOND)
            self.main_window.show()
            self.hide()

        except:
            message_box_info(1)

    def combo_selected(self):
        item1 = self.comboBox_COM_FIRST.currentText()
        item2 = self.comboBox_COM_SECOND.currentText()
        print(type(item1), item1)
        print(type(item2), item2)
        self.label_COM_FIRST.setText(item1)
        self.label_COM_SECOND.setText(item2)

    def current_com(self):
        print(self.comboBox_COM_FIRST.currentText(), self.comboBox_COM_SECOND.currentText())
        return self.comboBox_COM_FIRST.currentText(), self.comboBox_COM_SECOND.currentText()


app = QApplication(sys.argv)
AUTHwindow = AUTH_window()
AUTHwindow.show()
sys.exit(app.exec_())