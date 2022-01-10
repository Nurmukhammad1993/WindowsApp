# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import time

from PyQt5 import QtCore, QtGui, QtWidgets
import serial.tools.list_ports
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout, QMessageBox, QStyleFactory
import sys
from MAIN_WINDOW import MAIN_window
from GLOBAL_FUNCTIONS import create_modbus_connection, serial_ports, message_box_info



class AUTH_window(QtWidgets.QDialog):
    def __init__(self):
        super(AUTH_window, self).__init__()
        loadUi("AUTH.ui", self)

        self.label_only_COM_FIRST = self.findChild(QtWidgets.QLabel, 'label_only_COM_FIRST')
        self.label_COM_FIRST = self.findChild(QtWidgets.QLabel, 'label_COM_FIRST')
        self.label_only_COM_SECOND = self.findChild(QtWidgets.QLabel, 'label_only_COM_SECOND')
        self.label_COM_SECOND = self.findChild(QtWidgets.QLabel, 'label_COM_SECOND')

        self.pushButton = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.pushButton_First_Device = self.findChild(QtWidgets.QPushButton, 'pushButton_First_Device')
        self.pushButton_Second_Device = self.findChild(QtWidgets.QPushButton, 'pushButton_Second_Device')

        # self.available_ports = serial_ports()

        # self.First_Device_Slave_Address = 1

        self.pushButton.clicked.connect(self.open_main_window)
        self.pushButton_First_Device.clicked.connect(self.pushButton_First_Device_clicked)
        self.pushButton_Second_Device.clicked.connect(self.pushButton_Second_Device_clicked)
        self.reset()



        QApplication.setStyle(QStyleFactory.create('Fusion'))
        QApplication.setPalette(QApplication.style().standardPalette())
        # self.setGeometry(200, 200, 700, 250)
        self.setWindowTitle("Дальномер")

        self.main_window = MAIN_window()


    def reset(self):
        self.First_Device_Current_COM = ''
        self.Second_Device_Current_COM = ''
        self.First_Device_ID = 1
        self.Second_Device_ID = 2
        self.pushButton_First_Device.setStyleSheet("background-color :  None")
        self.pushButton_Second_Device.setStyleSheet("background-color :  None")
        self.label_COM_FIRST.setText('')
        self.label_COM_SECOND.setText('')
        self.pushButton_First_Device_Success = False
        self.pushButton_Second_Device_Success = False
        self.pushButton.setStyleSheet("background-color :  red")


    def pushButton_First_Device_clicked(self):

        self.First_Device_Current_COM = str(serial_ports(self.First_Device_ID))
        if self.First_Device_Current_COM == 'None':
            # print('Ошибка подключения')
            self.label_COM_FIRST.setText('Ошибка подключения')
            self.pushButton_First_Device.setStyleSheet("background-color :  red")
            message_box_info(2)
        else:
            # print('Bingo')
            self.label_COM_FIRST.setText("Подключено по {} порту!!! ".format(self.First_Device_Current_COM))
            self.pushButton_First_Device.setStyleSheet("background-color :  rgb(0, 255, 127)")
            self.pushButton_First_Device_Success = True


        if self.pushButton_First_Device_Success and self.pushButton_Second_Device_Success:
            self.pushButton.setStyleSheet("background-color :  rgb(0, 255, 127)")



    def pushButton_Second_Device_clicked(self):

        self.Second_Device_Current_COM = str(serial_ports(self.Second_Device_ID))
        if self.Second_Device_Current_COM == 'None':
            # print('Ошибка подключения')
            self.label_COM_SECOND.setText('Ошибка подключения')
            self.pushButton_Second_Device.setStyleSheet("background-color :  red")
            message_box_info(2)
        else:
            # print('Bingo')
            self.label_COM_SECOND.setText("Подключено по {} порту!!! ".format(self.Second_Device_Current_COM))
            self.pushButton_Second_Device.setStyleSheet("background-color :  rgb(0, 255, 127)")
            self.pushButton_Second_Device_Success = True

        if self.pushButton_First_Device_Success and self.pushButton_Second_Device_Success:
            self.pushButton.setStyleSheet("background-color :  rgb(0, 255, 127)")

    def open_main_window(self):

        # current_COM_FIRST, current_COM_SECOND = self.current_com()
        # print('Current COMS',current_COM_FIRST, current_COM_SECOND)

        try:
            connection1 = create_modbus_connection(self.First_Device_Current_COM, 1, 9600, 8, 1, 1)
            print(connection1.instrument.read_float(registeraddress=1, functioncode=3, number_of_registers=2, ))

            connection2 = create_modbus_connection(self.Second_Device_Current_COM, 2, 9600, 8, 1, 1)
            print(connection2.instrument.read_float(registeraddress=1, functioncode=3, number_of_registers=2, ))

            self.main_window.set_connection_parameters(self.First_Device_Current_COM, self.Second_Device_Current_COM,
                                                       self.First_Device_ID, self.Second_Device_ID)
            self.main_window.show()
            self.hide()

        except:
            self.reset()
            message_box_info(1)

    # def combo_selected(self):
    #     item1 = self.comboBox_COM_FIRST.currentText()
    #     item2 = self.comboBox_COM_SECOND.currentText()
    #     print(type(item1), item1)
    #     print(type(item2), item2)
    #     self.label_COM_FIRST.setText(item1)
    #     self.label_COM_SECOND.setText(item2)
    #
    # def current_com(self):
    #     return self.First_Device_Current_COM, self.Second_Device_Current_COM



app = QApplication(sys.argv)
AUTHwindow = AUTH_window()
AUTHwindow.show()
sys.exit(app.exec_())