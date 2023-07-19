from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton
from PyQt5.QtGui import QPixmap, QPainter, QIcon, QColor, QFont, QPainterPath
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore
from threading import Thread
import serial
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuickAlert")
        self.initUI()
        self.initSerial()
        self.startSerialThread()

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)

        self.label0 = QLabel(self)
        self.label0.setGeometry(15, 50, 1160, 990)
        self.label0.setStyleSheet("background-color: red")

        self.label1 = QLabel(self)
        self.label1.setGeometry(1200, 50, 700, 80)
        self.label1.setStyleSheet("background-color: gray; font-size: 24px; border : 3px solid black; color:white")
        self.label1.setContentsMargins(20, 0, 0, 0)
        self.label1.setText("Device1")

        self.image_label1 = QLabel(self)
        self.image_label1.setGeometry(1500, 65, 60, 50)
        image_path = "al_smg.png"
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(60, 50)
        self.image_label1.setPixmap(scaled_pixmap)

        self.image_label10 = QLabel(self)
        self.image_label10.setGeometry(1500, 65, 60, 50)
        image_path = "normal_1.png"
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(60, 50)
        self.image_label10.setPixmap(scaled_pixmap)


        self.label2 = QLabel(self)
        self.label2.setGeometry(1200, 140, 700, 80)
        self.label2.setStyleSheet("background-color: gray; font-size: 24px; border : 3px solid black; color:white")
        self.label2.setText("Device2")
        self.label2.setContentsMargins(20, 0, 0, 0)

        self.image_label2 = QLabel(self)
        self.image_label2.setGeometry(1500, 155, 60, 50)
        image_path = "al_smg.png"
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(60, 50)
        self.image_label2.setPixmap(scaled_pixmap)

        self.label3 = QLabel(self)
        self.label3.setGeometry(1200, 230, 700, 80)
        self.label3.setStyleSheet("background-color: gray; font-size: 24px; border : 3px solid black; color:white")
        self.label3.setText("Device3")
        self.label3.setContentsMargins(20, 0, 0, 0)

        self.image_label3 = QLabel(self)
        self.image_label3.setGeometry(1500, 245, 60, 50)
        image_path = "al_smg.png"
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(60, 50)
        self.image_label3.setPixmap(scaled_pixmap)

        self.label4 = QLabel(self)
        self.label4.setGeometry(1200, 320, 700, 80)
        self.label4.setStyleSheet("background-color: gray; font-size: 24px; border : 3px solid black; color:white")
        self.label4.setText("Device4")
        self.label4.setContentsMargins(20, 0, 0, 0)

        self.image_label4 = QLabel(self)
        self.image_label4.setGeometry(1500, 335, 60, 50)
        image_path = "al_smg.png"
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(60, 50)
        self.image_label4.setPixmap(scaled_pixmap)

        self.label5 = QLabel(self)
        self.label5.setGeometry(1200, 410, 700, 80)
        self.label5.setStyleSheet("background-color: gray; font-size: 24px; border : 3px solid black; color:white")
        self.label5.setText("Device5")
        self.label5.setContentsMargins(20, 0, 0, 0)

        self.image_label5 = QLabel(self)
        self.image_label5.setGeometry(1500, 425, 60, 50)
        image_path = "al_smg.png"
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(60, 50)
        self.image_label5.setPixmap(scaled_pixmap)

        self.label8 = QLabel(self)
        self.label8.setGeometry(1350, 500, 400, 190)
        self.label8.setStyleSheet("background-color: gray; font-size: 24px; color: white; border: 3px solid black")
        self.label8.setText("data\n")
        self.label8.setContentsMargins(0, 70, 0, 0)
        self.label8.setAlignment(QtCore.Qt.AlignCenter)
        self.label8.setWordWrap(True)

        self.label12 = QLabel(self)
        self.label12.setGeometry(1500, 507, 100, 50)
        self.label12.setStyleSheet("background-color: gray; font-size: 24px; color: white")
        self.label12.setText("Data")
        self.label12.setAlignment(QtCore.Qt.AlignCenter)

        button = QPushButton('Evacuate', self)
        button.setToolTip('This is an example button')
        button.setGeometry(1450, 900, 200, 100)
        button.setStyleSheet("background-color: red; font-size: 24px; border: 3px solid black; color:white;  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);")

        # Set the icon for the button
        icon = QIcon('eva.png.png')
        button.setIcon(icon)

        button.clicked.connect(self.on_click)

        self.show()

    def initSerial(self):
            self.ser = serial.Serial()
            self.ser.baudrate = 9600
            self.ser.port = 'COM3'
            self.ser.setDTR(False)
            self.ser.setRTS(False)

            try:
                self.ser.open()
            except serial.SerialException as e:
                print("Failed to open serial port:", e)
                sys.exit(1)

    def startSerialThread(self):
            self.serial_thread = Thread(target=self.serialDataThread)
            self.serial_thread.daemon = True
            self.serial_thread.start()

    def serialDataThread(self):
        while True:
            b = self.ser.readline()
            str1 = b.decode('UTF-8')
            lst = str1.split('|')
            if len(lst) > 2:
                att = lst[0].split(',')
                rtt = lst[1].split(',')
                stt = lst[2]

                attx, atty, attz = "", "", ""
                rttx, rtty, rttz = "", "", ""

                if len(att) >= 3:
                    attx = att[0]
                    atty = att[1]
                    attz = att[2]

                if len(rtt) >= 3:
                    rttx = rtt[0]
                    rtty = rtt[1]
                    rttz = rtt[2]

                self.updateSerialData(attx, atty, attz, rttx, rtty, rttz, stt)

    def updateSerialData(self, attx, atty, attz, rttx, rtty, rttz, stt):
        text = f"attx: {attx}, atty: {atty}, attz: {attz}\nrttx: {rttx}, rtty: {rtty}, rttz: {rttz}\nstt: {stt}"
        self.label8.setText(text)

        if stt == '0':
            self.image_label1.hide()
            self.image_label10.show()
        else:
            self.image_label1.show()
            self.image_label10.hide()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')

app = QApplication(sys.argv)
window = Window()
window.showMaximized()
sys.exit(app.exec_())
