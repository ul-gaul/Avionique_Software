import unittest
from unittest.mock import patch

from src.replay_controller import ReplayController


class ReplayControllerTest(unittest.TestCase):

    PACKET_COUNT = 0

    def setUp(self):
        self.replay_widget_patcher = patch('src.ui.replay_widget.ReplayWidget')
        self.file_data_producer_patcher = patch('src.file_data_producer.FileDataProducer')
        self.consumer_patcher = patch('src.consumer.Consumer')

        replay_widget_class = self.replay_widget_patcher.start()
        file_data_producer_class = self.file_data_producer_patcher.start()
        self.consumer_patcher.start()

        self.addCleanup(self.clean_up)

        self.replay_widget = replay_widget_class()
        self.file_data_producer = file_data_producer_class()
        self.file_data_producer.get_total_packet_count.return_value = self.PACKET_COUNT

        self.replay_controller = ReplayController(self.replay_widget, self.file_data_producer)

    def test_init_should_set_control_bar_max_value(self):
        self.replay_widget.set_control_bar_max_value.assert_called_with(self.PACKET_COUNT - 1)

    def test_control_bar_callback_should_pass_frame_index_to_data_producer(self):
        frame_index = 3

        self.replay_controller.control_bar_callback(frame_index)

        self.file_data_producer.set_current_packet_index.assert_called_with(frame_index)

    def clean_up(self):
        """
        This is used instead of the tearDown method because if an exception is raised in setUp, tearDown is not called,
        but we still need to undo the patching.
        """
        self.replay_widget_patcher.stop()
        self.file_data_producer_patcher.stop()
        self.consumer_patcher.stop()
