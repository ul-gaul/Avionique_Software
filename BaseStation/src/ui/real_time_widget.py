from src.ui.data_widget import DataWidget
from PyQt5 import QtWidgets


class RealTimeWidget(DataWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_acquiring = False
        self.start_stop_button = None
        self.init_button_and_timer()

    def init_button_and_timer(self):
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.start_stop_button = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start_stop_button.sizePolicy().hasHeightForWidth())
        self.start_stop_button.setSizePolicy(sizePolicy)
        self.start_stop_button.setObjectName("start_stop_button")
        self.start_stop_button.setText("Démarrer l'acquisition")
        self.horizontalLayout_5.addWidget(self.start_stop_button)
        self.lcdNumber = QtWidgets.QLCDNumber(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lcdNumber.sizePolicy().hasHeightForWidth())
        self.lcdNumber.setSizePolicy(sizePolicy)
        self.lcdNumber.setObjectName("lcdNumber")
        self.horizontalLayout_5.addWidget(self.lcdNumber)
        self.horizontalLayout.addLayout(self.horizontalLayout_5)
        self.start_stop_button.clicked.connect(self.update_button_text)

    def update_button_text(self):
        self.is_acquiring = not self.is_acquiring
        if self.is_acquiring:
            self.start_stop_button.setText("Arrêter l'acquisition")
        else:
            self.start_stop_button.setText("Démarrer l'acquisition")
