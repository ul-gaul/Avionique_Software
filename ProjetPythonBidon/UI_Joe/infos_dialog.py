from PyQt4 import QtCore, QtGui
from infos_dialogUI import Ui_InfoDialog

class InfosDialog(QtGui.QDialog, Ui_InfoDialog):
    def __init__(self, text, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.text = text

        self.init_widgets()
        self.fill_fields()

    def init_widgets(self):
        self.pushButton.clicked.connect(self.ok)

    def fill_fields(self):
        self.label.setText(self.text)

    def ok(self):
        self.done(1)

