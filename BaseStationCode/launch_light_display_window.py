import sys
from PyQt4 import QtGui
from ui.light_display_window import LightDisplayWindow

if __name__ == "__main__":
    a = QtGui.QApplication(sys.argv)
    # f = QtGui.QMainWindow()
    main_window = LightDisplayWindow()
    main_window.show()
    sys.exit(a.exec_())