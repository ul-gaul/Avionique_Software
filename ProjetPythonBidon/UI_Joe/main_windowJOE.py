from main_windowUIJOE import Ui_MainWindow
from PyQt4 import QtCore, QtGui
import sys

from infos_dialog import InfosDialog

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(parent)
        self.init_widgets()

    def init_widgets(self):
        self.pushButton_open.setEnabled(False)

        #connections
        self.lineEdit_infos.editingFinished.connect(self.enable_button)
        self.pushButton_open.clicked.connect(self.open_dialog)

    def enable_button(self):
        if self.lineEdit_infos.text() != '':
            self.pushButton_open.setEnabled(True)
        else:
            self.pushButton_open.setEnabled(False)

    def open_dialog(self):
        infos_dialog = InfosDialog(self.lineEdit_infos.text())
        infos_dialog.exec_()
        self.textBrowser.append(infos_dialog.text)

if __name__ == '__main__':
    a = QtGui.QApplication(sys.argv)
    f = QtGui.QMainWindow()
    MainWindow(f)
    f.show()
    a.exec_()