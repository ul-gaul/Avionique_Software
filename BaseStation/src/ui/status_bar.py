from PyQt5.QtWidgets import QStatusBar

from src.message_listener import MessageListener, MessageType


class StatusBar(QStatusBar, MessageListener):

    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("status_bar")

    def notify(self, message: str, message_type: MessageType):
        # TODO: add different behavior for every message type
        self.showMessage(message, 3000)
        print(message_type)
