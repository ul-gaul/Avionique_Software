import unittest
from unittest.mock import patch, Mock

from src.file_data_producer import FileDataProducer
from src.replay_controller import ReplayController
from src.ui.replay_widget import ReplayWidget
from tests.builders.config_builder import ConfigBuilder


class ReplayControllerTest(unittest.TestCase):

    PACKET_COUNT = 0

    def setUp(self):
        self.consumer_patcher = patch('src.replay_controller.Consumer', autospec=True)
        self.consumer_patcher.start()
        self.addCleanup(self.consumer_patcher.stop)

        self.replay_widget = Mock(spec=ReplayWidget)
        self.file_data_producer = Mock(spec=FileDataProducer)
        self.file_data_producer.get_total_packet_count.return_value = self.PACKET_COUNT

        config = ConfigBuilder().build()

        self.replay_controller = ReplayController(self.replay_widget, self.file_data_producer, config)

    def test_init_should_set_control_bar_max_value(self):
        self.replay_widget.set_control_bar_max_value.assert_called_with(self.PACKET_COUNT - 1)

    def test_control_bar_callback_should_pass_frame_index_to_data_producer(self):
        frame_index = 3

        self.replay_controller.control_bar_callback(frame_index)

        self.file_data_producer.set_current_packet_index.assert_called_with(frame_index)
