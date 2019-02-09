from src.message_sender import MessageSender
from src.message_type import MessageType


class ChecksumValidator(MessageSender):

    def validate(self, data_array: bytes):
        checksum = sum(data_array) % 256
        if checksum == 255:
            return True
        else:
            self.notify_all_message_listeners("Invalid Checksum : expected = 255, calculated = {}".format(checksum),
                                              MessageType.WARNING)
            return False
