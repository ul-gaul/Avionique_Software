
from BaseStationCode.ui.main_window import MainWindow
from PyQt4 import QtGui
import sys
import serial
from BaseStationCode.communication.DetectSerial import *
from BaseStationCode.communication.serialReader import SerialReader
import time

if __name__ == '__main__':
    #portserie = serial_port()[0]
    #ser = serial.Serial(portserie, 9600,timeout = 0.2)
    #reader = SerialReader(ser, 'acquisition.csv')

    a = QtGui.QApplication(sys.argv)
    f = QtGui.QMainWindow()
    MainWindow(f)
    f.show()
    sys.exit(a.exec())
