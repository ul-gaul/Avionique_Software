
from ui.main_window import MainWindow
from PyQt5 import QtGui
import sys
import time

if __name__ == '__main__':
    a = QtGui.QApplication(sys.argv)
    f = QtGui.QMainWindow()
    MainWindow(f)
    f.show()
    sys.exit(a.exec())
