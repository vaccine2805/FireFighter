from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys
from random import randint
import serial
import csv
import time
import math

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.ser = serial.Serial()
        self.ser.port = 'COM6'
        self.ser.baudrate = 9600
        self.ser.setDTR(False)
        self.ser.setRTS(False)

        self.ser.open()

        self.attx = []
        self.atty = []
        self.attz = []
        self.rttx = []
        self.rtty = []
        self.rttz = []

        # Create the QTabWidget and add the three PlotWidget instances as tabs
        # Create tabs
        self.tabs = QtWidgets.QTabWidget()
        self.tab1 = QtWidgets.QWidget()
        self.tab2 = QtWidgets.QWidget()
        self.tabs.addTab(self.tab1, "Accelerometer")
        self.tabs.addTab(self.tab2, "Rotation")

        # Create layouts for each tab
        self.layout1 = QtWidgets.QGridLayout()
        self.layout2 = QtWidgets.QGridLayout()
        self.tab1.setLayout(self.layout1)
        self.tab2.setLayout(self.layout2)

        # Initialize the plots and add them to the layouts
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setTitle("Accelerometer X")
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setYRange(-50, 50)
        self.graphWidget.setMouseEnabled(x=False, y=False)
        self.graphWidget2 = pg.PlotWidget()
        self.graphWidget2.setTitle("Accelerometer Y")
        self.graphWidget2.showGrid(x=True, y=True)
        self.graphWidget2.setYRange(-50, 50)
        self.graphWidget2.setMouseEnabled(x=False, y=False)
        self.graphWidget3 = pg.PlotWidget()
        self.graphWidget3.setTitle("Accelerometer Z")
        self.graphWidget3.showGrid(x=True, y=True)
        self.graphWidget3.setYRange(-50, 50)
        self.graphWidget3.setMouseEnabled(x=False, y=False)
        self.graphWidget4 = pg.PlotWidget()
        self.graphWidget4.setTitle("Rotation X")
        self.graphWidget4.showGrid(x=True, y=True)
        self.graphWidget4.setYRange(-50, 50)
        self.graphWidget4.setMouseEnabled(x=False, y=False)
        self.graphWidget5 = pg.PlotWidget()
        self.graphWidget5.setTitle("Rotation Y")
        self.graphWidget5.showGrid(x=True, y=True)
        self.graphWidget5.setYRange(-50, 50)
        self.graphWidget5.setMouseEnabled(x=False, y=False)
        self.graphWidget6 = pg.PlotWidget()
        self.graphWidget6.setTitle("Rotation Z")
        self.graphWidget6.showGrid(x=True, y=True)
        self.graphWidget6.setYRange(-50, 50)
        self.graphWidget6.setMouseEnabled(x=False, y=False)

        self.layout1.addWidget(self.graphWidget, 0, 0)
        self.layout1.addWidget(self.graphWidget2, 1, 0)
        self.layout1.addWidget(self.graphWidget3, 2, 0)
        self.layout2.addWidget(self.graphWidget4, 0, 0)
        self.layout2.addWidget(self.graphWidget5, 1, 0)
        self.layout2.addWidget(self.graphWidget6, 2, 0)

        # Set initial data for the plots
        self.x = list(range(20))  # 20 time points
        self.attx = [randint(0, 0) for _ in range(20)]  # 20 data points
        self.atty = [randint(0, 0) for _ in range(20)]  # 20 data points
        self.attz = [randint(0, 0) for _ in range(20)]  # 20 data points
        self.rttx = [randint(0, 0) for _ in range(20)]  # 20 data points
        self.rtty = [randint(0, 0) for _ in range(20)]  # 20 data points
        self.rttz = [randint(0, 0) for _ in range(20)]  # 20 data points

        pen = pg.mkPen(color=(255, 0, 0))
        pen2 = pg.mkPen(color=(0, 255, 0))
        pen3 = pg.mkPen(color=(0, 0, 255))
        pen4 = pg.mkPen(color=(0, 102, 102))
        pen5 = pg.mkPen(color=(204, 0, 204))
        pen6 = pg.mkPen(color=(255, 128, 0))

        self.data_line = self.graphWidget.plot(self.x, self.attx, pen=pen)
        self.data_line2 = self.graphWidget2.plot(self.x, self.atty, pen=pen2)
        self.data_line3 = self.graphWidget3.plot(self.x, self.attz, pen=pen3)
        self.data_line4 = self.graphWidget4.plot(self.x, self.rttx, pen=pen4)
        self.data_line5 = self.graphWidget5.plot(self.x, self.rtty, pen=pen5)
        self.data_line6 = self.graphWidget6.plot(self.x, self.rttz, pen=pen6)

        # Add the plots to the layouts and set the initial data
        self.graphWidget.plot(self.x, self.attx, pen)
        self.graphWidget2.plot(self.x, self.atty, pen2)
        self.graphWidget3.plot(self.x, self.attz, pen3)
        self.graphWidget4.plot(self.x, self.rttx, pen4)
        self.graphWidget5.plot(self.x, self.rtty, pen5)
        self.graphWidget6.plot(self.x, self.rttz, pen6)



        # Set the layout for the main window
        centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(centralWidget)
        layout = QtWidgets.QVBoxLayout()
        centralWidget.setLayout(layout)

        # Add the tab widget to the main window layout
        layout.addWidget(self.tabs)

        # Set up the timer for updating the plots
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        b = self.ser.readline()
        str1 = b.decode('UTF-8')
        lst = str1.split('|')
        if len(lst) > 0:
            att = lst[0].split(',')
            rtt = lst[1].split(',')

            # Keep only the last 20 values in each list
            self.attx = self.attx[1:]
            self.atty = self.atty[1:]
            self.attz = self.attz[1:]
            self.rttx = self.rttx[1:]
            self.rtty = self.rtty[1:]
            self.rttz = self.rttz[1:]

            self.attx.append(float(att[0]))
            self.atty.append(float(att[1]))
            self.attz.append(float(att[2]))
            self.rttx.append(float(rtt[0]))
            self.rtty.append(float(rtt[1]))
            self.rttz.append(float(rtt[2]))

            # Update the data for each plot
            self.data_line.setData(self.x, self.attx)
            self.data_line2.setData(self.x, self.atty)
            self.data_line3.setData(self.x, self.attz)
            self.data_line4.setData(self.x, self.rttx)
            self.data_line5.setData(self.x, self.rtty)
            self.data_line6.setData(self.x, self.rttz)

            # Adjust the x-axis range to show only the latest value
            # x_max = self.x[-1] + 1
            # x_min = x_max - 20
            # self.graphWidget.setXRange(x_min, x_max)
            # self.graphWidget2.setXRange(x_min, x_max)
            # self.graphWidget3.setXRange(x_min, x_max)
            # self.graphWidget4.setXRange(x_min, x_max)
            # self.graphWidget5.setXRange(x_min, x_max)
            # self.graphWidget6.setXRange(x_min, x_max)
            self.x = self.x[1:]  # Remove the first y element.
            self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.




            header = ['attx', 'atty']
            data = [self.attx, self.atty, ['attz', self.attz], ['rttx', self.rttx], ['rtty', self.rtty], ['rttz', self.rttz]]

            with open('data2.csv', 'w', encoding='UTF-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                for row in data:
                    writer.writerow(row)

            # header = ['time', 'attx', 'atty', 'attz', 'rttx', 'rtty', 'rttz']
            # with open('data.csv', 'w', encoding='UTF-8', newline='') as f:
            #     writer = csv.writer(f)
            #     writer.writerow(header)
            #
            #         current_time = time.time()
            #         attx = att_data['attx']
            #         atty = att_data['atty']
            #         attz = att_data['attz']
            #         rttx = rtt_data['rttx']
            #         rtty = rtt_data['y']
            #         rttz = rtt_data['z']
            #
            #         data = [current_time, attx, atty, attz, rttx, rtty, rttz]
            #
            #         writer.writerow(data)
            #         f.flush()
            #         time.sleep(1)


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())
