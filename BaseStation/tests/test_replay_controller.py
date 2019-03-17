import unittest
from unittest.mock import Mock, MagicMock, patch

from src.data_processing.consumer import Consumer
from src.replay.file_data_producer import FileDataProducer
from src.replay_controller import ReplayController
from src.ui.replay_widget import ReplayWidget
from tests.builders.config_builder import ConfigBuilder


class ReplayControllerTest(unittest.TestCase):

    PACKET_COUNT = 0

    def setUp(self):
        self.replay_widget = Mock(spec=ReplayWidget)
        self.file_data_producer = Mock(spec=FileDataProducer)
        self.file_data_producer.get_total_packet_count.return_value = self.PACKET_COUNT
        self.consumer = MagicMock(spec=Consumer)

        config = ConfigBuilder().build()

        self.replay_controller = ReplayController(self.replay_widget, self.file_data_producer, self.consumer, config)

    def test_init_should_set_control_bar_max_value(self):
        self.replay_widget.set_control_bar_max_value.assert_called_with(self.PACKET_COUNT - 1)

    def test_control_bar_callback_should_pass_frame_index_to_data_producer(self):
        frame_index = 3

        self.replay_controller.control_bar_callback(frame_index)

        self.file_data_producer.set_current_packet_index.assert_called_with(frame_index)

    @patch("src.controller.Thread")
    def test_deactivate_should_stop_thread_when_is_running(self, thread_mock):
        self.replay_controller.is_running = True
        self.replay_controller.thread = thread_mock

        self.replay_controller.deactivate()

        thread_mock.join.assert_called_with()
        self.file_data_producer.stop.assert_called_with()

    @patch("src.controller.Thread")
    def test_deactivate_should_not_stop_thread_when_is_not_running(self, thread_mock):
        self.replay_controller.is_running = False
        self.replay_controller.thread = thread_mock

        self.replay_controller.deactivate()

        thread_mock.join.assert_not_called()
        self.file_data_producer.stop.assert_not_called()

    def test_deactivate_should_reset_consumer(self):
        self.replay_controller.is_running = False

        self.replay_controller.deactivate()

        self.consumer.reset.assert_called_with()

    def test_deactivate_should_reset_ui(self):
        self.replay_controller.is_running = False

        self.replay_controller.deactivate()

        self.replay_widget.reset.assert_called_with()

    def test_deactivate_should_return_true(self):
        self.replay_controller.is_running = False

        deactivated = self.replay_controller.deactivate()

        self.assertTrue(deactivated)
