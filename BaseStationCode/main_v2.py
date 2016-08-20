import sys
from PyQt4 import QtGui
from ui.test_window import TestWindow

if __name__ == "__main__":
    a = QtGui.QApplication(sys.argv)
    f = QtGui.QMainWindow()
    main_window = TestWindow(f)
    f.show()
    a.exec_()