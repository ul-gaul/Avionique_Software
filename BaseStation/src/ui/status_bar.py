from PyQt5.QtWidgets import QStatusBar, QLabel

from src.message_listener import MessageListener, MessageType


class StatusBar(QStatusBar, MessageListener):

    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("status_bar")

        self.label = QLabel(self)
        self.label.setObjectName("status_bar_label")
        self.addWidget(self.label)

    def notify(self, message: str, message_type: MessageType):
        self.clearMessage()
        self.label.hide()

        if message_type == MessageType.INFO:
            self.showMessage(message, 3000)
        else:
            self.label.setText(message)
            self.label.show()
