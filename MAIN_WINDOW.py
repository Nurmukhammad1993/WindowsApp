from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont
import serial.tools.list_ports
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout, QMessageBox
import sys
import minimalmodbus
import time
from GLOBAL_FUNCTIONS import create_modbus_connection, serial_ports, message_box_info
from PDF_GENERATOR import Window

class MAIN_window(QtWidgets.QMainWindow):
    def __init__(self):
        super(MAIN_window, self).__init__()
        loadUi('MAIN.ui', self)
        self.label = self.findChild(QtWidgets.QLabel, 'label')
        self.pushButton = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.pushButton_pdf_generate = self.findChild(QtWidgets.QPushButton, 'pushButton_generate')
        self.lineEdit_values = self.findChild(QtWidgets.QLineEdit, 'lineEdit_values')
        self.tableWidget = self.findChild(QtWidgets.QTableWidget, 'tableWidget')
        self.spinBox_repeat_count = self.findChild(QtWidgets.QSpinBox, 'spinBox_repeat_count')
        self.spinBox_period = self.findChild(QtWidgets.QSpinBox, 'spinBox_period')
        self.spinBox_repeat_count.setMaximum(10)
        self.spinBox_period.setMaximum(60)
        self.spinBox_repeat_count.setMinimum(1)
        self.spinBox_period.setMinimum(1)

        self.spinBox_repeat_count.setValue(5)
        self.spinBox_period.setValue(5)

        self.repeat_count = 5
        self.period = 5

        # self.spinBox_period.valueChanged.connect(self.set_value)
        self.spinBox_repeat_count.valueChanged.connect(self.set_value)
        self.spinBox_period.valueChanged.connect(self.set_value)

        self.tableWidget.setColumnWidth(0, 175)
        self.tableWidget.setColumnWidth(1, 135)
        self.tableWidget.setColumnWidth(2, 135)

        self.pushButton.clicked.connect(self.read_device_value)
        self.pushButton_pdf_generate.clicked.connect(self.generator_button_clicked)
        self.setWindowTitle("Дальномер")

        self.generator_window = Window()

    def generator_button_clicked(self):
        self.generator_window.show()
        # self.hide()


    def set_value(self):
        self.repeat_count = self.spinBox_repeat_count.value()
        self.period = self.spinBox_period.value()



    def set_connection_parameters(self, COM_FIRST, COM_SECOND, First_Device_ID, Second_Device_ID):
        self.current_COM_FIRST = COM_FIRST
        self.current_COM_SECOND = COM_SECOND
        self.First_Device_ID = First_Device_ID
        self.Second_Device_ID = Second_Device_ID
        print('Current COM is: ', COM_FIRST, COM_SECOND)

    def reset_tableWidget(self):

        self.tableWidget.clear()
        self.tableWidget.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Время'))
        self.tableWidget.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem('Устройство_1'))
        self.tableWidget.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem('Устройство_2'))

    def read_device_value(self):
        # Перед началом новой записи, очищаем таблицу
        self.reset_tableWidget()
        self.tableWidget = self.findChild(QtWidgets.QTableWidget, 'tableWidget')
        self.thread = QtCore.QThread()
        self.browserHandler = BrowserHandler()
        self.browserHandler.set_connection_parameters(self.current_COM_FIRST, self.current_COM_SECOND,
                                                      self.First_Device_ID, self.Second_Device_ID,
                                                      self.repeat_count, self.period)
        self.browserHandler.moveToThread(self.thread)

        self.thread.started.connect(self.browserHandler.run)
        self.browserHandler.finished.connect(self.thread.quit)

        self.browserHandler.finished.connect(self.browserHandler.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.browserHandler.finished.connect(self.ended)

        self.browserHandler.newText.connect(self.addNewText)
        self.thread.start()

        self.browserHandler.progress.connect(self.change_button_color)
        self.pushButton.setEnabled(False)

        self.browserHandler.finished.connect(lambda: self.pushButton.setEnabled(True))

    def change_button_color(self, state):
        if state:
            self.pushButton.setStyleSheet("background-color :  red")
        else:
            self.pushButton.setStyleSheet("background-color :  None")

    def ended(self):
        print('Thread has been terminated')

    # @QtCore.pyqtSlot(str)
    def addNewText(self, Dict):
        print(Dict)
        test = Dict['Time'][0]
        iter = int(Dict['iteration'][0])
        self.lineEdit_values.setText(test)
        self.tableWidget.setItem(iter, 0, QtWidgets.QTableWidgetItem(Dict['Time'][0]))
        self.tableWidget.setItem(iter, 1, QtWidgets.QTableWidgetItem(Dict['COM1'][0]))
        self.tableWidget.setItem(iter, 2, QtWidgets.QTableWidgetItem(Dict['COM2'][0]))


# Объект, который будет перенесён в другой поток для выполнения кода
class BrowserHandler(QtCore.QObject):
    # running = False
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(bool)
    newText = QtCore.pyqtSignal(dict)
    Dict = {}

    def set_connection_parameters(self, COM_FIRST, COM_SECOND, First_Device_ID, Second_Device_ID, repeat_count, period):
        self.COM_FIRST = COM_FIRST
        self.COM_SECOND = COM_SECOND
        self.First_Device_ID = First_Device_ID
        self.Second_Device_ID = Second_Device_ID
        self.spinBox_repeat_count = repeat_count
        self.spinBox_period = period

    # метод, который будет выполнять алгоритм в другом потоке
    def run(self):
        i = 0
        Dict = {'Time': [], 'COM1': [], 'COM2': [], 'iteration': []}

        connection1 = create_modbus_connection(self.COM_FIRST, 1, 9600, 8, 1, 1)
        connection2 = create_modbus_connection(self.COM_SECOND, 2, 9600, 8, 1, 1)
        while i < self.spinBox_repeat_count:
            self.progress.emit(True)
            # посылаем сигнал из второго потока в GUI поток
            Dict['Time'].append(str(time.strftime("%Y.%m.%d %H:%M:%S", time.localtime())))
            Dict['COM1'].append(
                str(round(connection1.instrument.read_float(registeraddress=1, functioncode=3, number_of_registers=2),
                          2)))
            Dict['COM2'].append(
                str(round(connection2.instrument.read_float(registeraddress=1, functioncode=3, number_of_registers=2),
                          2)))
            Dict['iteration'].append(i)

            self.newText.emit(Dict)
            Dict = {'Time': [], 'COM1': [], 'COM2': [], 'iteration': []}
            time.sleep(self.spinBox_period)

            i += 1

        self.progress.emit(False)
        self.finished.emit()
