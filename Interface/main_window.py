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
        MainWindow.resize(794, 591)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_5 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.speedLayout = QtGui.QHBoxLayout()
        self.speedLayout.setObjectName(_fromUtf8("speedLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.speedLayout.addItem(spacerItem)
        self.graphicsView_3 = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView_3.setObjectName(_fromUtf8("graphicsView_3"))
        self.speedLayout.addWidget(self.graphicsView_3)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.speedLayout.addItem(spacerItem1)
        self.gridLayout_5.addLayout(self.speedLayout, 0, 0, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.lcdNumber = QtGui.QLCDNumber(self.centralwidget)
        self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))
        self.horizontalLayout_3.addWidget(self.lcdNumber)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem4)
        self.gridLayout_5.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        self.mapLayout = QtGui.QHBoxLayout()
        self.mapLayout.setObjectName(_fromUtf8("mapLayout"))
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.mapLayout.addItem(spacerItem5)
        self.graphicsView_4 = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView_4.setObjectName(_fromUtf8("graphicsView_4"))
        self.mapLayout.addWidget(self.graphicsView_4)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.mapLayout.addItem(spacerItem6)
        self.gridLayout_5.addLayout(self.mapLayout, 0, 2, 1, 1)
        self.heightLayout = QtGui.QHBoxLayout()
        self.heightLayout.setObjectName(_fromUtf8("heightLayout"))
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.heightLayout.addItem(spacerItem7)
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.heightLayout.addWidget(self.graphicsView)
        spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.heightLayout.addItem(spacerItem8)
        self.gridLayout_5.addLayout(self.heightLayout, 1, 0, 1, 1)
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem9 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem9)
        self.lcdNumber_2 = QtGui.QLCDNumber(self.centralwidget)
        self.lcdNumber_2.setObjectName(_fromUtf8("lcdNumber_2"))
        self.horizontalLayout_4.addWidget(self.lcdNumber_2)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_4.addWidget(self.label_2)
        self.gridLayout_4.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)
        spacerItem10 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem10, 0, 0, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        spacerItem11 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem11)
        self.lcdNumber_3 = QtGui.QLCDNumber(self.centralwidget)
        self.lcdNumber_3.setObjectName(_fromUtf8("lcdNumber_3"))
        self.horizontalLayout_5.addWidget(self.lcdNumber_3)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_5.addWidget(self.label_3)
        self.gridLayout_4.addLayout(self.horizontalLayout_5, 3, 0, 1, 1)
        spacerItem12 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem12, 2, 0, 1, 1)
        spacerItem13 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem13, 4, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_4, 1, 1, 1, 1)
        self.angleLayout = QtGui.QHBoxLayout()
        self.angleLayout.setObjectName(_fromUtf8("angleLayout"))
        spacerItem14 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.angleLayout.addItem(spacerItem14)
        self.graphicsView_2 = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView_2.setObjectName(_fromUtf8("graphicsView_2"))
        self.angleLayout.addWidget(self.graphicsView_2)
        spacerItem15 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.angleLayout.addItem(spacerItem15)
        self.gridLayout_5.addLayout(self.angleLayout, 1, 2, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem16 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem16)
        self.analyseButton = QtGui.QPushButton(self.centralwidget)
        self.analyseButton.setObjectName(_fromUtf8("analyseButton"))
        self.horizontalLayout.addWidget(self.analyseButton)
        self.gridLayout_5.addLayout(self.horizontalLayout, 2, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "m/s", None))
        self.label_2.setText(_translate("MainWindow", "m", None))
        self.label_3.setText(_translate("MainWindow", "°", None))
        self.analyseButton.setText(_translate("MainWindow", "Démarrer l\'analyse", None))

