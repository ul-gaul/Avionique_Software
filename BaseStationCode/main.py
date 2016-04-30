from ui.main_window import MainWindow
from PyQt4 import QtGui
import sys

if __name__ == '__main__':
    a = QtGui.QApplication(sys.argv)
    f = QtGui.QMainWindow()
    MainWindow(f)
    f.show()
    sys.exit(a.exec())
