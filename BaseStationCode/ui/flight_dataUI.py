# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'flight_data.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(746, 534)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.speedLayout = QtGui.QHBoxLayout()
        self.speedLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.speedLayout.setObjectName(_fromUtf8("speedLayout"))
        self.gridLayout.addLayout(self.speedLayout, 0, 0, 1, 1)
        self.vSpeedLayout = QtGui.QVBoxLayout()
        self.vSpeedLayout.setObjectName(_fromUtf8("vSpeedLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vSpeedLayout.addItem(spacerItem)
        self.hSpeedLayout = QtGui.QHBoxLayout()
        self.hSpeedLayout.setObjectName(_fromUtf8("hSpeedLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hSpeedLayout.addItem(spacerItem1)
        self.speedLCD = QtGui.QLCDNumber(Dialog)
        self.speedLCD.setStyleSheet(_fromUtf8("QLCDNumber{\n"
"    color: rgb(0, 0, 0);    \n"
"}"))
        self.speedLCD.setSmallDecimalPoint(False)
        self.speedLCD.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.speedLCD.setObjectName(_fromUtf8("speedLCD"))
        self.hSpeedLayout.addWidget(self.speedLCD)
        self.speedLabel = QtGui.QLabel(Dialog)
        self.speedLabel.setObjectName(_fromUtf8("speedLabel"))
        self.hSpeedLayout.addWidget(self.speedLabel)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hSpeedLayout.addItem(spacerItem2)
        self.vSpeedLayout.addLayout(self.hSpeedLayout)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vSpeedLayout.addItem(spacerItem3)
        self.gridLayout.addLayout(self.vSpeedLayout, 0, 1, 1, 1)
        self.mapLayout = QtGui.QHBoxLayout()
        self.mapLayout.setObjectName(_fromUtf8("mapLayout"))
        self.gridLayout.addLayout(self.mapLayout, 0, 2, 1, 1)
        self.heightLayout = QtGui.QHBoxLayout()
        self.heightLayout.setObjectName(_fromUtf8("heightLayout"))
        self.gridLayout.addLayout(self.heightLayout, 1, 0, 1, 1)
        self.instantSpeedAngleLay = QtGui.QGridLayout()
        self.instantSpeedAngleLay.setObjectName(_fromUtf8("instantSpeedAngleLay"))
        self.instantHeightLay = QtGui.QHBoxLayout()
        self.instantHeightLay.setObjectName(_fromUtf8("instantHeightLay"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.instantHeightLay.addItem(spacerItem4)
        self.heightLCD = QtGui.QLCDNumber(Dialog)
        self.heightLCD.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.heightLCD.setObjectName(_fromUtf8("heightLCD"))
        self.instantHeightLay.addWidget(self.heightLCD)
        self.heightLabel = QtGui.QLabel(Dialog)
        self.heightLabel.setObjectName(_fromUtf8("heightLabel"))
        self.instantHeightLay.addWidget(self.heightLabel)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.instantHeightLay.addItem(spacerItem5)
        self.instantSpeedAngleLay.addLayout(self.instantHeightLay, 1, 0, 1, 1)
        spacerItem6 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.instantSpeedAngleLay.addItem(spacerItem6, 0, 0, 1, 1)
        self.instantAngleLay = QtGui.QHBoxLayout()
        self.instantAngleLay.setObjectName(_fromUtf8("instantAngleLay"))
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.instantAngleLay.addItem(spacerItem7)
        self.angleLCD = QtGui.QLCDNumber(Dialog)
        self.angleLCD.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.angleLCD.setObjectName(_fromUtf8("angleLCD"))
        self.instantAngleLay.addWidget(self.angleLCD)
        self.angleLabel = QtGui.QLabel(Dialog)
        self.angleLabel.setObjectName(_fromUtf8("angleLabel"))
        self.instantAngleLay.addWidget(self.angleLabel)
        spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.instantAngleLay.addItem(spacerItem8)
        self.instantSpeedAngleLay.addLayout(self.instantAngleLay, 3, 0, 1, 1)
        spacerItem9 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.instantSpeedAngleLay.addItem(spacerItem9, 2, 0, 1, 1)
        spacerItem10 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.instantSpeedAngleLay.addItem(spacerItem10, 4, 0, 1, 1)
        self.gridLayout.addLayout(self.instantSpeedAngleLay, 1, 1, 1, 1)
        self.angleLayout = QtGui.QHBoxLayout()
        self.angleLayout.setObjectName(_fromUtf8("angleLayout"))
        self.gridLayout.addLayout(self.angleLayout, 1, 2, 1, 1)
        self.AnalysisLayout = QtGui.QHBoxLayout()
        self.AnalysisLayout.setObjectName(_fromUtf8("AnalysisLayout"))
        self.startButton = QtGui.QPushButton(Dialog)
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.AnalysisLayout.addWidget(self.startButton)
        self.stopButton = QtGui.QPushButton(Dialog)
        self.stopButton.setObjectName(_fromUtf8("stopButton"))
        self.AnalysisLayout.addWidget(self.stopButton)
        spacerItem11 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.AnalysisLayout.addItem(spacerItem11)
        self.analyseButton = QtGui.QPushButton(Dialog)
        self.analyseButton.setObjectName(_fromUtf8("analyseButton"))
        self.AnalysisLayout.addWidget(self.analyseButton)
        self.gridLayout.addLayout(self.AnalysisLayout, 2, 0, 1, 3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.speedLabel.setText(_translate("Dialog", "m/s", None))
        self.heightLabel.setText(_translate("Dialog", "m", None))
        self.angleLabel.setText(_translate("Dialog", "°", None))
        self.startButton.setText(_translate("Dialog", "Start", None))
        self.stopButton.setText(_translate("Dialog", "Arrêter la lecture", None))
        self.analyseButton.setText(_translate("Dialog", "Démarrer l\'analyse", None))

