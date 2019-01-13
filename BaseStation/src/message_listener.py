import abc

from src.message_type import MessageType


class MessageListener:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def notify(self, message: str, message_type: MessageType):
        pass
