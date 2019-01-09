import unittest
from unittest.mock import patch, Mock

from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMessageBox

from src.message_listener import MessageListener
from src.message_type import MessageType
from src.real_time_controller import RealTimeController
from src.serial_data_producer import SerialDataProducer
from src.ui.real_time_widget import RealTimeWidget


class RealTimeControllerTest(unittest.TestCase):

    VALID_SAVE_FILE_NAME = "file.csv"
    EMPTY_SAVE_FILE_NAME = ""

    def setUp(self):
        self.thread_patcher = patch("src.controller.Thread")
        self.thread_patcher.start()
        self.addCleanup(self.thread_patcher.stop)

        self.real_time_widget = Mock(spec=RealTimeWidget)
        self.serial_data_producer = Mock(spec=SerialDataProducer)
        self.event = Mock(spec=QCloseEvent)

        self.real_time_controller = RealTimeController(self.real_time_widget, self.serial_data_producer)
        self.real_time_controller.is_running = False

    def test_save_data_should_call_serial_data_producer(self):
        self.real_time_controller.save_data(self.VALID_SAVE_FILE_NAME)

        self.serial_data_producer.save.assert_called_with(self.VALID_SAVE_FILE_NAME)

    def test_save_data_should_notify_message_listeners(self):
        listener = MessageListener()
        listener.notify = Mock()
        self.real_time_controller.register_message_listener(listener)

        self.real_time_controller.save_data(self.VALID_SAVE_FILE_NAME)

        filename_argument = listener.notify.call_args[0][0]
        message_type_argument = listener.notify.call_args[0][1]
        self.assertTrue(self.VALID_SAVE_FILE_NAME in filename_argument)
        self.assertEqual(message_type_argument, MessageType.INFO)

    def test_on_close_should_stop_thread_if_is_running(self):
        self.real_time_controller.is_running = True
        self.serial_data_producer.has_unsaved_data.return_value = False

        self.real_time_controller.on_close(self.event)

        self.real_time_controller.thread.join.assert_called_with()
        self.serial_data_producer.stop.assert_called_with()

    def test_on_close_should_not_close_when_user_chooses_no_save_file(self):
        self.serial_data_producer.has_unsaved_data.return_value = True
        self.real_time_widget.show_save_message_box.return_value = QMessageBox.Yes
        self.real_time_widget.get_save_file_name.return_value = self.EMPTY_SAVE_FILE_NAME

        self.real_time_controller.on_close(self.event)

        self.event.ignore.assert_called_with()

    def test_on_close_should_not_save_data_when_user_chooses_no_save_file(self):
        self.serial_data_producer.has_unsaved_data.return_value = True
        self.real_time_widget.show_save_message_box.return_value = QMessageBox.Yes
        self.real_time_widget.get_save_file_name.return_value = self.EMPTY_SAVE_FILE_NAME

        self.real_time_controller.on_close(self.event)

        self.serial_data_producer.save.assert_not_called()

    def test_on_close_should_save_data_when_user_chooses_valid_save_file(self):
        self.serial_data_producer.has_unsaved_data.return_value = True
        self.real_time_widget.show_save_message_box.return_value = QMessageBox.Yes
        self.real_time_widget.get_save_file_name.return_value = self.VALID_SAVE_FILE_NAME

        self.real_time_controller.on_close(self.event)

        self.serial_data_producer.save.assert_called_with(self.VALID_SAVE_FILE_NAME)

    def test_on_close_should_close_when_user_chooses_valid_save_file(self):
        self.serial_data_producer.has_unsaved_data.return_value = True
        self.real_time_widget.show_save_message_box.return_value = QMessageBox.Yes
        self.real_time_widget.get_save_file_name.return_value = self.VALID_SAVE_FILE_NAME

        self.real_time_controller.on_close(self.event)

        self.event.accept.assert_called_with()

    def test_on_close_should_close_when_user_doesnt_save(self):
        self.serial_data_producer.has_unsaved_data.return_value = True
        self.real_time_widget.show_save_message_box.return_value = QMessageBox.No

        self.real_time_controller.on_close(self.event)

        self.event.accept.assert_called_with()

    def test_on_close_should_not_save_data_when_user_doesnt_save(self):
        self.serial_data_producer.has_unsaved_data.return_value = True
        self.real_time_widget.show_save_message_box.return_value = QMessageBox.No

        self.real_time_controller.on_close(self.event)

        self.serial_data_producer.save.assert_not_called()

    def test_on_close_should_not_close_when_user_cancels(self):
        self.serial_data_producer.has_unsaved_data.return_value = True
        self.real_time_widget.show_save_message_box.return_value = QMessageBox.Cancel

        self.real_time_controller.on_close(self.event)

        self.event.ignore.assert_called_with()

    def test_on_close_should_not_save_data_when_user_cancels(self):
        self.serial_data_producer.has_unsaved_data.return_value = True
        self.real_time_widget.show_save_message_box.return_value = QMessageBox.Cancel

        self.real_time_controller.on_close(self.event)

        self.serial_data_producer.save.assert_not_called()

    def test_on_close_should_close_when_no_unsaved_data(self):
        self.serial_data_producer.has_unsaved_data.return_value = False

        self.real_time_controller.on_close(self.event)

        self.event.accept.assert_called_with()
