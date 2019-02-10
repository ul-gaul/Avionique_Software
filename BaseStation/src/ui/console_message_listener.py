from src.message_listener import MessageListener
from src.message_type import MessageType


class ConsoleMessageListener(MessageListener):

    def notify(self, message: str, message_type: MessageType):
        print("[{}] {}".format(message_type.name, message))
