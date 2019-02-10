from src.message_listener import MessageListener
from src.message_type import MessageType


class MessageSender:
    def __init__(self):
        self.message_listeners = []

    def register_message_listener(self, message_listener: MessageListener):
        self.message_listeners.append(message_listener)

    def notify_all_message_listeners(self, message: str, message_type: MessageType):
        for message_listener in self.message_listeners:
            message_listener.notify(message, message_type)
