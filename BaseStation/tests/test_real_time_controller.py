import unittest
from unittest.mock import Mock, MagicMock, ANY

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QCloseEvent

from src.data_processing.consumer_factory import ConsumerFactory
from src.message_listener import MessageListener
from src.message_type import MessageType
from src.real_time_controller import RealTimeController
from src.realtime.serial_data_producer import SerialDataProducer, NoConnectedDeviceException
from src.save import SaveManager, SaveStatus
from src.ui.real_time_widget import RealTimeWidget
from tests.builders.config_builder import ConfigBuilder


class RealTimeControllerTest(unittest.TestCase):

    VALID_SAVE_FILE_NAME = "file.csv"
    EMPTY_SAVE_FILE_NAME = ""
    A_ROCKET_PACKET_VERSION = 2019

    def setUp(self):
        self.real_time_widget = Mock(spec=RealTimeWidget)
        self.serial_data_producer = Mock(spec=SerialDataProducer)
        self.consumer_factory = MagicMock(spec=ConsumerFactory)
        self.save_manager = Mock(spec=SaveManager)
        self.event = Mock(spec=QCloseEvent)

        self.config = ConfigBuilder().with_rocket_packet_version(self.A_ROCKET_PACKET_VERSION).build()
        self.qtimer = Mock(spec=QTimer)

        self.real_time_controller = RealTimeController(self.real_time_widget, self.serial_data_producer,
                                                       self.consumer_factory, self.save_manager, self.config,
                                                       self.qtimer)
        self.real_time_controller.is_running = False

    def test_real_time_button_callback_should_stop_timer_when_is_running(self):
        self.real_time_controller.is_running = True

        self.real_time_controller.real_time_button_callback()

        self.qtimer.stop.assert_called_with()
        self.serial_data_producer.stop.assert_called_with()

    def test_real_time_button_callback_should_update_button_text_when_is_running(self):
        self.real_time_controller.is_running = True

        self.real_time_controller.real_time_button_callback()

        self.real_time_widget.update_button_text.assert_called_with(False)

    def test_real_time_button_callback_should_start_timer_when_is_not_running(self):
        self.serial_data_producer.has_unsaved_data.return_value = True

        self.real_time_controller.real_time_button_callback()

        self.serial_data_producer.start.assert_called_with()
        self.qtimer.start.assert_called_with(ANY)

    def test_real_time_button_callback_should_update_button_text_when_is_not_running(self):
        self.serial_data_producer.has_unsaved_data.return_value = True

        self.real_time_controller.real_time_button_callback()

        self.real_time_widget.update_button_text.assert_called_with(True)

    def test_real_time_button_callback_should_create_new_consumer_when_is_not_running(self):
        self.serial_data_producer.has_unsaved_data.return_value = True
        self.save_manager.save.return_value = SaveStatus.SAVED

        self.real_time_controller.real_time_button_callback()

        self.consumer_factory.create.assert_called_with(self.serial_data_producer, self.A_ROCKET_PACKET_VERSION,
                                                        self.config)

    def test_real_time_button_callback_should_reset_ui_when_is_not_running(self):
        self.serial_data_producer.has_unsaved_data.return_value = True
        self.save_manager.save.return_value = SaveStatus.SAVED

        self.real_time_controller.real_time_button_callback()

        self.real_time_widget.reset.assert_called_with()

    def test_real_time_button_callback_should_do_nothing_when_unsaved_data_and_save_status_is_cancelled(self):
        self.serial_data_producer.has_unsaved_data.return_value = True
        self.save_manager.save.return_value = SaveStatus.CANCELLED

        self.real_time_controller.real_time_button_callback()

        self.consumer_factory.create.assert_not_called()
        self.real_time_widget.reset.assert_not_called()
        self.real_time_widget.update_button_text.assert_not_called()
        self.serial_data_producer.start.assert_not_called()
        self.qtimer.start.assert_not_called()

    def test_real_time_button_callback_should_notify_message_listeners_when_data_producer_throws_exception(self):
        error_message = "message"
        self.serial_data_producer.start.side_effect = NoConnectedDeviceException(error_message)
        self.serial_data_producer.has_unsaved_data.return_value = False
        message_listener = Mock(spec=MessageListener)
        self.real_time_controller.register_message_listener(message_listener)

        self.real_time_controller.real_time_button_callback()

        message_listener.notify.assert_called_with(error_message, MessageType.ERROR)

    def test_on_close_should_stop_timer_if_is_running(self):
        self.real_time_controller.is_running = True
        self.serial_data_producer.has_unsaved_data.return_value = False

        self.real_time_controller.on_close(self.event)

        self.qtimer.stop.assert_called_with()
        self.serial_data_producer.stop.assert_called_with()

    def test_on_close_should_stop_timer_when_is_running_and_save_status_is_not_cancelled(self):
        self.real_time_controller.is_running = True
        self.serial_data_producer.has_unsaved_data.return_value = True
        self.save_manager.save.return_value = SaveStatus.SAVED

        self.real_time_controller.on_close(self.event)

        self.qtimer.stop.assert_called_with()
        self.serial_data_producer.stop.assert_called_with()

    def test_on_close_should_not_close_when_cancelled_save_status(self):
        self.serial_data_producer.has_unsaved_data.return_value = True
        self.save_manager.save.return_value = SaveStatus.CANCELLED

        self.real_time_controller.on_close(self.event)

        self.event.ignore.assert_called_with()

    def test_on_close_should_not_stop_timer_when_cancelled_save_status(self):
        self.serial_data_producer.has_unsaved_data.return_value = True
        self.save_manager.save.return_value = SaveStatus.CANCELLED

        self.real_time_controller.on_close(self.event)

        self.serial_data_producer.save.assert_not_called()
        self.qtimer.stop.assert_not_called()

    def test_on_close_should_close_when_saved_save_status(self):
        self.serial_data_producer.has_unsaved_data.return_value = True
        self.save_manager.save.return_value = SaveStatus.SAVED

        self.real_time_controller.on_close(self.event)

        self.event.accept.assert_called_with()

    def test_on_close_should_close_when_unsaved_save_status(self):
        self.serial_data_producer.has_unsaved_data.return_value = True
        self.save_manager.save.return_value = SaveStatus.UNSAVED

        self.real_time_controller.on_close(self.event)

        self.event.accept.assert_called_with()

    def test_on_close_should_close_when_no_unsaved_data(self):
        self.serial_data_producer.has_unsaved_data.return_value = False

        self.real_time_controller.on_close(self.event)

        self.event.accept.assert_called_with()

    def test_activate_should_update_button_text(self):
        self.real_time_controller.activate("")

        self.real_time_widget.update_button_text.assert_called_with(False)

    def test_deactivate_should_stop_timer_when_is_running(self):
        self.real_time_controller.is_running = True
        self.serial_data_producer.has_unsaved_data.return_value = False

        self.real_time_controller.deactivate()

        self.qtimer.stop.assert_called_with()
        self.serial_data_producer.stop.assert_called_with()

    def test_deactivate_should_clear_data_producer(self):
        self.real_time_controller.is_running = False
        self.serial_data_producer.has_unsaved_data.return_value = False

        self.real_time_controller.deactivate()

        self.serial_data_producer.clear_rocket_packets.assert_called_with()

    def test_deactivate_should_reset_data_widget(self):
        self.real_time_controller.is_running = False
        self.serial_data_producer.has_unsaved_data.return_value = False

        self.real_time_controller.deactivate()

        self.real_time_widget.reset.assert_called_with()

    def test_deactivate_should_return_true_when_save_status_is_not_cancelled(self):
        self.real_time_controller.is_running = False
        self.serial_data_producer.has_unsaved_data.return_value = True
        self.save_manager.save.return_value = SaveStatus.SAVED

        is_deactivated = self.real_time_controller.deactivate()

        self.assertTrue(is_deactivated)

    def test_deactivate_should_do_nothing_when_save_status_is_cancelled(self):
        self.real_time_controller.is_running = True
        self.serial_data_producer.has_unsaved_data.return_value = True
        self.save_manager.save.return_value = SaveStatus.CANCELLED

        self.real_time_controller.deactivate()

        self.serial_data_producer.clear_rocket_packets.assert_not_called()
        self.real_time_widget.reset.assert_not_called()
        self.qtimer.stop.assert_not_called()
        self.serial_data_producer.stop.assert_not_called()

    def test_deactivate_should_return_false_when_save_status_is_cancelled(self):
        self.real_time_controller.is_running = True
        self.serial_data_producer.has_unsaved_data.return_value = True
        self.save_manager.save.return_value = SaveStatus.CANCELLED

        is_deactivated = self.real_time_controller.deactivate()

        self.assertFalse(is_deactivated)
