from PyQt5.QtWidgets import QStatusBar, QLabel

from src.message_listener import MessageListener, MessageType
from src.ui.utils import read_stylesheet


class StatusBar(QStatusBar, MessageListener):

    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("status_bar")

        self.label = QLabel(self)
        self.label.setObjectName("status_bar_label")
        label_stylesheet = read_stylesheet("src/resources/status_bar_label.css")
        self.label.setStyleSheet(label_stylesheet)
        self.addWidget(self.label)

    def notify(self, message: str, message_type: MessageType):
        self.clearMessage()
        self.label.hide()

        if message_type == MessageType.INFO:
            self.showMessage(message, 3000)
        else:
            self.label.setText(message)
            self.label.show()
