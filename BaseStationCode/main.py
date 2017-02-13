import sys

from PyQt4 import QtGui

from src.ui import MainWindow

if __name__ == '__main__':
    a = QtGui.QApplication(sys.argv)
    f = QtGui.QMainWindow()
    MainWindow(f)
    f.show()
    sys.exit(a.exec())
