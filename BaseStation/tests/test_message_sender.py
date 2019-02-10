from unittest import TestCase
from unittest.mock import Mock

from src.message_listener import MessageListener
from src.message_sender import MessageSender
from src.message_type import MessageType


class MessageSenderTest(TestCase):
    MESSAGE = "A MESSAGE"
    MESSAGE_TYPE = MessageType.INFO

    def setUp(self):
        self.message_listener1 = Mock(spec=MessageListener)
        self.message_listener2 = Mock(spec=MessageListener)

        self.messageSender = MessageSender()

    def test_register_message_listener_should_add_listener_in_list(self):
        self.messageSender.register_message_listener(self.message_listener1)
        self.messageSender.register_message_listener(self.message_listener2)

        num_listeners = len(self.messageSender.message_listeners)
        self.assertEqual(num_listeners, 2)

    def test_notify_all_message_listeners_should_call_notify_on_each_listeners(self):
        self.messageSender.register_message_listener(self.message_listener1)
        self.messageSender.register_message_listener(self.message_listener2)

        self.messageSender.notify_all_message_listeners(self.MESSAGE, self.MESSAGE_TYPE)

        self.message_listener1.notify.assert_called_with(self.MESSAGE, self.MESSAGE_TYPE)
        self.message_listener2.notify.assert_called_with(self.MESSAGE, self.MESSAGE_TYPE)
