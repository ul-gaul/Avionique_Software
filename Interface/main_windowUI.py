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
        self.speedGraph = QtGui.QGraphicsView(self.centralwidget)
        self.speedGraph.setObjectName(_fromUtf8("speedGraph"))
        self.speedLayout.addWidget(self.speedGraph)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.speedLayout.addItem(spacerItem1)
        self.gridLayout_5.addLayout(self.speedLayout, 0, 0, 1, 1)
        self.vSpeedLayout = QtGui.QVBoxLayout()
        self.vSpeedLayout.setObjectName(_fromUtf8("vSpeedLayout"))
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vSpeedLayout.addItem(spacerItem2)
        self.hSpeedLayout = QtGui.QHBoxLayout()
        self.hSpeedLayout.setObjectName(_fromUtf8("hSpeedLayout"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hSpeedLayout.addItem(spacerItem3)
        self.speedLCD = QtGui.QLCDNumber(self.centralwidget)
        self.speedLCD.setObjectName(_fromUtf8("speedLCD"))
        self.hSpeedLayout.addWidget(self.speedLCD)
        self.speedLabel = QtGui.QLabel(self.centralwidget)
        self.speedLabel.setObjectName(_fromUtf8("speedLabel"))
        self.hSpeedLayout.addWidget(self.speedLabel)
        self.vSpeedLayout.addLayout(self.hSpeedLayout)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vSpeedLayout.addItem(spacerItem4)
        self.gridLayout_5.addLayout(self.vSpeedLayout, 0, 1, 1, 1)
        self.mapLayout = QtGui.QHBoxLayout()
        self.mapLayout.setObjectName(_fromUtf8("mapLayout"))
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.mapLayout.addItem(spacerItem5)
        self.mapGraph = QtGui.QGraphicsView(self.centralwidget)
        self.mapGraph.setObjectName(_fromUtf8("mapGraph"))
        self.mapLayout.addWidget(self.mapGraph)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.mapLayout.addItem(spacerItem6)
        self.gridLayout_5.addLayout(self.mapLayout, 0, 2, 1, 1)
        self.heightLayout = QtGui.QHBoxLayout()
        self.heightLayout.setObjectName(_fromUtf8("heightLayout"))
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.heightLayout.addItem(spacerItem7)
        self.heightGraph = QtGui.QGraphicsView(self.centralwidget)
        self.heightGraph.setObjectName(_fromUtf8("heightGraph"))
        self.heightLayout.addWidget(self.heightGraph)
        spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.heightLayout.addItem(spacerItem8)
        self.gridLayout_5.addLayout(self.heightLayout, 1, 0, 1, 1)
        self.instantSpeedAngleLay = QtGui.QGridLayout()
        self.instantSpeedAngleLay.setObjectName(_fromUtf8("instantSpeedAngleLay"))
        self.instantHeightLay = QtGui.QHBoxLayout()
        self.instantHeightLay.setObjectName(_fromUtf8("instantHeightLay"))
        spacerItem9 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.instantHeightLay.addItem(spacerItem9)
        self.heightLCD = QtGui.QLCDNumber(self.centralwidget)
        self.heightLCD.setObjectName(_fromUtf8("heightLCD"))
        self.instantHeightLay.addWidget(self.heightLCD)
        self.heightLabel = QtGui.QLabel(self.centralwidget)
        self.heightLabel.setObjectName(_fromUtf8("heightLabel"))
        self.instantHeightLay.addWidget(self.heightLabel)
        self.instantSpeedAngleLay.addLayout(self.instantHeightLay, 1, 0, 1, 1)
        spacerItem10 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.instantSpeedAngleLay.addItem(spacerItem10, 0, 0, 1, 1)
        self.instantAngleLay = QtGui.QHBoxLayout()
        self.instantAngleLay.setObjectName(_fromUtf8("instantAngleLay"))
        spacerItem11 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.instantAngleLay.addItem(spacerItem11)
        self.angleLCD = QtGui.QLCDNumber(self.centralwidget)
        self.angleLCD.setObjectName(_fromUtf8("angleLCD"))
        self.instantAngleLay.addWidget(self.angleLCD)
        self.angleLabel = QtGui.QLabel(self.centralwidget)
        self.angleLabel.setObjectName(_fromUtf8("angleLabel"))
        self.instantAngleLay.addWidget(self.angleLabel)
        self.instantSpeedAngleLay.addLayout(self.instantAngleLay, 3, 0, 1, 1)
        spacerItem12 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.instantSpeedAngleLay.addItem(spacerItem12, 2, 0, 1, 1)
        spacerItem13 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.instantSpeedAngleLay.addItem(spacerItem13, 4, 0, 1, 1)
        self.gridLayout_5.addLayout(self.instantSpeedAngleLay, 1, 1, 1, 1)
        self.angleLayout = QtGui.QHBoxLayout()
        self.angleLayout.setObjectName(_fromUtf8("angleLayout"))
        spacerItem14 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.angleLayout.addItem(spacerItem14)
        self.angleGraph = QtGui.QGraphicsView(self.centralwidget)
        self.angleGraph.setObjectName(_fromUtf8("angleGraph"))
        self.angleLayout.addWidget(self.angleGraph)
        spacerItem15 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.angleLayout.addItem(spacerItem15)
        self.gridLayout_5.addLayout(self.angleLayout, 1, 2, 1, 1)
        self.AnalysisLayout = QtGui.QHBoxLayout()
        self.AnalysisLayout.setObjectName(_fromUtf8("AnalysisLayout"))
        spacerItem16 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.AnalysisLayout.addItem(spacerItem16)
        self.analyseButton = QtGui.QPushButton(self.centralwidget)
        self.analyseButton.setObjectName(_fromUtf8("analyseButton"))
        self.AnalysisLayout.addWidget(self.analyseButton)
        self.gridLayout_5.addLayout(self.AnalysisLayout, 2, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.speedLabel.setText(_translate("MainWindow", "m/s", None))
        self.heightLabel.setText(_translate("MainWindow", "m", None))
        self.angleLabel.setText(_translate("MainWindow", "°", None))
        self.analyseButton.setText(_translate("MainWindow", "Démarrer l\'analyse", None))

