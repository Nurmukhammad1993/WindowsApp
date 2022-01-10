from PyQt5 import QtCore, QtGui, QtWidgets
import serial.tools.list_ports
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt,QThread, pyqtSignal
import sys
import minimalmodbus
import time





def serial_ports(slave_ID):
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass

    test = check_modbus_connection(result, slave_ID)
    print('serial_ports',test)
    return test





class create_modbus_connection():
    def __init__(self, COM, slave_address, baudrate, bytesize, stopbits, timeout):
        self.instrument = minimalmodbus.Instrument(COM, slave_address, mode=minimalmodbus.MODE_RTU)
        self.instrument.serial.baudrate = baudrate  # Baud
        self.instrument.serial.bytesize = bytesize
        self.instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
        self.instrument.serial.stopbits = stopbits
        self.instrument.serial.timeout = timeout  # seconds

        # Good practice
        self.instrument.close_port_after_each_call = True
        self.instrument.clear_buffers_before_each_transaction = True



def check_modbus_connection(ports, slave_ID):
    for port in ports:
        try:
            connection = create_modbus_connection(port, slave_ID, 9600, 8, 1, 1)
            print(connection.instrument.read_float(registeraddress=1, functioncode=3, number_of_registers=2, ))
            return port
        except:
            pass




def message_box_info(code):
    msg = QMessageBox()
    if code == 1:
        msg.setIcon(QMessageBox.Warning)

        msg.setText("Необходимо подключения обоих устройств")
        msg.setInformativeText("Подключите все устройства")
        # msg.setDetailedText("Убидитесь, что устройства подключены")
        msg.setWindowTitle("Ошибка")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.show()
        msg.exec_()
    elif code == 2:
        msg.setIcon(QMessageBox.Critical)

        msg.setText("Ошибка подключения")
        msg.setInformativeText("Не удается подключиться")
        msg.setDetailedText("проверьте целостность подключения кабелей")
        msg.setWindowTitle("Ошибка")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.show()
        msg.exec_()

