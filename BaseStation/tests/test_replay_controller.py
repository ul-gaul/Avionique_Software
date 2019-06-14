import unittest
from unittest.mock import Mock, MagicMock, patch

from src.data_processing.consumer import Consumer
from src.data_processing.consumer_factory import ConsumerFactory
from src.replay.file_data_producer import FileDataProducer
from src.replay_controller import ReplayController
from src.ui.replay_widget import ReplayWidget
from tests.builders.config_builder import ConfigBuilder


class ReplayControllerTest(unittest.TestCase):
    PACKET_COUNT = 0
    A_FILENAME = "path/to/file.csv"
    ALTITUDE_DATA = [0, 5000, 10000]

    def setUp(self):
        self.replay_widget = Mock(spec=ReplayWidget)
        self.file_data_producer = Mock(spec=FileDataProducer)
        self.file_data_producer.get_total_packet_count.return_value = self.PACKET_COUNT

        self.consumer = MagicMock(spec=Consumer)
        self.consumer_factory = Mock(spec=ConsumerFactory)
        self.consumer_factory.create.return_value = self.consumer   # FIXME: validate input parameters

        config = ConfigBuilder().build()

        self.replay_controller = ReplayController(self.replay_widget, self.file_data_producer, self.consumer_factory,
                                                  config)

    def test_control_bar_callback_should_pass_frame_index_to_data_producer(self):
        frame_index = 3

        self.replay_controller.control_bar_callback(frame_index)

        self.file_data_producer.set_current_packet_index.assert_called_with(frame_index)

    @patch("src.controller.Thread")
    def test_play_pause_button_callback_should_restart_data_producer_when_is_paused(self, _):
        self.file_data_producer.is_suspended.return_value = True

        self.replay_controller.play_pause_button_callback()

        self.file_data_producer.restart.assert_called_with()

    @patch("src.controller.Thread")
    def test_play_pause_button_callback_should_start_thread_when_is_paused_and_not_running(self, thread):
        thread_mock = thread.return_value
        self.file_data_producer.is_suspended.return_value = True
        self.replay_controller.is_running = False

        self.replay_controller.play_pause_button_callback()

        self.file_data_producer.start.assert_called_with()
        thread_mock.start.assert_called_with()

    @patch("src.controller.Thread")
    def test_play_pause_button_callback_should_not_start_thread_when_is_paused_and_running(self, thread):
        thread_mock = thread.return_value
        self.file_data_producer.is_suspended.return_value = True
        self.replay_controller.is_running = True

        self.replay_controller.play_pause_button_callback()

        self.file_data_producer.start.assert_not_called()
        thread_mock.start.assert_not_called()

    @patch("src.controller.Thread")
    def test_play_pause_button_callback_should_set_pause_button_text_when_is_paused(self, _):
        self.file_data_producer.is_suspended.return_value = True

        self.replay_controller.play_pause_button_callback()

        self.replay_widget.set_pause_button_text.assert_called_with()

    def test_play_pause_button_callback_should_suspend_data_producer_when_is_playing(self):
        self.file_data_producer.is_suspended.return_value = False

        self.replay_controller.play_pause_button_callback()

        self.file_data_producer.suspend.assert_called_with()

    def test_play_pause_button_callback_should_set_play_button_text_when_is_playing(self):
        self.file_data_producer.is_suspended.return_value = False

        self.replay_controller.play_pause_button_callback()

        self.replay_widget.set_play_button_text.assert_called_with()

    def test_activate_should_load_data(self):
        self.replay_controller.activate(self.A_FILENAME)

        self.file_data_producer.load.assert_called_with(self.A_FILENAME)

    def test_activate_should_reset_playback_state(self):
        self.replay_controller.activate(self.A_FILENAME)

        self.file_data_producer.reset_playback_state.assert_called_with()

    def test_activate_should_set_control_bar_max_value(self):
        self.replay_controller.activate(self.A_FILENAME)

        self.replay_widget.set_control_bar_max_value.assert_called_with(self.PACKET_COUNT - 1)

    def test_activate_should_update_consumer(self):
        self.replay_controller.activate(self.A_FILENAME)

        self.consumer.update.assert_called_with()

    def test_activate_should_set_play_button_text(self):
        self.replay_controller.activate(self.A_FILENAME)

        self.replay_widget.set_play_button_text.assert_called_with()

    def test_activate_should_update_ui(self):
        self.consumer.__getitem__.return_value = self.ALTITUDE_DATA

        self.replay_controller.activate(self.A_FILENAME)

        self.replay_widget.draw_altitude.assert_called_with(self.ALTITUDE_DATA)

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

    def test_deactivate_should_reset_ui(self):
        self.replay_controller.is_running = False

        self.replay_controller.deactivate()

        self.replay_widget.reset.assert_called_with()

    def test_deactivate_should_return_true(self):
        self.replay_controller.is_running = False

        deactivated = self.replay_controller.deactivate()

        self.assertTrue(deactivated)
