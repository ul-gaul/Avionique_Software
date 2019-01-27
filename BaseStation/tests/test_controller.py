import unittest
from unittest.mock import Mock

from src.consumer import Consumer
from src.controller import Controller
from src.data_producer import DataProducer
from src.message_listener import MessageListener
from src.message_type import MessageType
from src.ui.data_widget import DataWidget
from tests.builders.config_builder import ConfigBuilder


class ControllerTest(unittest.TestCase):

    MESSAGE = "A MESSAGE"
    MESSAGE_TYPE = MessageType.INFO

    def setUp(self):
        self.data_widget = Mock(spec=DataWidget)
        self.data_producer = Mock(spec=DataProducer)
        self.consumer = Mock(spec=Consumer)

        self.message_listener1 = MessageListener()
        self.message_listener1.notify = Mock()
        self.message_listener2 = MessageListener()
        self.message_listener2.notify = Mock()

        config = ConfigBuilder().build()

        self.controller = Controller(self.data_widget, self.data_producer, self.consumer, config)

    def test_register_message_listener_should_add_listener_in_list(self):
        self.controller.register_message_listener(self.message_listener1)
        self.controller.register_message_listener(self.message_listener2)

        num_listeners = len(self.controller.message_listeners)
        self.assertEqual(num_listeners, 2)

    def test_notify_all_message_listeners_should_call_notify_on_each_listeners(self):
        self.controller.register_message_listener(self.message_listener1)
        self.controller.register_message_listener(self.message_listener2)

        self.controller.notify_all_message_listeners(self.MESSAGE, self.MESSAGE_TYPE)

        self.message_listener1.notify.assert_called_with(self.MESSAGE, self.MESSAGE_TYPE)
        self.message_listener2.notify.assert_called_with(self.MESSAGE, self.MESSAGE_TYPE)
