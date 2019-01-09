import unittest
from unittest.mock import patch, Mock

from PyQt5.QtGui import QCloseEvent

from src.real_time_controller import RealTimeController


class RealTimeControllerTest(unittest.TestCase):

    def setUp(self):
        # TODO: check if this can't be simplified
        self.real_time_widget_patcher = patch("src.ui.real_time_widget.RealTimeWidget")
        self.serial_data_producer_patcher = patch("src.serial_data_producer.SerialDataProducer")
        self.thread_patcher = patch("threading.Thread")

        real_time_widget_class = self.real_time_widget_patcher.start()
        serial_data_producer_class = self.serial_data_producer_patcher.start()
        self.thread_patcher.start()

        self.addCleanup(self.clean_up)

        self.real_time_widget = real_time_widget_class()
        self.serial_data_producer = serial_data_producer_class()
        self.real_time_controller = RealTimeController(self.real_time_widget, self.serial_data_producer)

        self.event = QCloseEvent()
        self.event.accept = Mock()
        self.event.ignore = Mock()

    # def test_on_close_should_stop_thread_if_is_running(self):
    #     self.real_time_controller.is_running = True
    #     self.serial_data_producer.has_unsaved_data.return_value = False
    #
    #     self.real_time_controller.on_close(self.event)
    #
    #     self.serial_data_producer.stop.assert_was_called()

    def test_on_close_should_close_when_no_unsaved_data(self):
        self.real_time_controller.is_running = False
        self.serial_data_producer.has_unsaved_data.return_value = False

        self.real_time_controller.on_close(self.event)

        self.event.accept.assert_called_with()

    def clean_up(self):
        self.real_time_widget_patcher.stop()
        self.serial_data_producer_patcher.stop()
        self.thread_patcher.stop()
