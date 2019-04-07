from unittest import TestCase
from unittest.mock import Mock

from PyQt5.QtWidgets import QMessageBox

from src.message_listener import MessageListener
from src.message_type import MessageType
from src.realtime.serial_data_producer import SerialDataProducer
from src.save import SaveManager, SaveStatus
from src.ui.real_time_widget import RealTimeWidget
from tests.matchers import AnyStringWith


class SaveManagerTest(TestCase):

    A_FILE_NAME = "path/to/file.csv"
    EMPTY_FILE_NAME = ""

    def setUp(self):
        self.serial_data_producer = Mock(spec=SerialDataProducer)
        self.real_time_widget = Mock(spec=RealTimeWidget)

        self.save_manager = SaveManager(self.serial_data_producer, self.real_time_widget)

    def test_save_should_save_when_user_saves(self):
        self.real_time_widget.show_save_message_box.return_value = QMessageBox.Yes
        self.real_time_widget.get_save_file_name.return_value = self.A_FILE_NAME

        self.save_manager.save()

        self.serial_data_producer.save.assert_called_with(self.A_FILE_NAME)

    def test_save_should_notify_message_listener_when_user_saves(self):
        listener = Mock(spec=MessageListener)
        self.save_manager.register_message_listener(listener)
        self.real_time_widget.show_save_message_box.return_value = QMessageBox.Yes
        self.real_time_widget.get_save_file_name.return_value = self.A_FILE_NAME

        self.save_manager.save()

        listener.notify.assert_called_with(AnyStringWith(self.A_FILE_NAME), MessageType.INFO)

    def test_save_should_return_saved_status_when_user_saves(self):
        self.real_time_widget.show_save_message_box.return_value = QMessageBox.Yes
        self.real_time_widget.get_save_file_name.return_value = self.A_FILE_NAME

        save_status = self.save_manager.save()

        self.assertEqual(save_status, SaveStatus.SAVED)

    def test_save_should_not_save_when_user_chooses_no_file(self):
        self.real_time_widget.show_save_message_box.return_value = QMessageBox.Yes
        self.real_time_widget.get_save_file_name.return_value = self.EMPTY_FILE_NAME

        self.save_manager.save()

        self.serial_data_producer.save.assert_not_called()

    def test_save_should_return_cancelled_status_when_user_chooses_no_file(self):
        self.real_time_widget.show_save_message_box.return_value = QMessageBox.Yes
        self.real_time_widget.get_save_file_name.return_value = self.EMPTY_FILE_NAME

        save_status = self.save_manager.save()

        self.assertEqual(save_status, SaveStatus.CANCELLED)

    def test_save_should_not_save_when_user_doesnt_save(self):
        self.real_time_widget.show_save_message_box.return_value = QMessageBox.No

        self.save_manager.save()

        self.serial_data_producer.save.assert_not_called()

    def test_save_should_return_unsaved_status_when_user_doesnt_save(self):
        self.real_time_widget.show_save_message_box.return_value = QMessageBox.No

        save_status = self.save_manager.save()

        self.assertEqual(save_status, SaveStatus.UNSAVED)

    def test_save_should_not_save_when_user_cancels(self):
        self.real_time_widget.show_save_message_box.return_value = QMessageBox.Cancel

        self.save_manager.save()

        self.serial_data_producer.save.assert_not_called()

    def test_save_should_return_cancelled_status_when_user_cancels(self):
        self.real_time_widget.show_save_message_box.return_value = QMessageBox.Cancel

        save_status = self.save_manager.save()

        self.assertEqual(save_status, SaveStatus.CANCELLED)
