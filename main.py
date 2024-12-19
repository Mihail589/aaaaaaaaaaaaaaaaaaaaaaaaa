import sys
import asyncio
import re
from PyQt5.QtGui import * # type: ignore
from PyQt5.QtCore import *# type: ignore
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo# type: ignore
from PyQt5.QtWidgets import *# type: ignore
import serial# type: ignore
import ui
from qasync import QEventLoop, asyncSlot# type: ignore

class Example(QMainWindow, ui.Ui_MainWindow):# type: ignore
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.flag = False
        self.ser = None
        self.serialPort = None
        self.comboBox.addItems([serialPort.portName() for serialPort in QSerialPortInfo().availablePorts()])
        self.pushButton.clicked.connect(self.start_serial_port)

    @asyncSlot()
    async def start_serial_port(self):
        """Запуск асинхронной задачи для работы с последовательным портом."""
        port_name = self.comboBox.currentText()
        if port_name:
            if self.flag == False:
                self.pushButton.setText("СТОП")
                self.repaint()
                self.flag = True
                await self.open_serial_port(port_name)
                
            else:
                self.pushButton.setText("СТАРТ")
                self.repaint()
                self.flag = False
                self.ser.close()
                
        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите порт.")# type: ignore

    async def open_serial_port(self, port_name):
        """Асинхронное чтение данных из последовательного порта."""
        try:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self.read_from_port, port_name)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть порт: {e}")# type: ignore

    def read_from_port(self, port_name):
        """Синхронное чтение данных из последовательного порта (выполняется в потоке)."""
        try:
            self.ser = serial.Serial(port_name, baudrate=9600, timeout=1)
            print(f"Порт {port_name} успешно открыт.")
            while True:
                line = self.ser.readline()
                if line:
                    data = re.split(r"[,']", line.decode('utf-8').strip())
                    print(data)
                    self.lineEdit.setText(data[3])
        except Exception as e:
            print(f"Ошибка при работе с портом: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)# type: ignore

    # Использование qasync для интеграции событийного цикла
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    form = Example()
    form.show()

    with loop:
        loop.run_forever()
