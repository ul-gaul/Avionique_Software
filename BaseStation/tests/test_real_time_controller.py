import unittest
from unittest.mock import patch, Mock, MagicMock

from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMessageBox

from src.consumer import Consumer
from src.message_listener import MessageListener
from src.message_type import MessageType
from src.real_time_controller import RealTimeController
from src.serial_data_producer import SerialDataProducer
from src.ui.real_time_widget import RealTimeWidget
from tests.builders.config_builder import ConfigBuilder


class RealTimeControllerTest(unittest.TestCase):

    VALID_SAVE_FILE_NAME = "file.csv"
    EMPTY_SAVE_FILE_NAME = ""

    def setUp(self):
        self.real_time_widget = Mock(spec=RealTimeWidget)
        self.serial_data_producer = Mock(spec=SerialDataProducer)
        self.consumer = MagicMock(spec=Consumer)
        self.event = Mock(spec=QCloseEvent)

        config = ConfigBuilder().build()

        self.real_time_controller = RealTimeController(self.real_time_widget, self.serial_data_producer, self.consumer,
                                                       config)
        self.real_time_controller.is_running = False

    @patch("src.controller.Thread")
    def test_real_time_button_callback_should_stop_thread_when_is_running(self, thread):
        thread_mock = thread.return_value
        self.real_time_controller.is_running = True
        self.real_time_controller.thread = thread_mock

        self.real_time_controller.real_time_button_callback()

        thread_mock.join.assert_called_with()
        self.serial_data_producer.stop.assert_called_with()

    @patch("src.controller.Thread")
    def test_real_time_button_callback_should_update_button_text_when_is_running(self, thread):
        thread_mock = thread.return_value
        self.real_time_controller.is_running = True
        self.real_time_controller.thread = thread_mock

        self.real_time_controller.real_time_button_callback()

        self.real_time_widget.update_button_text.assert_called_with(False)

    @patch("src.controller.Thread")
    def test_real_time_button_callback_should_start_thread_when_is_not_running(self, thread):
        thread_mock = thread.return_value

        self.real_time_controller.real_time_button_callback()

        self.serial_data_producer.start.assert_called_with()
        thread_mock.start.assert_called_with()

    @patch("src.controller.Thread")
    def test_real_time_button_callback_should_update_button_text_when_is_not_running(self, _):
        self.real_time_controller.real_time_button_callback()

        self.real_time_widget.update_button_text.assert_called_with(True)

    @patch("src.controller.Thread")
    def test_real_time_button_callback_should_save_if_unsaved_data_and_user_saves_when_is_not_running(self, _):
        self.serial_data_producer.has_unsaved_data.return_value = True
        self.real_time_widget.show_save_message_box.return_value = QMessageBox.Yes
        self.real_time_widget.get_save_file_name.return_value = self.VALID_SAVE_FILE_NAME

        self.real_time_controller.real_time_button_callback()

        self.serial_data_producer.save.assert_called_with(self.VALID_SAVE_FILE_NAME)

    @patch("src.controller.Thread")
    def test_real_time_button_callback_should_not_save_when_unsaved_data_and_user_doesnt_save(self, _):
        self.serial_data_producer.has_unsaved_data.return_value = True
        self.real_time_widget.show_save_message_box.return_value = QMessageBox.No

        self.real_time_controller.real_time_button_callback()

        self.serial_data_producer.save.assert_not_called()

    @patch("src.controller.Thread")
    def test_real_time_button_callback_should_reset_consumer_when_unsaved_data(self, _):
        self.serial_data_producer.has_unsaved_data.return_value = True
        self.real_time_widget.show_save_message_box.return_value = QMessageBox.No

        self.real_time_controller.real_time_button_callback()

        self.consumer.reset.assert_called_with()

    @patch("src.controller.Thread")
    def test_real_time_button_callback_should_reset_ui_when_unsaved_data(self, _):
        self.serial_data_producer.has_unsaved_data.return_value = True
        self.real_time_widget.show_save_message_box.return_value = QMessageBox.No

        self.real_time_controller.real_time_button_callback()

        self.real_time_widget.reset.assert_called_with()

    @patch("src.controller.Thread")
    def test_real_time_button_callback_should_do_nothing_if_user_chooses_no_filename_when_saving(self, thread):
        thread_mock = thread.return_value
        self.serial_data_producer.has_unsaved_data.return_value = True
        self.real_time_widget.show_save_message_box.return_value = QMessageBox.Yes
        self.real_time_widget.get_save_file_name.return_value = self.EMPTY_SAVE_FILE_NAME

        self.real_time_controller.real_time_button_callback()

        self.consumer.reset.assert_not_called()
        self.real_time_widget.reset.assert_not_called()
        self.serial_data_producer.start.assert_not_called()
        self.serial_data_producer.save.assert_not_called()
        thread_mock.start.assert_not_called()

    @patch("src.controller.Thread")
    def test_real_time_button_callback_should_do_nothing_when_unsaved_data_and_user_cancels(self, thread):
        thread_mock = thread.return_value
        self.serial_data_producer.has_unsaved_data.return_value = True
        self.real_time_widget.show_save_message_box.return_value = QMessageBox.Cancel
        self.real_time_widget.get_save_file_name.return_value = self.EMPTY_SAVE_FILE_NAME

        self.real_time_controller.real_time_button_callback()

        self.consumer.reset.assert_not_called()
        self.real_time_widget.reset.assert_not_called()
        self.serial_data_producer.start.assert_not_called()
        self.serial_data_producer.save.assert_not_called()
        thread_mock.start.assert_not_called()

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

    @patch("src.controller.Thread")
    def test_on_close_should_stop_thread_if_is_running(self, thread):
        thread_mock = thread.return_value
        self.real_time_controller.is_running = True
        self.real_time_controller.thread = thread_mock
        self.serial_data_producer.has_unsaved_data.return_value = False

        self.real_time_controller.on_close(self.event)

        thread_mock.join.assert_called_with()
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
