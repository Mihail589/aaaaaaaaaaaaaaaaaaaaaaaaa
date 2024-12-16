import string
import sys
import serial
import re
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import qDebug, QIODevice
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtWidgets import *
import ui
class Example(QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.serialPort = QSerialPort()
        self.comboBox.addItems([serialPort.portName() for serialPort in QSerialPortInfo().availablePorts()])
        self.pushButton.clicked.connect(self.open_serial_port)
    def open_serial_port(self):
        ser = serial.Serial(port=self.comboBox.currentData(), baudrate=9600)
        while True:
            data = re.split("[,']", str(ser.readline()).rstrip('\n'))       
            print(data)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Example()
    form.show()
    app.exec()