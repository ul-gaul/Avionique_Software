# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main_window.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(805, 582)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(50, 240, 711, 92))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.menuLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.menuLayout.setObjectName(_fromUtf8("menuLayout"))
        self.flightDataPush = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.flightDataPush.setMinimumSize(QtCore.QSize(200, 80))
        self.flightDataPush.setIconSize(QtCore.QSize(24, 24))
        self.flightDataPush.setObjectName(_fromUtf8("flightDataPush"))
        self.menuLayout.addWidget(self.flightDataPush)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.menuLayout.addItem(spacerItem)
        self.analysisPush = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.analysisPush.setMinimumSize(QtCore.QSize(200, 80))
        self.analysisPush.setObjectName(_fromUtf8("analysisPush"))
        self.menuLayout.addWidget(self.analysisPush)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.flightDataPush.setText(_translate("MainWindow", "Donnée de vol", None))
        self.analysisPush.setText(_translate("MainWindow", "Analyse", None))

